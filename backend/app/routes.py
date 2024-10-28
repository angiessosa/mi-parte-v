from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Usuario, Taller
from app.schemas import UsuarioCreate, UsuarioLogin, AreaEncargada, CoordinacionInstru, FechaSeleccionada, RecuperarContrasena
from datetime import datetime

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



#RECUPERAR CONTRASEÑA






"""
# Crear taller
@router.post("/taller")
def crear_taller(taller: TallerCreate, db: Session = Depends(get_db), idUsuario = int):
    try:
        # 1. Crear una nueva instancia de la tabla Taller
        nuevo_taller = Taller(
            centroFormacion=taller.centroFormacion,
            jornada=taller.jornada,
            coordinacion=taller.coordinacion,
            numFicha=taller.numFicha,
            tema=taller.tema,
            fechaYHora=taller.fechaYHora,
            observaciones=taller.observaciones
        )

        # 2. Guardar el taller en la base de datos
        db.add(nuevo_taller)
        db.commit()
        db.refresh(nuevo_taller)  # Refrescar el objeto para obtener su idTaller generado

        # 3. Asignar el taller al usuario en la tabla intermedia usuario_taller
        usuario_taller = UsuarioTaller(
            idUsuario=idUsuario,  # Usar el idUsuario que recibes como argumento
            idTaller=nuevo_taller.idTaller  # Usamos el idTaller recién creado
        )

        # 4. Guardar la relación usuario_taller
        db.add(usuario_taller)
        db.commit()

        # 5. Retornar una respuesta exitosa con los datos creados
        return {
            "message": "Taller creado con éxito",
            "taller": {
                "idTaller": nuevo_taller.idTaller,
                "centroFormacion": nuevo_taller.centroFormacion,
                "tema": nuevo_taller.tema,
                "fechaYHora": nuevo_taller.fechaYHora
            }
        }

    except Exception as e:
        db.rollback()  # Si ocurre algún error, deshacer los cambios
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
"""


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