from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey, Enum,DateTime, Text, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship,joinedload
from datetime import datetime

import enum

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Region(Base):
    __tablename__ = 'region'

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String(200), nullable=False)

class Comuna(Base):
    __tablename__ = 'comuna'

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(BigInteger, ForeignKey("region.id"), nullable=False)

    comuna_region = relationship("Region")


class MedioContacto(enum.Enum):
    whatsapp = "whatsapp"
    telegram = "telegram"
    x = 'x'
    instagram = 'instagram'
    tiktok = 'tiktok'
    otra = "otra"


class Tipo(enum.Enum):
    perro = "perro"
    gato = "gato"

class Unidad(enum.Enum):
    a= "a"
    m = "m"

class Foto(Base):
    __tablename__ = 'foto'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    aviso_id = Column(BigInteger,ForeignKey('aviso_adopcion.id'), nullable=False)

    aviso = relationship("AvisoAdopcion", back_populates="fotos")


class ContactarPor(Base):
    __tablename__ = 'contactar_por'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(Enum(MedioContacto), nullable=False)
    identificador = Column(String(150), nullable=False)
    aviso_id = Column(BigInteger,ForeignKey('aviso_adopcion.id'), nullable=False)

    aviso = relationship("AvisoAdopcion", back_populates="contactos")


class AvisoAdopcion(Base):
    __tablename__ = 'aviso_adopcion'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    fecha_ingreso = Column(DateTime,nullable=False)
    comuna_id= Column(BigInteger,ForeignKey('comuna.id'), nullable=False)
    sector= Column(String(100), nullable=True)
    nombre= Column(String(100), nullable=False)
    email= Column(String(100), nullable=False)
    celular= Column(String(15), nullable=True)
    tipo = Column(Enum(Tipo), nullable=False)
    cantidad = Column(Integer, nullable=False)
    edad = Column(Integer, nullable=False)
    unidad_medida = Column(Enum(Unidad), nullable=False)
    fecha_entrega = Column(DateTime,nullable=False)
    descripcion = Column(Text,nullable=True)

    comuna = relationship("Comuna")
    fotos = relationship("Foto", back_populates="aviso", cascade="all, delete-orphan")
    contactos = relationship("ContactarPor", back_populates="aviso", cascade="all, delete-orphan")
    comentarios = relationship("Comentario", back_populates="aviso", cascade="all, delete-orphan")

class Comentario(Base):
    __tablename__ = 'comentario'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    aviso_id = Column(BigInteger, ForeignKey('aviso_adopcion.id'), nullable=False)
    nombre = Column(String(80), nullable=False)
    texto = Column(Text, nullable=False)
    fecha = Column(DateTime, nullable=False, server_default=func.now())

    aviso = relationship("AvisoAdopcion", back_populates="comentarios")




############################# Funciones

def obtenerRegiones():
    session = SessionLocal()
    try:
        regiones = session.query(Region).order_by(Region.nombre).all()
        return regiones
    finally:
        session.close()


def obtenerComunas():
    session = SessionLocal()
    try:
        comunas = session.query(Comuna).order_by(Comuna.nombre).all()
        return comunas
    finally:
        session.close()

def obtenerRedesSociales():
    redes = []
    for red in MedioContacto:
        redes.append({"id": red.value, "nombre": red.value.capitalize()})
    return redes

def crear_aviso(comuna,sector,nombre,email,celular,tipo,cantidad,edad,unidad,fecha_entrega,descripcion):
    session = SessionLocal()
    try:
        nuevo_aviso = AvisoAdopcion(
            fecha_ingreso=datetime.now(),
            comuna_id=comuna,
            sector=sector,
            nombre=nombre,
            email=email,
            celular=celular,
            tipo=tipo,
            cantidad=cantidad,
            edad=edad,
            unidad_medida=unidad,
            fecha_entrega=fecha_entrega,
            descripcion=descripcion
        )
        session.add(nuevo_aviso)
        session.commit()
        return nuevo_aviso.id
    finally:
        session.close()
    

def crear_foto(ruta_archivo, nombre_archivo, aviso_id):

    session = SessionLocal()
    try:
        nueva_foto = Foto(
            ruta_archivo=ruta_archivo,
            nombre_archivo=nombre_archivo,
            aviso_id=aviso_id
        )
        session.add(nueva_foto)
        session.commit()
        return nueva_foto.id
    finally:
        session.close()

def crear_contactar_por(nombre, identificador, aviso_id):
    session = SessionLocal()
    try:
        nuevo_contacto = ContactarPor(
            nombre=nombre,
            identificador=identificador,
            aviso_id=aviso_id
        )
        session.add(nuevo_contacto)
        session.commit()
        return nuevo_contacto.id 
    finally:
        session.close()

def crear_comentario(aviso_id, nombre, texto):
    session = SessionLocal()
    try:
        nuevo_comentario = Comentario(
            aviso_id=aviso_id,
            nombre=nombre,
            texto=texto,
            fecha=datetime.now()
        )
        session.add(nuevo_comentario)
        session.commit()
        return nuevo_comentario.id
    finally:
        session.close()


def obtenerUltimosAvisos(limit=5):
    session = SessionLocal()
    try:
        avisos = session.query(AvisoAdopcion)\
            .options(
                joinedload(AvisoAdopcion.comuna),
                joinedload(AvisoAdopcion.fotos),
                joinedload(AvisoAdopcion.contactos)
            )\
            .order_by(AvisoAdopcion.fecha_ingreso.desc())\
            .limit(limit)\
            .all()
        return avisos
    finally:
        session.close()

def obtenerAvisosPaginados(pagina=1, por_pagina=5):
    session = SessionLocal()
    try:
        offset = (pagina - 1) * por_pagina
        
        avisos = session.query(AvisoAdopcion)\
            .options(
                joinedload(AvisoAdopcion.comuna).joinedload(Comuna.comuna_region),
                joinedload(AvisoAdopcion.fotos),
                joinedload(AvisoAdopcion.contactos)
            )\
            .order_by(AvisoAdopcion.fecha_ingreso.desc())\
            .offset(offset)\
            .limit(por_pagina)\
            .all()
        
        total_avisos = session.query(AvisoAdopcion).count()
        total_paginas = (total_avisos + por_pagina - 1) // por_pagina
        
        return {
            'avisos': avisos,
            'pagina_actual': pagina,
            'total_paginas': total_paginas,
            'total_avisos': total_avisos
        }
    finally:
        session.close()



def obtenerAvisosPorDia():
    session = SessionLocal()
    try:
        rows = (
            session.query(
                func.date(AvisoAdopcion.fecha_entrega).label("fecha"),
                func.count(AvisoAdopcion.id).label("cantidad")
            )
            .group_by(func.date(AvisoAdopcion.fecha_entrega))
            .order_by(func.date(AvisoAdopcion.fecha_entrega))
            .all()
        )
        data = []
        for fecha, cantidad in rows:
            fecha_str = fecha.strftime("%Y-%m-%d") if hasattr(fecha, "strftime") else str(fecha)
            data.append({"fecha": fecha_str, "cantidad": int(cantidad)})

        return data
    finally:
        session.close()

def obtenerAvisosPorTipo():

    session = SessionLocal()
    try:
        rows = (
            session.query(AvisoAdopcion.tipo, func.count(AvisoAdopcion.id))
            .group_by(AvisoAdopcion.tipo)
            .all()
        )

        conteos = {}
        for tipo, cantidad in rows:
            key = tipo.value if hasattr(tipo, "value") else str(tipo)
            conteos[key] = int(cantidad)

        resultado = []
        for tipo in Tipo: 
            resultado.append({
                "tipo": tipo.value,
                "cantidad": conteos.get(tipo.value, 0)
            })

        return resultado
    finally:
        session.close()


def obtenerAvisosPorMesTipo():

    session = SessionLocal()
    try:
        q = (
            session.query(
                func.date_format(AvisoAdopcion.fecha_entrega, '%Y-%m').label('mes'),
                AvisoAdopcion.tipo.label('tipo'),
                func.count(AvisoAdopcion.id).label('cantidad')
            )
            .group_by('mes', AvisoAdopcion.tipo)
            .order_by('mes')
        )

        rows = q.all() 

        pivot = {}
        for mes, tipo, cantidad in rows:
            tipo_str = tipo.value if hasattr(tipo, "value") else str(tipo)
            if mes not in pivot:
                pivot[mes] = {'perro': 0, 'gato': 0}
            pivot[mes][tipo_str] = int(cantidad)

        resultado = []
        for mes in sorted(pivot.keys()):
            resultado.append({
                'mes': mes,
                'perro': pivot[mes].get('perro', 0),
                'gato': pivot[mes].get('gato', 0)
            })

        return resultado

    finally:
        session.close()

def obtenerComentariosPorAviso(aviso_id):
    session = SessionLocal()
    try:
        comentarios = (
            session.query(Comentario)
            .filter(Comentario.aviso_id == aviso_id)
            .order_by(Comentario.fecha.asc())
            .all()
        )
        return comentarios
    finally:
        session.close()

