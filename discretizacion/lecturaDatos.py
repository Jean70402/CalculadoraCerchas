import pandas as pd
import numpy as np
import discretizacion.datosGenerales as gd  # Usamos gd para llamar variables globales


def leer_datos_desde_excel(ruta="datos/datos.xlsx"):
    print(f"\n📥 Leyendo datos desde: {ruta}")

    # Leer cada hoja del archivo Excel
    elementos = pd.read_excel(ruta, sheet_name="Elementos")

    nodos = pd.read_excel(ruta, sheet_name="Nodos Coord")

    datos = pd.read_excel(ruta, sheet_name="Datos")

    loads = pd.read_excel(ruta, sheet_name="Nodos Loads")

    props = pd.read_excel(ruta, sheet_name="Props")

    restricciones = pd.read_excel(ruta, sheet_name="Restricciones")

    # Guardar en variables globales
    #Se define gd como global data, son las variables para usarse a lo largo del programa
    #Se guardan cada una accediendo a su valor (.values) y se elige la fila y columna de los datos
    gd.ndim = int(datos.values[0][0])
    gd.coord_nodos = nodos.values.tolist()
    gd.conexion_elementos = elementos.values.tolist()
    for j in range(2):
        for i in range (len(gd.conexion_elementos)):
            gd.conexion_elementos[i][j + 1]-=1
    gd.props = props.values.tolist()
    gd.restricciones = restricciones.values.tolist()
    #Len es la propiedad para llamar longitudes, devuelve enteros.
    gd.nn = len(nodos)
    gd.nels = len(elementos)
    gd.loads = loads
