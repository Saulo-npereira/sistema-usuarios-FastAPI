from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///banco.db')

Base = declarative_base()


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String)
    email = Column('email', String, unique=True)
    senha = Column('senha', String)

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

