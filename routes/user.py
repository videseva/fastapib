import io
import uuid
from anyio import Path
from fastapi import APIRouter, HTTPException, Response, UploadFile
from fastapi.responses import FileResponse
from config.db import conn
from models.user import users
from schemas.user import User, UserCount
from typing import List
from starlette.status import HTTP_204_NO_CONTENT
from sqlalchemy import func, select
import boto3;

from cryptography.fernet import Fernet

user = APIRouter()
key = Fernet.generate_key()
f = Fernet(key)

s3 = boto3.client('s3')


bucket_name = 'tallercloud-nuestrobucket'

@user.post("/upload-image", tags=["users"], description="Cargar una imagen en S3")
async def upload_image(file: UploadFile):
    unique_name = f"{uuid.uuid4()}{Path(file.filename).suffix}"
    try:
        s3.upload_fileobj(file.file, bucket_name, unique_name)
    except Exception as e:
        return {"message": "Error al cargar la imagen en S3"}
    file_url = f"https://{bucket_name}.s3.amazonaws.com/{unique_name}"
    return {"message": "Imagen cargada exitosamente", "unique_name": unique_name}

@user.get("/download-image/{nombre_archivo}", tags=["users"], description="Descargar una imagen desde S3")
async def download_image(nombre_archivo:str):

    
    try:
        response = s3.get_object(Bucket=bucket_name, Key=nombre_archivo)
        archivo = response['Body'].read()

        print(f"archivoS3: {str(archivo)}")

        # Convierte los bytes de archivo_bytes a una secuencia de bytes (bytes)
        archivo_bytes = bytes(archivo)
        print(f"archivo_bytes: {str(archivo_bytes)}")

        # Devuelve el archivo como una respuesta binaria
        return FileResponse(io.BytesIO(archivo_bytes), headers={"Content-Disposition": f"attachment; filename={nombre_archivo}"})
    except Exception as e:
         # Registra la excepción real para depuración
        print(f"Error al descargar el archivo desde S3: {str(e)}")
        return {"message": "Error al descargar el archivo desde S3"}
    
    else :
        return archivo
    
@user.get(
    "/users",
    tags=["users"],
    response_model=List[User],
    description="Get a list of all users",
)
def get_users():
   
    return conn.execute(users.select()).fetchall()

@user.get(
    "/users/{id}",
    tags=["users"],
    response_model=User,
    description="Get a single user by Id",
)
def get_user(id: str):
    return conn.execute(users.select().where(users.c.id == id)).first()


@user.post("/users", tags=["users"], response_model=User, description="Crear un nuevo user")
def create_user(user: User):
    new_user = { "id": user.id,"name": user.name, "lastname": user.lastname ,  "email": user.email, "photo":user.photo}
    result = conn.execute(users.insert().values(new_user))
    conn.commit()
    print(new_user)
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()