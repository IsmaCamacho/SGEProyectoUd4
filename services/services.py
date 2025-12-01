#Realizar aquí las consultas
import matplotlib.pyplot as plt
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

#for v in ventas:
#    id_venta, nombre, fecha, importe = v
#    print(id_venta, nombre, fecha.strftime("%d-%m-%Y"), importe)
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

    if (not nombre or not apellidos or not fechaNacimiento or not dni or
            not email or not nacionalidad or not telefono or not direccion):
        logger.log("ERROR", "Insertar Cliente. Ningún campo puede estar vacío")
        return

    try:
        telefonoInt = int(telefono)
    except ValueError:
        logger.log("ERROR", "Insertar Cliente. El teléfono debe ser un número entero")
        return

    existeCliente = session.query(Cliente).filter((Cliente.dni==dni) | (Cliente.email==email) | (Cliente.telefono==telefonoInt)).first()

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
        mes=input("Introduce el mes que quieres ver las ventas realizas (del 1 al 12)")
        try:
            mesOk=int(mes)
            if mesOk > 0 and mesOk <= 12:
                break
        except ValueError:
            logger.log("ERROR", "Consulta 1. No introduce el mes de tipo Int")
            return

    ventas = session.query(Venta).filter(extract('month', Venta.fecha_venta)==mesOk).all()

    if ventas:
        for venta in ventas:
            print(venta)
        logger.log("INFO", f"Consulta 1. ventas realizadas en el mes {mesOk}")
    else:
        logger.log("WARNING", f"Consulta 1. No hay ventas en el mes {mesOk}")




#2 Ventas que ha realizado un cliente
def consulta2():
    # Ventas que ha realizado un cliente

    print("Información de los clientes: ")
    clientesTodos = session.query(Cliente).all()
    for c in clientesTodos:
        print(c)

    try:
        clienteId = int(input("Introduce el Id del cliente para ver sus ventas."))
    except ValueError:
        logger.log("ERROR", "Consulta 2. Cansulta de ventas de un cliente cancelada: ID no numérico")
        return

    clienteExiste = session.query(Cliente).filter(Cliente.id == clienteId).first()

    if not clienteExiste:
        logger.log("WARNING", f"Consulta 2. Cliente {clienteId} NO existe")
    else:
        ventasCliente = session.query(Venta).filter(Venta.id_cliente == clienteId).all()

        if ventasCliente:
            for v in ventasCliente:
                print(v)
            logger.log("INFO", f"Consulta 2. Ventas realizadas del cliente {clienteId}")
        else:
            logger.log("WARNING", f"Consulta 2. Sin ventas del cliente {clienteId}")





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
    hace3Meses = date.today() - relativedelta(months=3)

    clientes = (session.query(Cliente)
                .join(Venta, Venta.id_cliente == Cliente.id)
                .group_by(Cliente.id)
                .having(func.max(Venta.fecha_venta) < hace3Meses)
                .all())

    for c in clientes:
        print(c)
    logger.log("INFO", "Consulta 5. Visualización de los clientes que hace 3 meses que no realizan una venta")





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


def graficoArribaOtraForma():

    oroPorCliente = (
        session.query(Venta.id_cliente, Cliente.nombre.label("nombre"), func.sum(Venta.cantidad).label("cantidad"))
        .join(Cliente, Cliente.id == Venta.id_cliente)
        .group_by(Venta.id_cliente)
        .group_by(Cliente.nombre).all())

    if not oroPorCliente:
        logger.log("WARNING", "Grafico 1: No hay ventas, no se puede generar el gráfico")
    else:
        logger.log("INFO", "Grafico 1: Cantidad de oro por cliente")

        nombres = []
        cantidad = []

        for o in oroPorCliente:
            nombres.append(o.nombre)
            cantidad.append(o.cantidad)

        plt.bar(nombres, cantidad)
        plt.title("CANTIDAD DE ORO POR CLIENTE")
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



#A PARTIR DE AQUI EXAMEN!
def guardarOroCliente():
    #comrpuebo que existen clientes y tipos de armario
    clientesExiste=session.query(Cliente).all()
    tiposArmarioExiste=session.query(TipoArmario).all()

    if not clientesExiste or not tiposArmarioExiste:
        logger.log("WARNING", "Guardar Oro Cliente. NO existen clientes, o tipos de armarios")
    else:
        #si hay ambas cosas muestro los clientes para que elija el cliente
        for c in clientesExiste:
            print(c)

        try:
            idCliente = int(input("Introduce el id del cliente del que quieres guardar oro"))
        except ValueError:
            logger.log("ERROR", "Guardar Oro Cliente. Dato introducido no es de tipo númerico")
            return

        #comprobamos si existe el cliente que ha intrtroducido
        existeCliente = session.query(Cliente).filter(Cliente.id==idCliente).first()
        if not existeCliente:
            logger.log("ERROR", "Guardar Oro Cliente. NO existe cliente")
        else:
            #si existe el cliente comprobamos si tiene oro guardado
            oroCliente = session.query(Armarios).filter(Armarios.id_cliente==idCliente).first()
            if not oroCliente:
                logger.log("WARNING", "Guardar Oro Cliente. NO tiene oro guardado")
                try:
                    cantidadOro = int(input("Introduce la cantidad de oro que quieres guardar en gramos"))
                except ValueError:
                    logger.log("ERROR", "Guardar Oro Cliente. Dato introducido no es de tipo númerico")
                    return

                #se guarda el oro
                if cantidadOro>0 and cantidadOro<=100:
                    #se guarda en armario pequeño
                    guardarOro=Armarios(id_cliente=idCliente,
                                        id_tipo_armario=1,
                                        gramos=cantidadOro)
                    session.add(guardarOro)
                    guardarHistorico = MovimientosArmarios(cantidad=cantidadOro,
                                                           operacion="Nuevo armario guardado",
                                                           fecha=date.today(),
                                                           id_cliente=idCliente)
                    session.add(guardarHistorico)
                    logger.log("INFO", "Guardar Oro Cliente. Oro guardado correctamente")

                elif cantidadOro>100 and cantidadOro<=300:
                    #se guarda en armario mediano
                    guardarOro = Armarios(id_cliente=idCliente,
                                          id_tipo_armario=2,
                                          gramos=cantidadOro)
                    session.add(guardarOro)
                    guardarHistorico = MovimientosArmarios(cantidad=cantidadOro,
                                                           operacion="Nuevo armario guardado",
                                                           fecha=date.today(),
                                                           id_cliente=idCliente)
                    session.add(guardarHistorico)
                    logger.log("INFO", "Guardar Oro Cliente. Oro guardado correctamente")

                elif cantidadOro>300 and cantidadOro<=2000:
                    guardarOro = Armarios(id_cliente=idCliente,
                                          id_tipo_armario=3,
                                          gramos=cantidadOro)
                    session.add(guardarOro)
                    guardarHistorico = MovimientosArmarios(cantidad=cantidadOro,
                                                           operacion="Nuevo armario guardado",
                                                           fecha=date.today(),
                                                           id_cliente=idCliente)
                    session.add(guardarHistorico)
                    logger.log("INFO", "Guardar Oro Cliente. Oro guardado correctamente")

                elif cantidadOro<0 or cantidadOro>2000:
                    logger.log("WARNING", "Guardar Oro Cliente. Cantidad oro fuera de limites")

                session.commit()
            else:
                try:
                    opcion = int(input("Ya tienes un armario asignado. Elige:\n"
                                       "1) Retirar Oro\n"
                                       "2) Guardar Oro\n"))
                except ValueError:
                    logger.log("ERROR", "Guardar Oro Cliente. Dato introducido no es de tipo númerico")
                    return

                if opcion <1 or opcion>2:
                    logger.log("ERROR", "Guardar Oro Cliente. Opcion introducida no válida")
                elif opcion==1:
                    try:
                        cantidadOroRetirar = int(input("Introduce la cantidad de oro que quieres retirar en gramos"))
                    except ValueError:
                        logger.log("ERROR", "Guardar Oro Cliente. Dato introducido no es de tipo númerico")
                        return

                    #sacamos el la canidad que tiene y le restamos lo que quiere restar
                    armarioCliente=session.query(Armarios).filter(Armarios.id_cliente==idCliente).first()

                    #si quiere retirar mas oro del que tiene salta un warning se le avisa
                    if armarioCliente.gramos < cantidadOroRetirar:
                        logger.log("WARNING", "Guardar Oro Cliente. No puedes retirar mas oro del que tienes")
                    else:
                        oroFinal = armarioCliente.gramos - cantidadOroRetirar
                        if oroFinal > 0 and oroFinal <= 100:
                            # se guarda en armario pequeño y actualizamos gramos
                            #comprobamos que tiene el mismo armario u otro
                            if armarioCliente.id_tipo_armario!=1:
                                armarioCliente.id_tipo_armario=1

                            armarioCliente.gramos=oroFinal
                            guardarHistorico = MovimientosArmarios(cantidad=oroFinal,
                                                                   operacion="Armario actualizado (retirada)",
                                                                   fecha=date.today(),
                                                                   id_cliente=idCliente)
                            session.add(guardarHistorico)
                            session.commit()
                            logger.log("INFO", "Guardar Oro Cliente. Oro y armario actualizado correctamente")

                        elif oroFinal > 100 and oroFinal <= 300:
                            # se guarda en armario mediano y actualizamos gramos
                            # comprobamos que tiene el mismo armario u otro
                            if armarioCliente.id_tipo_armario != 2:
                                armarioCliente.id_tipo_armario = 2

                            armarioCliente.gramos = oroFinal
                            guardarHistorico = MovimientosArmarios(cantidad=oroFinal,
                                                                   operacion="Armario actualizado (retirada)",
                                                                   fecha=date.today(),
                                                                   id_cliente=idCliente)
                            session.add(guardarHistorico)
                            session.commit()
                            logger.log("INFO", "Guardar Oro Cliente. Oro y armario actualizado correctamente")

                        elif oroFinal > 300 and oroFinal <= 2000:
                            # se guarda en armario grande y actualizamos gramos
                            # comprobamos que tiene el mismo armario u otro
                            if armarioCliente.id_tipo_armario != 3:
                                armarioCliente.id_tipo_armario = 3
                            guardarHistorico = MovimientosArmarios(cantidad=oroFinal,
                                                                   operacion="Armario actualizado (retirada)",
                                                                   fecha=date.today(),
                                                                   id_cliente=idCliente)
                            session.add(guardarHistorico)
                            armarioCliente.gramos = oroFinal

                            session.commit()
                            logger.log("INFO", "Guardar Oro Cliente. Oro y armario actualizado correctamente")

                        elif oroFinal < 0:
                            logger.log("WARNING", "Guardar Oro Cliente. Cantidad oro fuera de limites")

                elif opcion==2:
                    try:
                        cantidadOroSumar = int(input("Introduce la cantidad de oro que quieres retirar en gramos"))
                    except ValueError:
                        logger.log("ERROR", "Guardar Oro Cliente. Dato introducido no es de tipo númerico")
                        return

                    #sacamos el la canidad que tiene y le sumamos lo que quiere sumar
                    armarioCliente=session.query(Armarios).filter(Armarios.id_cliente==idCliente).first()

                    oroFinalSumado=armarioCliente.gramos + cantidadOroSumar

                    if oroFinalSumado > 2000:
                        logger.log("WARNING", "Guardar Oro Cliente. Cantidad oro fuera de limites")
                    else:
                        if oroFinalSumado > 0 and oroFinalSumado <= 100:
                            # se guarda en armario pequeño y actualizamos gramos
                            #comprobamos que tiene el mismo armario u otro
                            if armarioCliente.id_tipo_armario!=1:
                                armarioCliente.id_tipo_armario=1

                            armarioCliente.gramos=oroFinalSumado
                            guardarHistorico = MovimientosArmarios(cantidad=oroFinalSumado,
                                                                   operacion="Armario actualizado (ingreso)",
                                                                   fecha=date.today(),
                                                                   id_cliente=idCliente)
                            session.add(guardarHistorico)
                            session.commit()
                            logger.log("INFO", "Guardar Oro Cliente. Oro y armario actualizado correctamente")

                        elif oroFinalSumado > 100 and oroFinalSumado <= 300:
                            # se guarda en armario mediano y actualizamos gramos
                            # comprobamos que tiene el mismo armario u otro
                            if armarioCliente.id_tipo_armario != 2:
                                armarioCliente.id_tipo_armario = 2

                            armarioCliente.gramos = oroFinalSumado
                            guardarHistorico = MovimientosArmarios(cantidad=oroFinalSumado,
                                                                   operacion="Armario actualizado (ingreso)",
                                                                   fecha=date.today(),
                                                                   id_cliente=idCliente)
                            session.add(guardarHistorico)
                            session.commit()
                            logger.log("INFO", "Guardar Oro Cliente. Oro y armario actualizado correctamente")

                        elif oroFinalSumado > 300 and oroFinalSumado <= 2000:
                            # se guarda en armario grande y actualizamos gramos
                            # comprobamos que tiene el mismo armario u otro
                            if armarioCliente.id_tipo_armario != 3:
                                armarioCliente.id_tipo_armario = 3
                            guardarHistorico = MovimientosArmarios(cantidad=oroFinalSumado,
                                                                   operacion="Armario actualizado (ingreso)",
                                                                   fecha=date.today(),
                                                                   id_cliente=idCliente)
                            session.add(guardarHistorico)
                            armarioCliente.gramos = oroFinalSumado

                            session.commit()
                            logger.log("INFO", "Guardar Oro Cliente. Oro y armario actualizado correctamente")



def mostrarHistoricoCliente():
    clientesExiste = session.query(Cliente).all()
    movimientos = session.query(MovimientosArmarios).all()

    if not clientesExiste or not movimientos:
        logger.log("WARNING", "Historico cliente. NO existen clientes, o registro de historicos")
    else:
        # si hay ambas cosas muestro los clientes para que elija el cliente
        for c in clientesExiste:
            print(c)

        try:
            idCliente = int(input("Introduce el id del cliente del que quieres ver el historico"))
        except ValueError:
            logger.log("ERROR", "Historico cliente. Dato introducido no es de tipo númerico")
            return

        #comrpuebo que existe el cliente
        clienteExiste = session.query(Cliente).filter(Cliente.id==idCliente).first()

        if not clienteExiste:
            logger.log("WARNING", f"Historico cliente. Cliente {idCliente} no tiene histórico")
        else:
        #saco el historico de ese cliente
            historicoCliente = (session.query(MovimientosArmarios)
                                .filter(MovimientosArmarios.id_cliente==idCliente)
                                .order_by(MovimientosArmarios.fecha.desc()).all())
            if not historicoCliente:
                logger.log("WARNING", f"Historico cliente. Cliente {idCliente} no tiene histórico")
            else:
                for c in historicoCliente:
                    print(c)
                logger.log("INFO", f"Historico cliente. Consulta del histórico del cliente {idCliente}")





def comprobarArmarios():

    #sacamos todos los registros de la tabla armarios
    todosArmarios=session.query(Armarios).all()

    if not todosArmarios:
        logger.log("ERROR", "Comprobar Armarios. No hay registros de armarios aún")
    else:
        #recorro todos los armarios
        for armario in todosArmarios:

            armarioExacto = session.query(Armarios).filter(armario.id==Armarios.id).first()
            if (armarioExacto.gramos > 0 and armarioExacto<101) and armarioExacto.id_tipo_armario !=1:
                armarioExacto.id_tipo_armario=1
                logger.log("INFO", f"Comprobar Armarios. Modificación del armario {armario.id}")
                session.commit()
            elif (armarioExacto.gramos > 101 and armarioExacto<301) and armarioExacto.id_tipo_armario !=2:
                armarioExacto.id_tipo_armario = 2
                logger.log("INFO", f"Comprobar Armarios. Modificación del armario {armario.id}")
                session.commit()
            elif (armarioExacto.gramos > 301 and armarioExacto<2001) and armarioExacto.id_tipo_armario !=3:
                armarioExacto.id_tipo_armario = 3
                logger.log("INFO", f"Comprobar Armarios. Modificación del armario {armario.id}")
                session.commit()
