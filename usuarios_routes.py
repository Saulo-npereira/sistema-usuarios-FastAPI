from fastapi import APIRouter, Depends, HTTPException
from schemas import UsuarioSchema, LoginSchema
from dependencies import pegar_sessao, verificar_token
from sqlalchemy.orm import Session
from models import Usuario
from utils import gerar_hash, autenticar_usuario, criar_token
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from security import SECRET_KEY, ALGORITHM

usuarios_router = APIRouter(prefix='/usuarios', tags=['usuario'])

@usuarios_router.post('/criar_usuario')
async def criar_usuario(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail='já existe um usuario com esse email')
    
    usuario = Usuario(
        nome=usuario_schema.nome,
        email=usuario_schema.email,
        senha=gerar_hash(usuario_schema.senha)
    )
    session.add(usuario)
    session.commit()
    raise HTTPException(status_code=201, detail='usuario criado com sucesso')

@usuarios_router.get('/procurar_usuario')
async def proucurar_usuario(usuario_id: int, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.id==usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    return {
        'message': f'usuario de id {usuario.id} encontrado',
        'nome': usuario.nome,
        'email': usuario.email
    }

@usuarios_router.put('/editar_usuario')
async def editar_usuario(usuario_id: int, usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.id==usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    usuario_nome = usuario.nome
    usuario.nome = usuario_schema.nome
    usuario.email = usuario_schema.email
    usuario.senha = gerar_hash(usuario_schema.senha)
    session.commit()
    return {
        'message': f'usuario de nome {usuario_nome} editado com sucesso'
    }
    

@usuarios_router.delete('/deletar_usuario')
def deletar_usuario(usuario_id: int, session: Session = Depends(pegar_sessao), usuario_teste: str = Depends(verificar_token)):
    print(usuario_teste.nome)
    usuario = session.query(Usuario).filter(Usuario.id==usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    session.delete(usuario)
    session.commit()
    raise HTTPException(status_code=200, detail='Usuário deletado com sucesso')

@usuarios_router.post('/logar_usuario')
async def logar_usuario(usuario_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(email=usuario_schema.email, senha=usuario_schema.senha, session=session)
    if not usuario:
        raise HTTPException(status_code=404, detail='Credencias inválidas')
    token = criar_token({'sub': usuario_schema.email})
    refresh = criar_token({'sub': usuario_schema.email}, timedelta(days=7))
    return {
        'access_token': token,
        'refresh_token': refresh,
        'token_type': 'Bearer'
    }

@usuarios_router.post('/login-form')
async def login_form(oauth2_schema: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(email=oauth2_schema.username, senha=oauth2_schema.password, session=session)
    if not usuario:
        raise HTTPException(status_code=404, detail='Credencias inválidas')
    token = criar_token({'sub': oauth2_schema.username})
    refresh = criar_token({'sub': oauth2_schema.username}, timedelta(days=7))
    return {
        'access_token': token,
        'refresh_token': refresh,
        'token_type': 'Bearer'
    }


@usuarios_router.get('/perfil')
async def perfil(usuario: str = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    return {
        'message': f'usuario de id {usuario.id} encontrado',
        'usuario': usuario
    }

@usuarios_router.post('/refresh')
async def refresh(token: str, session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        usuario_email = dic_info.get('sub')
    except JWTError as erro:
        raise HTTPException(status_code=401, detail=f'acesso negado {erro}')
    usuario = session.query(Usuario).filter(Usuario.email==usuario_email).first()
    if not usuario:
        raise HTTPException(status_code = 404, detail='credencias inválidas')
    user_dict = {'sub': usuario_email}
    access_token = criar_token(user_dict)
    refresh_token = criar_token(user_dict, timedelta(days=7))
    return {
        'usuario_email': usuario_email,
        'access_token': access_token,
        'refresh_token': refresh_token
    }


