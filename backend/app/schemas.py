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

class TallerSchema(BaseModel):
    fechaYHora: datetime
    numFicha: str
    tema: str
    observaciones: str = None  # Puede ser nulo

class TallerCreate(BaseModel):
    fechaYHora: datetime
    numFicha: str
    tema: str
    observaciones: str

class TallerResponse(TallerCreate):
    idTaller: int

class UsuarioTallerBase(BaseModel):
    idUsuario: int
    idTaller: int

class UsuarioTallerCreate(UsuarioTallerBase):
    pass

class UsuarioTaller(UsuarioTallerBase):
    id: int
