from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

users = Table(
    "user",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name",String(50)),
    Column("lastname", String(50)),
    Column("email", String(50)),
    Column("photo", String(50)),
)

meta.create_all(engine)