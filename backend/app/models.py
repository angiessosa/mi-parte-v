from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Time
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

class Rol(Base):
    __tablename__ = "rol"

    idRol = Column(Integer, primary_key=True, index=True)
    tipoRol = Column(String(20))

class Taller(Base):
    __tablename__ = "taller"

    idTaller =  Column(Integer, primary_key=True, index=True)
    centroFormacion = Column(String(100))
    jornada = Column(String(50))
    coordinacion =  Column(String(100))
    numFicha = Column(String(11))
    tema = Column(String(50))
    fechaYHora = Column(DateTime)
    observaciones = Column(String(1000))

class UsuarioTaller(Base):
    __tablename__ = "usuario_taller"

    id = Column(Integer, primary_key=True, index=True)
    idUsuario =  Column(Integer, ForeignKey("usuarios.idUsuario"))
    idTaller = Column(Integer, ForeignKey("taller.idTaller"))

class Horarios(Base):
    __tablename__ = "horarios"

    idHorario =  Column(Integer, primary_key=True, index=True)
    idUsuario = Column(Integer, ForeignKey("usuarios.idUsuario"))
    idTaller = Column(Integer, ForeignKey("taller.idTaller"))
    fecha = Column(Date)
    horaInicio = Column(Time)
    horaFin = Column(Time)
