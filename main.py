from services import *
from services.services import *

def menu():
    while True:
        print("0) SALIR\n"
              "1) Ver las ventas realizadas en un mes\n"
              "2) Ver las ventas que ha realizado un cliente\n"
              "3) Ver las ventas que no están aceptadas\n"
              "4) Ver el cliente que ha realizado mas ventas\n"
              "5) Ver los clientes que hace 3 meses que no realizan una venta")

        opc = int(input("Dime que quieres hacer"))
        if opc==1:
            consulta1()
        elif opc==2:
            consulta2()
        elif opc==3:
            consulta3()
        elif opc==4:
            consulta4()
        elif opc==5:
            consulta5()
        else:
            break

if __name__ == '__main__':
    pass
