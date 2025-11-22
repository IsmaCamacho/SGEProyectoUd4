from sqlalchemy import BigInteger, Column, String, Date, ForeignKey
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

    def __repr__(self):
        return (f"Cliente id={self.id}, Nombre: {self.nombre}, apellidos: {self.apellidos}, fecha nacimiento: {self.fecha_nacimiento} "
                f"dni: {self.dni}, email: {self.email}, nacionalidad: {self.nacionalidad}, telefono: {self.telefono}, direccion: {self.direccion}")


class Cotizacion(Base):
    __tablename__ =  "cotizacion"
    __table_args__ = {"schema": "proyecto"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False, unique=True)
    precio = Column(BigInteger, nullable=False)

    def __repr__(self):
        return f"Precio id={self.id}, fecha: {self.fecha}, precio: {self.precio}"


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
