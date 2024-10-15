from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    idUsuario = Column(Integer, primary_key=True, index=True)
    tipoDocumento = Column(String(50))
    numeroDocumento = Column(String(15), unique=True, index=True)
    nombres = Column(String(100))
    apellidos = Column(String(100))
    correoUsuario = Column(String(250))
    claveUsuario = Column(String(60))
    idRol = Column(Integer)
    estado = Column(String, default="pendiente")  # Estado por defecto "pendiente"
    talleres = relationship('UsuarioTaller', back_populates='usuario')

class Rol(Base):
    __tablename__ = "rol"

    idRol = Column(Integer, primary_key=True, index=True)
    tipoRol = Column(String(20))

class Taller(Base):
    __tablename__ = "taller"
    
    idTaller = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fechaYHora = Column(DateTime, nullable=False)
    numFicha = Column(String(11), index=True)
    tema = Column(String(50), index=True)
    observaciones = Column(String(1000), nullable=True)
    usuarios = relationship('UsuarioTaller', back_populates='taller')

class UsuarioTaller(Base):
    __tablename__ = 'usuario_taller'
    
    id = Column(Integer, primary_key=True, index=True)
    idUsuario = Column(Integer, ForeignKey('usuarios.idUsuario'))
    idTaller = Column(Integer, ForeignKey('taller.idTaller'))

    usuario = relationship('Usuario', back_populates='talleres')
    taller = relationship('Taller', back_populates='usuarios')