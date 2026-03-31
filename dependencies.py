from models import engine, Usuario
from sqlalchemy.orm import sessionmaker, Session
from security import oauth2_schema
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from security import SECRET_KEY, ALGORITHM

def pegar_sessao():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        usuario_email = dic_info.get('sub')
    except JWTError:
        raise HTTPException(status_code=401, detail='acesso negado')

    usuario = session.query(Usuario).filter(Usuario.email==usuario_email).first()
    if not usuario:
        raise HTTPException(status_code=401, detail='credencias invalidas')
    return usuario


