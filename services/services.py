#Realizar aquí las consultas
import matplotlib.pyplot as plt
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from sqlalchemy import extract
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.functions import count, func

from db.config import session, Session
from db.models.models import *
from log.log import *

logger = Log()

def insertarCliente():
    logger.log("INFO", "Intentando insertar un nuevo cliente")

    print("Has decidido insertar un cliente")
    nombre=input("Introduce el nombre: ")
    apellidos=input("Introduce el apellido: ")
    fechaNacimiento = input("Introduce la fecha de nacimiento Ej: (20-12-2004): ")
    dni=input("Introduce el DNI: ")
    email=input("Introduce el email: ")
    nacionalidad=input("Introduce la nacionalidad: ")
    telefono=input("Introduce el telefono: ")
    direccion=input("Introduce la direccion: ")

    existeCliente = session.query(Cliente).filter((Cliente.dni==dni) | (Cliente.email==email) | (Cliente.telefono==telefono))

    if existeCliente:
        logger.log("ERROR", "Insertar Cliente. DNI, Telefono o email ya existen")
        return #para vovler al menu principal

    else:
        try:
            nuevoCliente = Cliente(
                nombre=nombre,
                apellidos=apellidos,
                fecha_nacimiento=datetime.strptime(fechaNacimiento, "%d-%m-%Y").date(), #pasar la fecha que introduce el usaario a ese formatp
                dni=dni,
                email=email,
                nacionalidad=nacionalidad,
                telefono=int(telefono),
                direccion=direccion,
                activo=True
            )
            session.add(nuevoCliente)

            session.commit()
            logger.log("INFO", f"Insertar Cliente. Cliente {nuevoCliente.nombre} {nuevoCliente.apellidos} guardado correctamente")
        #esta excepcion la he buscado, he insertado un cliente que ya coincidia en el dni y como es unique ha petado por eso tuve que poner esta excepcion para controlar que no meta un cliente que ya existe
        except Exception:
            logger.log("ERROR", "Insertar Cliente. Error al guardar el cliente")
            return #para que vuelva al menu y no se termine el programa



#1 Ventas realizadas en un mes que se introduzca por pantalla
def consulta1():

    while True:
        mes=int(input("Introduce el mes que quieres ver las ventas realizas"))
        if mes>0 and mes<=12:
            break

    ventas = session.query(Venta).filter(extract('month', Venta.fecha_venta)==mes).all()

    if ventas:
        for venta in ventas:
            print(venta)
        logger.log("INFO", f"Consulta 1. ventas realizadas en el mes {mes}")
    else:
        logger.log("WARNING", f"Consulta 1. No hay ventas en el mes {mes}")




#2 Ventas que ha realizado un cliente
def consulta2():
    id = input("Dime el cliente que quieres sabeer las ventas")

    try:
        idcliente = int(id)
    except ValueError:
        logger.log("ERROR", "Consulta 2. No introduce cantidad o el id del Cliente de tipo Int")
        return

    #sacamos si el cliente existe
    clienteExiste=session.query(Cliente).filter(Cliente.id==idcliente).first()

    #si el cliente existe sacamos las ventas que ha realizado
    if clienteExiste:
        ventas=session.query(Venta).filter(Venta.id_cliente==idcliente).all()

        if ventas:
            for venta in ventas:
                print(venta)
            logger.log("INFO", f"Consulta 2. Visualizacion de ventas que ha realizado el cliente {clienteExiste.nombre}")
        else:
            logger.log("WARNING", f"Consulta 2. Cliente {clienteExiste.nombre} no tiene ventas")
    else:
        logger.log("ERROR", f"Consulta 2. No existe el cliente con id {idcliente}")





#3 Tasaciones que no se encuentran aceptadas
def consulta3():

    #saco el id del estado aceptada y luego saco las tasaciones que no tengan como estado aceptadas
    estadoAceptadas=session.query(Estado).filter(Estado.nombre=="ACEPTADA").first()
    tasaciones=session.query(Venta).filter(Venta.id_estado!=estadoAceptadas.id).all()

    for tas in tasaciones:
        print(tas)
    logger.log("INFO", "Consulta 3. Visualizacion de todas las ventas que están aceptadas")





#4 Cliente que más ventas ha realizado
def consulta4():

    clienteMasVentas = (session.query(Cliente, Venta.id_cliente, count(Venta.id))
                        .join(Cliente, Cliente.id==Venta.id_cliente)
                        .group_by(Venta.id_cliente, Cliente)
                        .order_by(count(Venta.id).desc()).first())

#comproobamos que haya ventas
    if not clienteMasVentas:
        logger.log("WARNING", "Consulta 4. No hay ventas registradas")
    else:
        logger.log("INFO", f"Consulta 4. Cliente con ms ventas") #preguntar a Fran si esto funciona
        print("El cliente que mas ventas ha realizado es: ")
        print(clienteMasVentas)





#5 búsqueda de clientes que hace 3 meses que no realizan una venta.
def consulta5():

#para restar tres meses
    hace3Meses = date.today() - relativedelta(months=3)

    cliente = ((session.query(Cliente)
               .join(Venta, Venta.id_cliente==Cliente.id)
               .filter(Venta.fecha_venta<hace3Meses)).distinct().all()) #esta bien poner distinct porque si un cliente tiene 3 ventas antiguas va a salir 3 veces

    for c in cliente:
        print(c)
    logger.log("INFO", "Consulta 5. Visualizacion de los clientes que hace 3 meses que no realizan una venta")






def graficoCantidadOroPorCliente():

    clientes=session.query(Cliente).all() #saco todos los clientes

    #saco la suma de la cantidad de oro por cliente
    oroPorCliente=(session.query(Venta.id_cliente, func.sum(Venta.cantidad)) #si no pongo func no deja hacer el sum
                   .group_by(Venta.id_cliente)).all()

    nombresClientes = []
    cantidadOro = []

    #comprobamos que hay ventas para poder hacer el gradico
    if oroPorCliente:
        logger.log("INFO", "Grafico 1: Cantidad de oro por cliente")

        # recorro los clientes
        for cliente in clientes:
            for id_cliente, cantidad in oroPorCliente:  # recorro el id del cliente y la cantidad de la consulta de OroPorCliente
                if cliente.id == id_cliente:  # si es el mismo cliente se añade el nombre y la cantidad de oro
                    nombresClientes.append(cliente.nombre)
                    cantidadOro.append(cantidad)

        plt.bar(nombresClientes, cantidadOro)
        plt.title("Cantidad de oro por cliente")
        plt.xlabel("Nombre")
        plt.ylabel("Cantidad de oro")
        plt.show()

    else:
        logger.log("WARNING", "Grafico 1: No hay ventas registradas para generar el gráfico de oro por cliente")







def graficoTotalVentaPorMes():

#saco el mes y cuento las ventas por ese mes y lo agrupo por mes
    ventasPorMes = (session.query(extract("month", Venta.fecha_venta), count(Venta.id))
                    .group_by(extract('month', Venta.fecha_venta))
                    .order_by(extract("month", Venta.fecha_venta)).all())

    meses = []
    totalVentas = []

#comrpobamos que ya hay ventas para poder hacer el grafico
    if ventasPorMes:
        logger.log("INFO", "Gráfico 2: Total de ventas por mes")

        for mes, total in ventasPorMes:
            meses.append(mes),
            totalVentas.append(total)

        plt.bar(meses, totalVentas)
        plt.title("Total de venta por mes")
        plt.xlabel("MES")
        plt.ylabel("VENTAS")
        plt.show()

    else:
        logger.log("WARNING", "Gráfico 2: No hay ventas registradas para generar el gráfico de ventas por mes")



