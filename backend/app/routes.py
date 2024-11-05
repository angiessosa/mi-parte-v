from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Usuario, Taller, Coordinacion, Ficha, Tematicas, UsuarioTaller
from app.schemas import UsuarioCreate, UsuarioLogin, AreaEncargada, CoordinacionInstru, FechaSeleccionada, CoordinacionResponse, FichasResponse, TemasResponse, ProfesionalResponse, TallerCreate, UsuarioTallerCreate
from datetime import datetime
from typing import List


from sqlalchemy import func

import bcrypt

router = APIRouter()


# Registro de usuarios
@router.post("/registro")
def registrer_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    # Mostrar los datos recibidos
    print(f"Datos recibidos: {user}")

    # Verificar si el usuario ya existe
    user_existence = db.query(Usuario).filter(Usuario.numeroDocumento == user.numeroDocumento).first()
    if user_existence:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    # Encriptar la contraseña
    hashed_password = bcrypt.hashpw(user.claveUsuario.encode('utf-8'), bcrypt.gensalt())

    # Crear nuevo usuario
    nuevo_usuario = Usuario(
        tipoDocumento=user.tipoDocumento,
        numeroDocumento=user.numeroDocumento,
        nombres=user.nombres,
        apellidos=user.apellidos,
        correoUsuario=user.correoUsuario,
        claveUsuario=hashed_password.decode('utf-8'),
        idRol=user.idRol,
        estado="pendiente"  # Estado inicial como pendiente
    )

    # Guardar el nuevo usuario en la base de datos
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {"message": "Usuario registrado exitosamente. Solicitud pendiente de aprobación"}



#usuarios pendientes
@router.get("/usuarios/pendientes")
def get_usuarios_pendientes(db: Session = Depends(get_db)):
    usuarios_pendientes = db.query(Usuario).filter(Usuario.estado == "pendiente").all()
    return usuarios_pendientes


@router.put("/usuarios/{idUsuario}/estado")
def update_estado_usuario(idUsuario: int, estado: str, db: Session = Depends(get_db)):

    # Buscar el usuario por su ID
    usuario = db.query(Usuario).filter(Usuario.idUsuario == idUsuario).first()
    
    # Si el usuario no existe, lanzar un error 404
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar el estado del usuario (puede ser "aprobado" o "rechazado")
    usuario.estado = estado
    db.commit()  # Guardar los cambios en la base de datos
    
    # Devolver un mensaje de éxito
    return {"message": f"Estado del usuario actualizado a {estado}"}




#login
@router.post("/login")
def login(user: UsuarioLogin, db: Session = Depends(get_db)):

    #Verificar si el usuario existe
    usuario = db.query(Usuario).filter(Usuario.numeroDocumento == user.numeroDocumento).first()

    #validar si el usuario existe
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    #validar si el usuario es aprobado
    if usuario.estado != "aprobado":
        raise HTTPException(status_code=403, detail="Usuario no aprobado")
    
    #validar la contraseña
    if not bcrypt.checkpw(user.claveUsuario.encode('utf-8'), usuario.claveUsuario.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    return {"message": "Login exitoso", "rol": usuario.idRol, "nombres": usuario.nombres}

#Filtro de profesionales por area
@router.post("/areaSelecionada")
def seleccion_area(area: AreaEncargada, db: Session = Depends(get_db)):
    print(f"Área encargada es: {area.areaEncargada}")
    usuarios_en_area = db.query(Usuario).filter(Usuario.areaEncargada == area.areaEncargada).all()
    return usuarios_en_area

#Filtros de instructores por coordinación 
@router.post("/coordinacionselecionada")
def seleccion_coordinacion(coordinacio: CoordinacionInstru, db: Session = Depends(get_db)):
    print(f"Coordinacion es: {coordinacio.coordinacionInstru}")
    usuarios_en_coordi = db.query(Usuario).filter(Usuario.coordinacionInstru == coordinacio.coordinacionInstru).all()
    return usuarios_en_coordi

@router.post("/fechaSeleccionada")
def seleccion_fecha(fecha: FechaSeleccionada, db: Session = Depends(get_db)):
    print(f"Fecha seleccionada es: {fecha.dia}")
    
    try:
        fecha_formateada = datetime.strptime(fecha.dia, "%Y-%m-%d").date()  # Asegúrate de que el formato es correcto
        talleres_en_fecha = db.query(Taller).filter(func.date(Taller.fechaYHora) == fecha_formateada).all()
        
        if not talleres_en_fecha:
            return {"message": "No hay talleres programados para esta fecha."}

        return {"message": "Talleres encontrados", "data": talleres_en_fecha}

    except ValueError:
        return {"error": "Formato de fecha inválido. Asegúrate de enviar la fecha en formato yyyy-MM-dd"}



#Mostrar talleres hoy
@router.get("/buscarTalleres")
def get_all_talleres(db: Session = Depends(get_db)):
    return db.query(Taller).all()

@router.get("/buscarTalleres/hoy")
def get_talleres_hoy(db: Session = Depends(get_db)):
    # Obtener la fecha actual
    today = datetime.now().date()
    
    # Consulta para obtener talleres cuya fecha es hoy
    talleres_hoy = db.query(Taller).filter(Taller.fechaYHora == today).all()
    
    return talleres_hoy


#Filtros para agendar taller

@router.get("/getCoordinaciones", response_model=List[CoordinacionResponse])
def get_coordinaciones(db: Session = Depends(get_db)):
    coordinaciones = db.query(Coordinacion).all()
    if not coordinaciones:
        raise HTTPException(status_code=404, detail="No se encontraron coordinaciones")
    return coordinaciones

@router.get("/getNumFicha", response_model=List[FichasResponse])
def get_numfichas(db: Session = Depends(get_db)):
    try:
        numfichas = db.query(Ficha).all()
        if not numfichas:
            raise HTTPException(status_code=404, detail="No se encontraron fichas")
        return numfichas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Devuelve el error al cliente

@router.get("/getTematica", response_model=List[TemasResponse])
def get_coordinaciones(db: Session = Depends(get_db)):
    tematicas = db.query(Tematicas).all()
    if not tematicas:
        raise HTTPException(status_code=404, detail="No se encontraron tematicas")
    return tematicas

@router.get("/getProfesionales", response_model=List[ProfesionalResponse])
def get_profesionales(db: Session = Depends(get_db)):
    try:
        get_profesionales = db.query(Usuario).filter(Usuario.idRol == 3).all()
        if not get_profesionales:
            raise HTTPException(status_code=404, detail="No se encontraron profesionales")
        return get_profesionales
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Devuelve el error al cliente





#CREAR TALLERRRRRRRRRRRRRR T_T ;-;
@router.post("/Creartaller", response_model=TallerCreate)
def create_taller(taller: TallerCreate, db: Session = Depends(get_db)):
    try:
        # Crear el taller
        nuevo_taller = Taller(
            centroFormacion=taller.centroFormacion,
            jornada=taller.jornada,
            coordinacion=taller.coordinacion,
            numFicha=taller.numFicha,
            tema=taller.tema,  # No validar contra tematicas
            fechaYHora=datetime.fromisoformat(taller.fechaYHora),
            observaciones=taller.observaciones
        )
        db.add(nuevo_taller)
        db.commit()
        return nuevo_taller
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=str(e))
  

@router.post("/usuario_taller")
def assign_profesional_to_taller(idTaller: int, idUsuario: int, db: Session = Depends(get_db)):
    try:
        # Crear la relación en usuario_taller
        usuario_taller = UsuarioTaller(idUsuario=idUsuario, idTaller=idTaller)  # Asegúrate de que esto es correcto
        db.add(usuario_taller)
        db.commit()
        return {"message": "Profesional asignado al taller correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al asignar profesional: {str(e)}")








"""crear profesionales de bienestar
@router.post("/profesionales")
async def crear_profesional(profesional: ProfesionalCreate, db: Session = Depends(get_db)):
    # Verificar si ya existe un profesional con el mismo número de documento
    existing_profesional = db.query(Usuario).filter(Usuario.numeroDocumento == profesional.numeroDocumento).first()
    
    if existing_profesional:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese número de documento")
    
    # Encriptar la contraseña
    hashed_password = bcrypt.hashpw(profesional.claveUsuario.encode('utf-8'), bcrypt.gensalt())
    
    try:
        nuevo_profesional = Usuario(
            tipoDocumento=profesional.tipoDocumento,
            numeroDocumento=profesional.numeroDocumento,
            nombres=profesional.nombres,
            apellidos=profesional.apellidos,
            correoUsuario=profesional.correoUsuario,
            claveUsuario=hashed_password.decode('utf-8'),
            idRol=3,  # Asignando el rol
            area_encargada=profesional.areaEncargada,
        )
        db.add(nuevo_profesional)
        db.commit()
        db.refresh(nuevo_profesional)
        return {"mensaje": "Profesional registrado exitosamente", "profesional": nuevo_profesional}
    except Exception as e:
        db.rollback()  # Revertir cambios si ocurre un error
        raise HTTPException(status_code=500, detail=str(e))
"""
