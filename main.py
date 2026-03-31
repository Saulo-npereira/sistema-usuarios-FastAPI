from fastapi import FastAPI
from models import engine, Base
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()



Base.metadata.create_all(bind=engine)

from usuarios_routes import usuarios_router

app.include_router(usuarios_router)

