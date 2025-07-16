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

    #Arreglo para definir cuales columnas deben eliminarse de los datos.

    gd.neq = 0
    columnas_a_borrar = []
    if gd.ndim == 1 and gd.cer_por == 1:
        print("Pórtico de 1 dimension")
        columnas_a_borrar = [1, 3, 4, 5]
    elif gd.ndim == 2 and gd.cer_por == 1:
        print("Pórtico de 2 dimension")
        columnas_a_borrar = [3, 4, 5]

    if gd.cer_por == 0:
        columnas_a_borrar = [4, 5, 6]
        if gd.ndim == 1:
            print("Cercha de 1 dimension")
            columnas_a_borrar += [2, 3]
        elif gd.ndim == 2:
            print("Cercha de 2 dimensiones")
            columnas_a_borrar += [3]

    for fila in gd.restricciones:
        for i in sorted(columnas_a_borrar, reverse=True):
            del fila[i]
    #print(gd.restricciones)
    #Esto define el número de restricciones que se impone,
    # según dimensión, una vez se han borrado columnas
    gd.restri = len(gd.restricciones[0]) - 1