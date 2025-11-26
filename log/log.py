from datetime import datetime
import os

class Log:
    def __init__(self):
        self.nombre_fichero = f"logs/ErrorCreandoFichero_MOVIMIENTOS-VENTAS.log"

    def log(self, tipo, mensaje):
        self.generarFichero()

        timestamp = datetime.now().strftime("%d%m%Y %H:%M:%S")
        linea_log = f"[{timestamp}] ---- [{tipo}] ---- {mensaje}\n"

        with open(self.nombre_fichero, 'a', encoding='utf-8') as f:  #el encoding es para los carateres como la ñ
            f.write(linea_log)
            print(f"Guardado en log:{linea_log}")

    def generarFichero(self):
        fecha = datetime.now().strftime("%Y%m%d").lower()  #para ordenar el log automaticamente con la fecha
        self.nombre_fichero = f"logs/{fecha}_MOVIMIENTOS-VENTAS.log"
        os.makedirs(
            os.path.dirname(self.nombre_fichero) if os.path.dirname(self.nombre_fichero) else '.',
            exist_ok=True)  #Comprueba los directorios de la ruta, si no tiene el directorio es esta carpeta, si ya existe no crea nada y no da error