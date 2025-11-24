#Realizar aquí las consultas
import matplotlib.pyplot as plt
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from sqlalchemy import extract
from sqlalchemy.sql.functions import count, func

from db.config import session, Session
from db.models.models import *

def insertarCliente():
    print("Has decidido insertar un cliente")
    nombre=input("Introduce el nombre: ")
    apellidos=input("Introduce el apellido: ")
    fechaNacimiento = input("Introduce la fecha de nacimiento Ej: (20-12-2004): ")
    dni=input("Introduce el DNI: ")
    email=input("Introduce el email: ")
    nacionalidad=input("Introduce la nacionalidad: ")
    telefono=input("Introduce el telefono: ")
    direccion=input("Introduce la direccion: ")

    try:
        nuevoCliente = Cliente(
            nombre=nombre,
            apellidos=apellidos,
            fecha_nacimiento=datetime.strptime(fechaNacimiento, "%d-%m-%Y").date(), #pasar la fecha que introduce el usaario a ese formatp
            dni=dni,
            email=email,
            nacionalidad=nacionalidad,
            telefono=int(telefono),
            direccion=direccion
        )
        session.add(nuevoCliente)

        session.commit()
        print("Cliente guardado correctamente")
    except Exception as e:
        print(f"Error al guardar el cliente {e}")
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
    else:
        print("No hay ventas en el mes " + str(mes))





#2 Ventas que ha realizado un cliente
def consulta2():
    idcliente = int(input("Dime el cliente que quieres sabeer las ventas"))

    #sacamos si el cliente existe
    clienteExiste=session.query(Cliente).filter(Cliente.id==idcliente).first()

    #si el cliente existe sacamos las ventas que ha realizado
    if clienteExiste:
        ventas=session.query(Venta).filter(Venta.id_cliente==idcliente).all()

        if ventas:
            for venta in ventas:
                print(venta)
        else:
            print("Ese cliente no tiene ventas")
    else:
        print("No existe ese cliente")





#3 Tasaciones que no se encuentran aceptadas
def consulta3():

    #saco el id del estado aceptada y luego saco las tasaciones que no tengan como estado aceptadas
    estadoAceptadas=session.query(Estado).filter(Estado.nombre=="ACEPTADA").first()
    tasaciones=session.query(Venta).filter(Venta.id_estado!=estadoAceptadas.id).all()

    for tas in tasaciones:
        print(tas)





#4 Cliente que más ventas ha realizado
def consulta4():

    clienteMasVentas = (session.query(Cliente, Venta.id_cliente, count(Venta.id))
                        .join(Cliente, Cliente.id==Venta.id_cliente)
                        .group_by(Venta.id_cliente, Cliente)
                        .order_by(count(Venta.id).desc()).first())

#comproobamos que haya ventas
    if not clienteMasVentas:
        print("No hay ninguna venta aun")
    else:
        print("El cliente que mas ventas ha realizado es: ")
        print(clienteMasVentas)





#5 búsqueda de clientes que hace 3 meses que no realizan una venta.
def consulta5():

#para restar tres meses
    hace3Meses = date.today() - relativedelta(months=3)

    cliente = (session.query(Cliente)
               .join(Venta, Venta.id_cliente==Cliente.id)
               .filter(Venta.fecha_venta<hace3Meses)).all()

    for c in cliente:
        print(c)






def graficoCantidadOroPorCliente():

    clientes=session.query(Cliente).all() #saco todos los clientes

    #saco la suma de la cantidad de oro por cliente
    oroPorCliente=(session.query(Venta.id_cliente, func.sum(Venta.cantidad))
                   .group_by(Venta.id_cliente)).all()

    nombresClientes = []
    cantidadOro = []

#recorro los clientes
    for cliente in clientes:
        for id_cliente, cantidad in oroPorCliente: #recorro el id del cliente y la cantidad de la consulta de OroPorCliente
            if cliente.id==id_cliente:  #si es el mismo cliente se añade el nombre y la cantidad de oro
                nombresClientes.append(cliente.nombre)
                cantidadOro.append(cantidad)

    plt.bar(nombresClientes, cantidadOro)
    plt.title("Cantidad de oro por cliente")
    plt.xlabel("Nombre")
    plt.ylabel("Cantidad de oro")
    plt.show()





def graficoTotalVentaPorMes():

#saco el mes y cuento las ventas por ese mes y lo agrupo por mes
    ventasPorMes = (session.query(extract("month", Venta.fecha_venta), count(Venta.id))
                    .group_by(extract('month', Venta.fecha_venta))
                    .order_by(extract("month", Venta.fecha_venta)).all())

    meses = []
    totalVentas = []

    for mes, total in ventasPorMes:
        meses.append(mes),
        totalVentas.append(total)

    plt.bar(meses, totalVentas)
    plt.title("Total de venta por mes")
    plt.xlabel("MES")
    plt.ylabel("VENTAS")
    plt.show()
