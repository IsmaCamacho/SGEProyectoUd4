from datetime import date, datetime, timedelta
import random
from math import trunc

from faker import Faker
from sqlalchemy import func, extract

from db.config import session, Session
from db.models.models import *
from log.log import *

fake = Faker("es_ES")
logger = Log()

def crearEstados():

    #comprobamos si estan creados ya los estados
    estados=session.query(Estado).count()
    if estados==0:
        estados=["PENDIENTE", "ACEPTADA", "RECHAZADA"]  #creo una lista con los tres estados
    #recorro la lista y compruebo si ya existen
        for nombre in estados:
            existe=session.query(Estado).filter(Estado.nombre==nombre).first()
            #si no existe lo añade
            if not existe:
                estado=Estado(nombre=nombre)
                session.add(estado)

        session.commit()
        logger.log("INFO", "Creación Estados. Estados iniciales creados correctamente")
    else:
        logger.log("WARNING", "Creación Estados. Ya estan los estados iniciales creados")




#crear los clientes
def crearClientes():

    #comprobamos si hay clientes o no
    clientes = session.query(Cliente).count()

    if clientes==0:
        for i in range(20):
            telefono = random.randint(111111111, 999999999)
            cliente = Cliente(nombre=fake.first_name(),
                              apellidos=fake.last_name(),
                              fecha_nacimiento=fake.date_of_birth(minimum_age=18), #asi no tengo que controlar que en las ventas sean mayor a 18
                              dni=fake.unique.nif(), #con el unique por si crea mas de un personaje con el dni y peta el programa como me ha pasado, asi no lo repite
                              email=fake.email(),
                              nacionalidad="España",
                              telefono=telefono,
                              direccion=fake.address(),
                              activo=True)
            session.add(cliente)
        session.commit()
        logger.log("INFO", "Creación Clientes. Clientes iniciales creados correctamente")
    else:
        logger.log("WARNING", "Creación Clientes. Ya estan los clientes iniciales creados")





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
    logger.log("INFO", "Creación Cotización. Ya estan todos los registros del oro creados y actualizados hasta dia de hoy")




#crear las ventas
def crearVenta():

    #comprobamos si ya hay ventas o no para crearlas
    totalVentas=session.query(Venta).count()
    if totalVentas >= 400:
        logger.log("WARNING", "Creación Ventas. Ya estan todas las Ventas iniciales creadas")
        return

    ##si quiere crear ventas tiene que haber creado antes los clientes, la cotizaacion y los estados
    clientes = session.query(Cliente).all()  #los clientes mayores de edad unica forma y que esten activos
    precios = session.query(Cotizacion).all()
    estados = session.query(Estado).all()

    if not clientes or not precios or not estados:
        logger.log("ERROR", "Creación Ventas. No se pueden crear ventas: faltan clientes, precios o estados")
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
        logger.log("INFO", "Creación Ventas. Ventas iniciales creadas correctamente (450 ventas generadas)")




def generar1Venta():

    todosClientes = session.query(Cliente).all()
    for cliente in todosClientes:
        print(cliente)

    id = input("\nDime el id del cliente que va a generar la venta")
    cant = input("Dime la cantidad de oro (en gramos): ")
    try:
        idCliente = int(id)
        cantidad = int(cant)
    except ValueError:
        logger.log("ERROR", "Generar venta. No introduce cantidad o el id del Cliente de tipo Int")
        return  # para que vuelva al menu

    #hay que comprobar si existe el cliente y si esta activo      para la comprobacion de si es mayor de edad lo he buscado y es lo mas facil e intuitivo encontrado, extraer el año de la fehca del cliente y del dia de hoy
    clienteExiste = session.query(Cliente).filter(Cliente.id==idCliente).filter(Cliente.activo==True).filter((extract('year', func.now()) - extract('year', Cliente.fecha_nacimiento))>=18).first()

    if not clienteExiste:
        logger.log("ERROR", "Generar venta. Ese cliente no existe, es menor de edad o esta inactivo")
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
        logger.log("INFO", "Generar venta. Venta generada correctamente")




def cambiarEstadoVenta():

    id=input("Dime el id de la venta que quieres cambiar")
    try:
        idVenta=int(id)
    except ValueError:
        logger.log("ERROR", "Cambiar Estado. No introduce el id de la Venta de tipo Int")
        return #para que vuelva al menu

    #saco la venta
    venta=session.query(Venta).filter(Venta.id==idVenta).first()

#si no existe la venta lo informo
    if not venta:
        logger.log("ERROR", "Cambiar Estado. No existe esa venta")
    else: #si existe se pide el estado al que quiere cambiarla
        estadoNuevo=input("Dime el estado nuevo")
        estado=session.query(Estado).filter(func.upper(Estado.nombre) == estadoNuevo.upper()).first() #obliga a poner func delante de upperEstado.nombre

        #si no existe el estado
        if not estado:
            logger.log("ERROR", f"Cambiar Estado. No existe ese Estado: {estadoNuevo}")
        elif venta.id_estado==estado.id: #si el que dice es el msimo que el que tiene
            logger.log("WARNING", f"Cambiar Estado. No puede cambiar de estado porque esa Venta {venta.id} ya tiene ese Estado")
        else: #sacamos la fecha y el precio del oro hoy y se cambia pero primero compruebo si ya se ha creado la cotizacion hoy
            cotizacionHoy=session.query(Cotizacion).filter(Cotizacion.fecha==date.today()).first()
            if not cotizacionHoy:
                logger.log("ERROR", "Cambiar Estado. No hay cotización en el dia de hoy")
            else:
                venta.id_estado=estado.id
                venta.fecha_venta=cotizacionHoy.fecha
                venta.id_precio=cotizacionHoy.id

                session.commit()
                logger.log("INFO", f"Cambiar Estado. Estado de la venta: {venta.id} cambiado")



def darBajaCliente():
    id = input("Dime el id del cliente que quieres dar de baja")
    try:
        idCliente = int(id)
    except ValueError:
        logger.log("ERROR", "Baja Cliente. No introduce el id del Cliente de tipo Int")
        return  # para que vuelva al menu

#comprobamos si existe el cliente
    clienteExiste = session.query(Cliente).filter(Cliente.id==idCliente).first()

    if not clienteExiste:
        logger.log("ERROR", "Baja Cliente. No existe ese cliente")
    elif clienteExiste.activo==False:
        logger.log("WARNING", "Baja Cliente. Cliente ya estaba dado de baja")
    else:

        clienteExiste.activo=False
        session.commit()
        logger.log("INFO", "Baja Cliente. Cliente dado de baja correctamente")





def darAltaClienteExistente():
    id = input("Dime el id del cliente que quieres dar de alta")
    try:
        idCliente = int(id)
    except ValueError:
        logger.log("ERROR", "Alta Cliente. No introduce el id del Cliente de tipo Int")
        return  # para que vuelva al menu

    # comprobamos si existe el cliente
    clienteExiste = session.query(Cliente).filter(Cliente.id == idCliente).first()

    if not clienteExiste:
        logger.log("ERROR", "Alta Cliente. No existe ese cliente")
    elif clienteExiste.activo == True:
        logger.log("WARNING", "Alta Cliente. Cliente ya estaba dado de alta")
    else:

        clienteExiste.activo = True
        session.commit()
        logger.log("INFO", "Alta Cliente. Cliente dado de alta correctamente")



#A PARTIR DE AQUI EXAMEN!
def cargarDatosPruebaArmarios():

    hayDatosArmarios = session.query(Armarios).all()
    if not hayDatosArmarios:

        #comprobamos si hay clientes
        clientesExisten=session.query(Cliente).all()
        tiposArmariosExisten=session.query(TipoArmario).all()

        if not clientesExisten or not tiposArmariosExisten:
            logger.log("WARNING", "Datos Prueba Armarios. NO existen clientes, o tipos de armarios")
        else:
            for i in range(50):
                #hago un random de los clientes
                cliente = random.choice(clientesExisten)
                #hago un random del tipo de armarios
                tipoArmario=random.choice(tiposArmariosExisten)
                #hago un random de los gramos entre 1 y 500
                gramos=random.randint(1,500)
                nuevoArmario=Armarios(id_cliente=cliente.id,
                                      id_tipo_armario=tipoArmario.id,
                                      gramos=gramos)
                session.add(nuevoArmario)

            session.commit()
            logger.log("INFO", "Datos Prueba Armarios. Datos de prubea de la tabla Armarios cargado correctamente")
    else:
        logger.log("WARNING", "Datos Prueba Armarios. Datos de prubea de la tabla Armarios ya existen")






