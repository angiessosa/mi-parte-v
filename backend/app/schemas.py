from pydantic import BaseModel
from datetime import datetime

class UsuarioCreate(BaseModel):
    tipoDocumento: str
    numeroDocumento: str
    nombres: str
    apellidos: str
    correoUsuario: str
    claveUsuario: str
    idRol: int


class UsuarioLogin(BaseModel):
    numeroDocumento: str
    claveUsuario: str


class TallerCreate(BaseModel):
    centroFormacion: str
    jornada: str
    coordinacion: str
    numFicha: str
    tema: str
    fechaYHora: datetime
    observaciones: str

class UsuarioTallerInsert(BaseModel):
    idUsuario: int
