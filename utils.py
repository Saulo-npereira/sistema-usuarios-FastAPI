from security import bcrypt_context
from models import Usuario
from security import ALGORITHM, ACCESS_TOKEN_EXPIRE_TIME, SECRET_KEY
from datetime import datetime, UTC, timedelta
from jose import jwt

def gerar_hash(senha: str):
    return bcrypt_context.hash(senha)


def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    if not bcrypt_context.verify(senha, usuario.senha):
        return False
    return True

def criar_token(dados: dict, duracao = timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)):
    dados_copia = dados.copy()
    expire = datetime.now(UTC) + duracao
    dados_copia.update({'exp': expire})
    token = jwt.encode(dados_copia, SECRET_KEY, algorithm=ALGORITHM)
    return token

