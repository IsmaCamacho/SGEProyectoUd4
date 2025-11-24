from datetime import date, datetime, timedelta
import random
from faker import Faker
from db.config import session
from db.models.models import *

fake = Faker("es_ES")

def crearEstados():

    #comprobamos si estan creados ya los estados
    estados=session.query(Estado).all()
    if not estados:
        estados=["PENDIENTE", "ACEPTADA", "RECHAZADA"]  #creo una lista con los tres estados
    #recorro la lista y compruebo si ya existen
        for i in estados:
            existe=session.query(Estado).filter(Estado.nombre==i).first()
            #si no existe lo añade
            if not existe:
                estado=Estado(Estado.nombre==i)
                session.add(estado)

        session.commit()
        print("Estados creados correctamente")
    else:
        print("Ya estan todos los estados correctamente")


#crear los clientes
def crearClientes():

    #comprobamos si hay clientes o no
    clientes = session.query(Cliente).all()

    if not clientes:
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
        print("Clientes creados correctamente")
    else:
        print("Ya estan todos los clientes creados")


def crearPreciosOro():

    precioInicial = 113002
    fechaInicio = date(2025, 1, 1)
    hoy = date.today() #para que solo coja el dia que si pongo datetime.now coge tambien la hora

##saco el ultimo dia de registro
    ultimoDiaRegistrado = session.query(Cotizacion.fecha).order_by(Cotizacion.fecha.desc()).first()

#si todavia no hay registros la fecha es la fecha de inicio (1 de enero de 2025)
    if not ultimoDiaRegistrado:
        fecha = fechaInicio
    else: #sino pues la fecha es la del ultimo dia registrado mas un dia
        fecha=ultimoDiaRegistrado + timedelta(days=1)


    while fecha<=hoy:
        porcentaje = random.randint(-3, 3) / 100  ##si el porcentaje es 2 / 100 = 0.02
        precioHoy = precioInicial + (precioInicial * porcentaje)  # ejemplos eria 113002 + (113002 * 0.02)

        cotizacion = Cotizacion(fecha=fecha,
                                precio=precioHoy)
        session.add(cotizacion)

        fecha+=timedelta(days=1)

    session.commit()



#crear las ventas
def crearVenta():

    ##si quiere crear ventas tiene que haber creado antes los clientes, la cotizaacion y los estados
    clientes = session.query(Cliente).all()
    precios = session.query(Cotizacion).all()
    estados = session.query(Estado).all()

    if not clientes or not precios or not estados:
        print("Para crear las ventas debes crear primeros los clientes, los precios y los estados")
    else:
        estadoAceptada=session.query(Estado).filter(Estado.nombre=="ACEPTADA").first()

    #creo las ventas con estado ACEPTADAS
        for i in range(400):
            cliente = random.choice(clientes)
            precio = random.choice(precios)
            venta = Venta(id_cliente=cliente.id,
                        id_precio=precio.id,
                        id_estado=estadoAceptada,
                        cantidad=random.randint(1,100),
                        fecha_venta=precio.fecha)
            session.add(venta)


    #creo las ventas con estado rechazado
        estadoRechazado = session.query(Estado).filter(Estado.nombre == "RECHAZADA").first()
        for i in range(30):
            cliente = random.choice(clientes)
            precio = random.choice(precios)
            venta = Venta(id_cliente=cliente.id,
                          id_precio=precio.id,
                          id_estado=estadoRechazado,
                          cantidad=random.randint(1, 100),
                          fecha_venta=precio.fecha)
            session.add(venta)


    #creo las ventas con estado pendiente
        estadoPendiente = session.query(Estado).filter(Estado.nombre == "PENDIENTE").first()
        for i in range(20):
            cliente = random.choice(clientes)
            precio = random.choice(precios)
            venta = Venta(id_cliente=cliente.id,
                        id_precio=precio.id,
                        id_estado=estadoPendiente,
                        cantidad=random.randint(1,100),
                        fecha_venta=precio.fecha)
            session.add(venta)

        session.commit()