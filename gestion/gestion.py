from services.services import *
from db.factory.factory import *

class Gestor:
    #sino se han creado los datos por defecto se crean la primera vez que se ejecuta
    crearEstados()
    crearPreciosOro()  # automaticamente nada mas ejecutar al menu, se crean las cotizaciones del oro del dia de hoy si no hay
    crearClientes()
    crearVenta()
    def menu(self):
        print("\n0) SALIR\n"
              "1) Crear estados\n"
              "2) Crear clientes\n"
              "3) Crear ventas\n"
              "4) Generar una venta\n"
              "5) Ver las ventas realizadas en un mes\n"
              "6) Ver las ventas que ha realizado un cliente\n"
              "7) Ver las ventas que no están aceptadas\n"
              "8) Ver el cliente que ha realizado mas ventas\n"
              "9) Ver los clientes que hace 3 meses que no realizan una venta\n"
              "10) Insertar nuevo cliente\n"
              "11) Grafico de la cantidad de oro por cliente\n"
              "12) Grafico de ventas por mes\n"
              "13) Cambiar el estado de una venta\n")

    def ejecutarOpcion(self):
        opcion = 0
        while True:
            self.menu()
            try:
                opcion = int(input("Elige que quieres hacer\n"))

            except ValueError:
                print("Debes escribir un numero")
                continue #para que vuelva al menu y a preguntar cual quiere hacer


            if opcion==1:
                crearEstados()
            elif opcion==2:
                crearClientes()
            elif opcion==3:
                crearVenta()
            elif opcion==4:
                generar1Venta()
            elif opcion==5:
                consulta1()
            elif opcion==6:
                consulta2()
            elif opcion==7:
                consulta3()
            elif opcion==8:
                consulta4()
            elif opcion==9:
                consulta5()
            elif opcion==10:
                insertarCliente()
            elif opcion==11:
                graficoCantidadOroPorCliente()
            elif opcion==12:
                graficoTotalVentaPorMes()
            elif opcion==13:
                cambiarEstadoVenta()
            else:
                print("Has decicido salir")
                return
