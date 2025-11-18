from sqlalchemy import BigInteger, Column, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Cliente(Base):
    __tablename__ =  "cliente"
    __table_args__ = {"schema": "proyecto"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    apellidos = Column(String(200), nullable=False, unique=True)
    fecha_nacimiento = Column(Date, nullable=False, unique=True)
    dni = Column(String(20), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    nacionalidad = Column(String(100), nullable=False, unique=True)
    telefono = Column(BigInteger, nullable=False, unique=True)
    direccion = Column(String(200), nullable=False, unique=True)

    def __repr__(self):
        return (f"Cliente id={self.id}, Nombre: {self.nombre}, apellidos: {self.apellidos}, fecha nacimiento: {self.fecha_nacimiento} "
                f"dni: {self.dni}, email: {self.email}, nacionalidad: {self.nacionalidad}, telefono: {self.telefono}, direccion: {self.direccion}")


class Precio(Base):
    __tablename__ =  "precio"
    __table_args__ = {"schema": "proyecto"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False, unique=True)
    precio = Column(BigInteger, nullable=False, unique=True)

    def __repr__(self):
        return f"Precio id={self.id}, fecha: {self.fecha}, precio: {self.precio}"


class Venta(Base):
    __tablename__ =  "venta"
    __table_args__ = {"schema": "proyecto"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_cliente = Column(BigInteger, ForeignKey("proyecto.cliente.id"), nullable=False, unique=True)
    id_precio = Column(BigInteger, ForeignKey("proyecto.precio.id"), nullable=False, unique=True)
    id_estado = Column(BigInteger, ForeignKey("proyecto.estado.id"), nullable=False, unique=True)
    cantidad = Column(BigInteger, nullable=False, unique=True)
    fecha_venta = Column(Date, nullable=False, unique=True)



    def __repr__(self):
        return f"Venta id={self.id}, Cliente id: {self.id_cliente}, precio id: {self.precio}, estado id: {self.id_estado}, cantidad: {self.cantidad}, fecha venta: {self.fecha_venta}"


class Estado(Base):
    __tablename__ =  "estado"
    __table_args__ = {"schema": "proyecto"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"Estado id={self.id}, nombre: {self.nombre}"
