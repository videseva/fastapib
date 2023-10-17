from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[int]
    name: str
    lastname: str
    email: str
    photo: str
    
class UserCount(BaseModel):
    total: int