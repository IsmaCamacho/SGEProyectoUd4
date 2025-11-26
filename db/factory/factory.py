from datetime import date, datetime, timedelta
import random
from faker import Faker
from sqlalchemy import func

from db.config import session, Session
from db.models.models import *
from log.log import *

fake = Faker("es_ES")
logger = Log()

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
        logger.log("INFO", "Estados iniciales creados correctamente")
    else:
        logger.log("WARNING", "Ya estan los estados iniciales creados")




#crear los clientes
def crearClientes():

    #comprobamos si hay clientes o no
    clientes = session.query(Cliente).all()

    if not clientes:
        for i in range(20):
            telefono = random.randint(111111111, 999999999)
            cliente = Cliente(nombre=fake.first_name(),
                              apellidos=fake.last_name(),
                              fecha_nacimiento=fake.date_of_birth(minimum_age=18), #asi no tengo que controlar que en las ventas sean mayor a 18
                              dni=fake.nif(),
                              email=fake.email(),
                              nacionalidad="España",
                              telefono=telefono,
                              direccion=fake.address())
            session.add(cliente)
        session.commit()
        logger.log("INFO", "Clientes iniciales creados correctamente")
    else:
        logger.log("WARNING", "Ya estan los clientes iniciales creados")





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
        fecha=ultimoDiaRegistrado[0] + timedelta(days=1)


    while fecha<=hoy:
        porcentaje = random.randint(-3, 3) / 100  ##si el porcentaje es 2 / 100 = 0.02
        precioHoy = precioInicial + (precioInicial * porcentaje)  # ejemplos eria 113002 + (113002 * 0.02)

        cotizacion = Cotizacion(fecha=fecha,
                                precio=precioHoy)
        session.add(cotizacion)

        fecha+=timedelta(days=1)

    session.commit()
    logger.log("INFO", "Ya estan todos los registros del oro creados y actualizados hasta dia de hoy")




#crear las ventas
def crearVenta():

    ##si quiere crear ventas tiene que haber creado antes los clientes, la cotizaacion y los estados
    clientes = session.query(Cliente).all()
    precios = session.query(Cotizacion).all()
    estados = session.query(Estado).all()

#comprobamos que ya se han generado todas las ventas
    totalVentas = session.query(Venta).count()

    if not clientes or not precios or not estados:
        print("Para crear las ventas debes crear primeros los clientes, los precios y los estados")
    elif totalVentas>=450:
        print("Ya están todas las ventas creadas")
    else:
        estadoAceptada=session.query(Estado).filter(Estado.nombre=="ACEPTADA").first()

    #creo las ventas con estado ACEPTADAS
        for i in range(400):
            cliente = random.choice(clientes)
            precio = random.choice(precios)
            venta = Venta(id_cliente=cliente.id,
                        id_precio=precio.id,
                        id_estado=estadoAceptada.id,
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
                          id_estado=estadoRechazado.id,
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
                        id_estado=estadoPendiente.id,
                        cantidad=random.randint(1,100),
                        fecha_venta=precio.fecha)
            session.add(venta)

        session.commit()


def generar1Venta():
    id = input("Dime el id del cliente que va a generar la venta")
    cant = input("Dime la cantidad de oro (en gramos): ")
    try:
        idCliente = int(id)
        cantidad = int(cant)
    except:
        logger.log("ERROR", "No introduce cantidad o el id del Cliente de tipo Int")
        return  # para que vuelva al menu

    #hay que comprobar si existe el cliente
    clienteExiste = session.query(Cliente).filter(Cliente.id==idCliente).first()

    if not clienteExiste:
        logger.log("ERROR", "Ese cliente no existe")
    else:
        #sacamos los datos de la fecha del precio del dia que genera la venta
        cotizacionHoy = session.query(Cotizacion).filter(Cotizacion.fecha == date.today()).first()

        #por defecto al entrar una nueva venta, debe ser en estado pendiente. COJO EL ID DEL ESTADO PENDIENTE
        estado = session.query(Estado).filter(func.upper(Estado.nombre) == "PENDIENTE").first()  # obliga a poner func delante de upperEstado.nombre

        ventaNueva = Venta(id_cliente=idCliente,
                            id_precio=cotizacionHoy.id,
                            id_estado=estado.id,
                            cantidad=cantidad,
                            fecha_venta=cotizacionHoy.fecha)
        session.add(ventaNueva)
        session.commit()
        logger.log("INFO", "Venta generada correctamente")



def cambiarEstadoVenta():

    id=input("Dime el id de la venta que quieres cambiar")
    try:
        idVenta=int(id)
    except:
        logger.log("ERROR", "No introduce el id de la Venta de tipo Int")
        return #para que vuelva al menu

    #saco la venta
    venta=session.query(Venta).filter(Venta.id==idVenta).first()

#si no existe la venta lo informo
    if not venta:
        logger.log("ERROR", "No existe esa venta")
    else: #si existe se pide el estado al que quiere cambiarla
        estadoNuevo=input("Dime el estado nuevo")
        estado=session.query(Estado).filter(func.upper(Estado.nombre) == estadoNuevo.upper()).first() #obliga a poner func delante de upperEstado.nombre

        #si no existe el estado
        if not estado:
            logger.log("ERROR", f"No existe ese Estado: ${estado.nombre}")
        elif venta.id_estado==estado.id: #si el que dice es el msimo que el que tiene
            logger.log("WARNING", f"No puede cambiar de estado porque esa Venta ${venta.id} ya tiene ese Estado")
        else: #sacamos la fecha y el precio del oro hoy y se cambia pero primero compruebo si ya se ha creado la cotizacion hoy
            cotizacionHoy=session.query(Cotizacion).filter(Cotizacion.fecha==date.today()).first()
            if not cotizacionHoy:
                logger.log("ERROR", "No hay cotización en el dia de hoy")
            else:
                venta.id_estado=estado.id
                venta.fecha_venta=cotizacionHoy.fecha
                venta.id_precio=cotizacionHoy.id

                session.commit()
                logger.log("INFO", f"Estado de la venta: ${venta.id} cambiado")
