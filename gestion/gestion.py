from sqlalchemy import false

from services.services import *
from db.factory.factory import *

class Gestor:

    datosInicialesCargados = False

    def __init__(self):
        if not Gestor.datosInicialesCargados:
            #sino se han creado los datos por defecto se crean la primera vez que se ejecuta
            crearEstados()
            crearPreciosOro()  # automaticamente nada mas ejecutar al menu, se crean las cotizaciones del oro del dia de hoy si no hay
            crearClientes()
            crearVenta()
            Gestor.datosInicialesCargados = True

    def menu(self):
        print("\n0) SALIR\n"
              "1) Generar una venta\n"
              "2) Ver las ventas realizadas en un mes\n"
              "3) Ver las ventas que ha realizado un cliente\n"
              "4) Ver las ventas que no están aceptadas\n"
              "5) Ver el cliente que ha realizado mas ventas\n"
              "6) Ver los clientes que hace 3 meses que no realizan una venta\n"
              "7) Insertar nuevo cliente\n"
              "8) Grafico de la cantidad de oro por cliente\n"
              "9) Grafico de ventas por mes\n"
              "10) Cambiar el estado de una venta\n"
              "11) Dar de baja a un cliente\n"
              "12) Dar de alta a un cliente existente\n")

    def ejecutarOpcion(self):
        while True:
            self.menu()
            try:
                opcion = int(input("Elige que quieres hacer\n"))

                if opcion == 1:
                    generar1Venta()
                elif opcion == 2:
                    consulta1()
                elif opcion == 3:
                    consulta2()
                elif opcion == 4:
                    consulta3()
                elif opcion == 5:
                    consulta4()
                elif opcion == 6:
                    consulta5()
                elif opcion == 7:
                    insertarCliente()
                elif opcion == 8:
                    graficoCantidadOroPorCliente()
                elif opcion == 9:
                    graficoTotalVentaPorMes()
                elif opcion == 10:
                    cambiarEstadoVenta()
                elif opcion == 11:
                    darBajaCliente()
                elif opcion == 12:
                    darAltaClienteExistente()
                else:
                    logger.log("INFO", "Usuario ha salido de la aplicación")
                    return

            except ValueError:
                #error al convertir la opción a número
                logger.log("ERROR", "Menú. Debes escribir un número")
                continue

            except Exception as e:
                #error interno de las funciones
                logger.log("ERROR", f"Error inesperado en la ejecución del menú: {e}")
                print("\nHa ocurrido un error inesperado, vuelve a intentarlo.\n")
                continue

