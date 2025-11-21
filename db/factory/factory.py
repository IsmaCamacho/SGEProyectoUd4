from datetime import date, datetime, timedelta
import random
from faker import Faker
from db.config import session
from db.models.models import *

fake = Faker("es_ES")

#crear los clientes
def crearClientes():

    telefono = random.randint(111111111, 999999999)
    for i in range(20):
        cliente = Cliente(nombre=fake.first_name(),
                          apellidos=fake.last_name(),
                          fecha_nacimiento=fake.date_of_birth(minimum_age=18),
                          dni=fake.nif(),
                          email=fake.email(),
                          nacionalidad="España",
                          telefono=telefono,
                          direccion=fake.address())
        session.add(cliente)
    session.commit()

def crearPreciosOro():

    fechaInicio = date(2025, 1, 1)
    hoy = date.today() #para que solo coja el dia que si pongo datetime.now coge tambien la hora

    precioInicial = 113002

    fecha=fechaInicio
    while fecha<=hoy:
        porcentaje = random.randint(-3,3)/100 ##si el porcentaje es 2 / 100 = 0.02
        precioHoy=precioInicial + (precioInicial * porcentaje) #ejemplos eria 113002 + (113002 * 0.02)

        cotizacion = Cotizacion(fecha=fecha,
                                precio=precioHoy)
        session.add(cotizacion)
        #PREGUNTAR A FRAN ESTO
        fecha += timedelta(days=1)


    session.commit()

#crear las ventas
def crearVenta():

    clientes = session.query(Cliente).all()
    precios = session.query(Cotizacion).all()


    for i in range(400):
        c = random.choice(clientes)
        p = random.choice(precios)
        venta = Venta(id_cliente=c.id,
                    id_precio=p.id,
                    id_estado=2,
                    cantidad=random.randint(1,100),
                    fecha_venta=p.fecha)
        session.add(venta)

    for i in range(30):
        c = random.choice(clientes)
        p = random.choice(precios)
        venta = Venta(id_cliente=c.id,
                      id_precio=p.id,
                      id_estado=3,
                      cantidad=random.randint(1, 100),
                      fecha_venta=p.fecha)
        session.add(venta)

    for i in range(20):
        c = random.choice(clientes)
        p = random.choice(precios)
        venta = Venta(id_cliente=c.id,
                    id_precio=p.id,
                    id_estado=1,
                    cantidad=random.randint(1,100),
                    fecha_venta=p.fecha)
        session.add(venta)

    session.commit()

def ejecutar_factory():
    crearClientes()
    crearPreciosOro()
    crearVenta()

if __name__ == "__main__":
    ejecutar_factory()
