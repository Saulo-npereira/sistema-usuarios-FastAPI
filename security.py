from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer


oauth2_schema = OAuth2PasswordBearer(tokenUrl='usuarios/login-form')

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_TIME = int(os.getenv('ACCESS_TOKEN_EXPIRE_TIME'))
ALGORITHM = os.getenv('ALGORITHM')

bcrypt_context = CryptContext(schemes=['argon2'], deprecated='auto')


