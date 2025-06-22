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

    gd.ndim = int(datos.values[0][0])
    gd.coord_nodos = nodos.values.tolist()
    gd.conexion_elementos = elementos.values.tolist()
    gd.props = props.values.tolist()
    gd.restricciones = restricciones.values.tolist()
    gd.nn = len(nodos)
    gd.nels = len(elementos)
    gd.nf = np.zeros((gd.nn, gd.ndim))
    gd.loads = loads
