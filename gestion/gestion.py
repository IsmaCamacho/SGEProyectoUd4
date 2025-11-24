from services.services import *
from db.factory.factory import *

class Gestor:
    def menu(self):
        print("\n0) SALIR\n"
              "1) Crear estados\n"
              "2) Crear clientes\n"
              "3) Crear precios del oro\n"
              "4) Crear ventas\n"
              "5) Ver las ventas realizadas en un mes\n"
              "6) Ver las ventas que ha realizado un cliente\n"
              "7) Ver las ventas que no están aceptadas\n"
              "8) Ver el cliente que ha realizado mas ventas\n"
              "9) Ver los clientes que hace 3 meses que no realizan una venta\n"
              "10) Insertar nuevo cliente\n"
              "11) Grafico de la cantidad de oro por cliente\n"
              "12) Grafico de ventas por mes\n")

    def ejecutarOpcion(self):
        while True:
            self.menu()
            opcion=int(input("Elige que quieres hacer\n"))
            if opcion==1:
                crearEstados()
            elif opcion==2:
                crearClientes()
            elif opcion==3:
                crearPreciosOro()
            elif opcion==4:
                crearVenta()
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
            else:
                return
