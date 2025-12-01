from time import sleep

from sqlalchemy import BigInteger, Column, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Cliente(Base):
    __tablename__ =  "cliente"
    __table_args__ = {"schema": "proyecto"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(200), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    dni = Column(String(10), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    nacionalidad = Column(String(100), nullable=False)
    telefono = Column(BigInteger, nullable=False, unique=True)
    direccion = Column(String(200), nullable=False)
    activo = Column(Boolean, nullable=False)

    def __repr__(self):
        return (f"Cliente id={self.id}, Nombre: {self.nombre}, apellidos: {self.apellidos}, fecha nacimiento: {self.fecha_nacimiento} "
                f"dni: {self.dni}, email: {self.email}, nacionalidad: {self.nacionalidad}, telefono: {self.telefono}, direccion: {self.direccion}")

    def __str__(self):
        return f"CLIENTE ID:{self.id}, Nombre: {self.nombre} {self.apellidos}"


class Cotizacion(Base):
    __tablename__ =  "cotizacion"
    __table_args__ = {"schema": "proyecto"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False, unique=True)
    precio = Column(BigInteger, nullable=False)

    def __repr__(self):
        return f"Precio id={self.id}, fecha: {self.fecha}, precio: {self.precio}"

    def __str__(self):
        return f"PRECIO ID:{self.id}, Fecha: ${self.fecha}, Precio: {self.precio}"


class Venta(Base):
    __tablename__ =  "venta"
    __table_args__ = {"schema": "proyecto"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_cliente = Column(BigInteger, ForeignKey("proyecto.cliente.id"), nullable=False)
    id_precio = Column(BigInteger, ForeignKey("proyecto.cotizacion.id"), nullable=False)
    id_estado = Column(BigInteger, ForeignKey("proyecto.estado.id"), nullable=False)
    cantidad = Column(BigInteger, nullable=False)
    fecha_venta = Column(Date, nullable=False)

    def __repr__(self):
        return f"Venta id={self.id}, Cliente id: {self.id_cliente}, precio id: {self.id_precio}, estado id: {self.id_estado}, cantidad: {self.cantidad}, fecha venta: {self.fecha_venta}"


class Estado(Base):
    __tablename__ =  "estado"
    __table_args__ = {"schema": "proyecto"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"Estado id={self.id}, nombre: {self.nombre}"


#A PARTIR DE AQUI EXAMEN!

class TipoArmario(Base):
    __tablename__ = "tipo_armario"
    __table_args__ = {"schema": "proyecto"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    descripcion = Column(String(200), nullable=False, unique=True)

    def __repr__(self):
        return f"Tipo Armario id={self.id}, descripcion: {self.descripcion}"


class MovimientosArmarios(Base):
    __tablename__ = "movimientos_armarios"
    __table_args__ = {"schema": "proyecto"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cantidad = Column(BigInteger, nullable=False)
    operacion = Column(String(200), nullable=False, unique=True)
    fecha= Column(Date, nullable=False)
    id_cliente = Column(BigInteger, ForeignKey("proyecto.cliente.id"), nullable=False)

    def __repr__(self):
        return (f"Movimientos Armario id={self.id}, cantidad: {self.cantidad}, operacion: {self.operacion}, "
                f"fecha: {self.fecha}, id_cliente {self.id_cliente}")

class Armarios(Base):
    __tablename__ = "armarios"
    __table_args__ = {"schema": "proyecto"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_cliente = Column(BigInteger, ForeignKey("proyecto.cliente.id"), nullable=False)
    id_tipo_armario = Column(BigInteger, ForeignKey("proyecto.tipo_armario.id"), nullable=False)
    gramos = Column(BigInteger, nullable=False)

    def __repr__(self):
        return (f"Armarios id={self.id}, id cliente: {self.id_cliente}, id tipo armario: {self.id_tipo_armario}, "
                f"cantidad gramos: {self.gramos}")