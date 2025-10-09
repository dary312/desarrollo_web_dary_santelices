from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey, Enum,DateTime, Text
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

def obtener_avisos_paginados(pagina=1, por_pagina=5):
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