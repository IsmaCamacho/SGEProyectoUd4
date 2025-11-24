#Realizar aquí las consultas
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from sqlalchemy import extract
from sqlalchemy.sql.functions import count

from db.config import session, Session
from db.models.models import *


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

    tasaciones=session.query(Venta).filter(Venta.id_estado!=2).all()

    for tas in tasaciones:
        print(tas)

#4 Cliente que más ventas ha realizado
def consulta4():

    clienteMasVentas = (session.query(Cliente, Venta.id_cliente, count(Venta.id))
                        .join(Cliente, Cliente.id==Venta.id_cliente)
                        .group_by(Venta.id_cliente, Cliente)
                        .order_by(count(Venta.id).desc()).first())

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
