import math

import numpy as np
from discretizacion.insertEA import insertarEa
import discretizacion.datosGenerales as gd


def pin_jointed():
    # define una lista de matriz vacia para elementos y para los km generados:
    elementos = []
    km_g = []
    # Iteración para recuperar valores de elementos y calcular las longitudes
    for fila in gd.conexion_elementos:
        # Lectura de los valores de la segunda y tercera columna (valores de nodos)
        nodo_i = fila[1]
        nodo_j = fila[2]
        # Recuperacion y guardado de la información de nodos (x,y,z)
        coords_i = gd.coord_nodos[nodo_i][:3]  # Primeras 3 columnas del nodo_i
        coords_j = gd.coord_nodos[nodo_j][:3]  # Primeras 3 columnas del nodo_j

        # detalle para 1 dimension
        if gd.ndim == 1:
            x1 = coords_j[0]
            x2 = coords_i[0]
            ell = abs(x2 - x1)
            ea = insertarEa(fila[0])
            ea_L = ea / ell
            km_local = np.array([
                [1, -1],
                [-1, 1]
            ]) * ea_L

            km_g.append(km_local)
            completo = np.append(fila, ell)
            elementos.append(completo)
        # detalle para 2 dimensiones
        if gd.ndim == 2:
            # Toma de datos de las posiciones de nodos conectados
            x1 = coords_j[0]
            y1 = coords_j[1]
            x2 = coords_i[0]
            y2 = coords_i[1]
            # Cálculo de la longitud
            ell = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            # Cálculo de senos y cosenos
            cos = (x2 - x1) / ell
            sen = (y2 - y1) / ell
            # Cálculo de cosenos cuadrados, en variables para fácil lectura
            a = cos * cos
            b = sen * sen
            c = cos * sen
            # Recuperación del valor de EA
            ea = insertarEa(fila[0])
            ea_L = ea / ell
            # Cálculo y formación de la matriz km de 1 elemento:
            km_local = np.array([
                [a, c, -a, -c],
                [c, b, -c, -b],
                [-a, -c, a, c],
                [-c, -b, c, b]
            ])

            km_local = km_local * ea_L
            # Añadir el km local al km global
            km_g.append(km_local)
            # Añadir longitud a la fila de elementos
            completo = np.append(fila, ell)
            elementos.append(completo)
        if gd.ndim == 3:
            x1 = coords_j[0]
            y1 = coords_j[1]
            z1 = coords_j[2]
            x2 = coords_i[0]
            y2 = coords_i[1]
            z2 = coords_i[2]

            xl = x2 - x1
            yl = y2 - y1
            zl = z2 - z1

            ell = math.sqrt((xl * xl) + (yl * yl) + (zl * zl))
            xl = xl / ell
            yl = yl / ell
            zl = zl / ell
            a = xl * xl
            b = yl * yl
            c = zl * zl
            d = xl * yl
            e = yl * zl
            f = zl * xl
            ea = insertarEa(fila[0])
            ea_L = ea / ell
            # Cálculo y formación de la matriz km de 1 elemento:
            km_local = np.array([
                [a, d, f, -a, -d, -f],
                [d, b, e, -d, -b, -e],
                [f, e, c, -f, -e, -c],
                [-a, -d, -f, a, d, f],
                [-d, -b, -e, d, b, e],
                [-f, -e, -c, f, e, c]
            ])

            km_local = km_local * ea_L
            # Añadir el km local al km global
            km_g.append(km_local)
            # Añadir longitud a la fila de elementos
            completo = np.append(fila, ell)
            elementos.append(completo)

    # Ubicación de variables en memoria global:
    gd.elementos = np.array(elementos)
    gd.km_locales = km_g
    #print(gd.km_locales[15])