import pandas as pd
import numpy as np
import discretizacion.datosGenerales as gd  # Usamos gd para llamar variables globales


def leer_datos_desde_excel(ruta="datos/datos.xlsx"):
    print(f"\n📥 Leyendo datos desde: {ruta}")

    # Leer cada hoja del archivo Excel
    elementos = pd.read_excel(ruta, sheet_name="Elementos")
    print("\n📄 Elementos:")
    print(elementos)

    nodos = pd.read_excel(ruta, sheet_name="Nodos Coord")
    print("\n📄 Nodos Coord:")
    print(nodos)

    datos = pd.read_excel(ruta, sheet_name="Datos")
    print("\n📄 Datos:")
    print(datos)

    loads = pd.read_excel(ruta, sheet_name="Nodos Loads")
    print("\n📄 Nodos Loads:")
    print(loads)

    props = pd.read_excel(ruta, sheet_name="Props")
    print("\n📄 Props:")
    print(props)

    restricciones = pd.read_excel(ruta, sheet_name="Restricciones")
    print("\n📄 Restricciones:")
    print(restricciones)

    # Guardar en variables globales
    gd.ndim = int(datos.values[0][0])
    print("Dimension")
    print(gd.ndim)
    gd.inf_nodos = nodos.values.tolist()
    print("Info nodos:")
    print(gd.inf_nodos)
    gd.inf_elementos = elementos.values.tolist()
    print("Inf elementos:")
    print(gd.inf_elementos)
    gd.props = props.values.tolist()
    print("Inf propiedades")
    print(gd.props)

    gd.nn = len(nodos)
    print("Nn")
    print(gd.nn)
    gd.nels = len(elementos)
    print("nels")
    print(gd.nels)
    gd.nf = np.zeros((gd.nn, gd.ndim))
    print("Nf")
    print(gd.nf)