import math

import numpy as np

import discretizacion.datosGenerales as gd
from discretizacion.insertEA import insertarEa, insertarEiY, insertarEiZ, insertarG


def rigid_jointed():
    # define una lista de matriz vacia para elementos y para los km generados:
    elementos = []
    km_g = []

    # Iteración para recuperar valores de elementos y calcular las longitudes
    for fila in gd.conexion_elementos:
        nodo_i = fila[1]
        nodo_j = fila[2]
        coords_i = gd.coord_nodos[nodo_i][:3]
        coords_j = gd.coord_nodos[nodo_j][:3]

        # detalle para 1 dimension
        if gd.ndim == 1:
            # prop(1,etype(iel)) en MATLAB → gd.prop[0, gd.etype[iel]]
            ei = insertarEiY(fila[0])
            # coord: primera fila coords_i, segunda coords_j
            x1 = coords_i[0]
            x2 = coords_j[0]
            ell = x2 - x1

            # inicializa km_local 4×4
            km_local = np.zeros((4, 4))
            km_local[0, 0] = 12 * ei / (ell ** 3)
            km_local[2, 2] = km_local[0, 0]
            km_local[0, 1] = 6 * ei / (ell ** 2)
            km_local[1, 0] = km_local[0, 1]
            km_local[0, 3] = km_local[0, 1]
            km_local[3, 0] = km_local[0, 3]
            km_local[0, 2] = -km_local[0, 0]
            km_local[2, 0] = km_local[0, 2]
            km_local[2, 3] = -km_local[0, 1]
            km_local[3, 2] = km_local[2, 3]
            km_local[1, 2] = km_local[2, 3]
            km_local[2, 1] = km_local[1, 2]
            km_local[1, 1] = 4 * ei / ell
            km_local[3, 3] = km_local[1, 1]
            km_local[1, 3] = 2 * ei / ell
            km_local[3, 1] = km_local[1, 3]

            km_g.append(km_local)
            completo = np.append(fila, ell)
            elementos.append(completo)

        # detalle para 2 dimensiones
        if gd.ndim == 2:
            ea = insertarEa(fila[0])
            ei = insertarEiY(fila[0])
            x1, y1 = coords_i[0], coords_i[1]
            x2, y2 = coords_j[0], coords_j[1]
            ell = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
            c = (x2 - x1) / ell
            s = (y2 - y1) / ell

            e1 = ea / ell
            e2 = 12 * ei / (ell ** 3)
            e3 = ei / ell
            e4 = 6 * ei / (ell ** 2)

            # inicializa km_local 6×6
            km_local = np.zeros((6, 6))

            km_local[0, 0] = c * c * e1 + s * s * e2
            km_local[3, 3] = km_local[0, 0]

            km_local[0, 1] = s * c * (e1 - e2)
            km_local[1, 0] = km_local[0, 1]
            km_local[3, 4] = km_local[0, 1]
            km_local[4, 3] = km_local[3, 4]

            km_local[0, 2] = -s * e4
            km_local[2, 0] = km_local[0, 2]
            km_local[0, 5] = km_local[0, 2]
            km_local[5, 0] = km_local[0, 5]

            km_local[2, 3] = s * e4
            km_local[3, 2] = km_local[2, 3]
            km_local[3, 5] = km_local[2, 3]
            km_local[5, 3] = km_local[3, 5]

            km_local[0, 3] = -km_local[0, 0]
            km_local[3, 0] = km_local[0, 3]

            km_local[0, 4] = s * c * (-e1 + e2)
            km_local[4, 0] = km_local[0, 4]
            km_local[1, 3] = km_local[0, 4]
            km_local[3, 1] = km_local[1, 3]

            km_local[1, 1] = s * s * e1 + c * c * e2
            km_local[4, 4] = km_local[1, 1]
            km_local[1, 4] = -km_local[1, 1]
            km_local[4, 1] = km_local[1, 4]

            km_local[1, 2] = c * e4
            km_local[2, 1] = km_local[1, 2]
            km_local[1, 5] = km_local[1, 2]
            km_local[5, 1] = km_local[1, 5]

            km_local[2, 2] = 4 * e3
            km_local[5, 5] = km_local[2, 2]

            km_local[2, 4] = -c * e4
            km_local[4, 2] = km_local[2, 4]
            km_local[4, 5] = km_local[2, 4]
            km_local[5, 4] = km_local[4, 5]

            km_local[2, 5] = 2 * e3
            km_local[5, 2] = km_local[2, 5]

            km_g.append(km_local)
            completo = np.append(fila, ell)
            elementos.append(completo)

            # detalle para 3 dimensiones
        if gd.ndim == 3:
            ea = insertarEa(fila[0])
            eiy = insertarEiY(fila[0])
            eiz = insertarEiZ(fila[0])
            gj = insertarG(fila[0])
            x1, y1, z1 = coords_i
            x2, y2, z2 = coords_j

            x1 = x2 - x1
            y1 = y2 - y1
            z1 = z2 - z1

            ell = math.sqrt(x1 * x1 + y1 * y1 + z1 * z1)

            # inicializa km_local y matrices temporales
            km_local = np.zeros((12, 12))
            t = np.zeros((12, 12))
            tt = np.zeros((12, 12))
            cc = np.zeros((12, 12))

            a1 = ea / ell
            a2 = 12 * eiz / (ell ** 3)
            a3 = 12 * eiy / (ell ** 3)
            a4 = 6 * eiz / (ell ** 2)
            a5 = 6 * eiy / (ell ** 2)
            a6 = 4 * eiz / ell
            a7 = 4 * eiy / ell
            a8 = gj / ell

            # --- asignaciones rígidas tal cual en MATLAB ---
            km_local[0, 0] = a1
            km_local[6, 6] = a1
            km_local[0, 6] = -a1
            km_local[6, 0] = -a1

            km_local[1, 1] = a2
            km_local[7, 7] = a2
            km_local[1, 7] = -a2
            km_local[7, 1] = -a2

            km_local[2, 2] = a3
            km_local[8, 8] = a3
            km_local[2, 8] = -a3
            km_local[8, 2] = -a3

            km_local[3, 3] = a8
            km_local[9, 9] = a8
            km_local[3, 9] = -a8
            km_local[9, 3] = -a8

            km_local[4, 4] = a7
            km_local[10, 10] = a7
            km_local[4, 10] = 0.5 * a7
            km_local[10, 4] = 0.5 * a7

            km_local[5, 5] = a6
            km_local[11, 11] = a6
            km_local[5, 11] = 0.5 * a6
            km_local[11, 5] = 0.5 * a6

            km_local[1, 5] = a4
            km_local[5, 1] = a4
            km_local[1, 11] = a4
            km_local[11, 1] = a4

            km_local[5, 7] = -a4
            km_local[7, 5] = -a4
            km_local[7, 11] = -a4
            km_local[11, 7] = -a4

            km_local[4, 8] = a5  # (5,9) en MATLAB es [4,8] en Python
            km_local[8, 4] = a5
            km_local[8, 10] = a5  # (9,11) es [8,10]
            km_local[10, 8] = a5

            km_local[2, 4] = -a5  # (3,5) es [2,4]
            km_local[4, 2] = -a5
            km_local[2, 10] = -a5  # (3,11) es [2,10]
            km_local[10, 2] = -a5

            # --- ahora la transformación con gamma y r0 ---
            gamrad = gd.restricciones[fila[0] - 1][6] * math.pi / 180
            cg = math.cos(gamrad)
            sg = math.sin(gamrad)
            den = ell * math.sqrt(x1 * x1 + z1 * z1)
            r0 = np.zeros((3, 3))
            if den != 0:
                r0[0, 0] = x1 / ell
                r0[0, 1] = y1 / ell
                r0[0, 2] = z1 / ell
                r0[1, 0] = (-x1 * y1 * cg - ell * z1 * sg) / den
                r0[1, 1] = den * cg / (ell * ell)
                r0[1, 2] = (-y1 * z1 * cg + ell * x1 * sg) / den
                r0[2, 0] = (x1 * y1 * sg - ell * z1 * cg) / den
                r0[2, 1] = -den * sg / (ell * ell)
                r0[2, 2] = (y1 * z1 * sg + ell * x1 * cg) / den
            else:
                r0[0, :] = [0, 1, 0]
                r0[1, :] = [-cg, 0, sg]
                r0[2, :] = [sg, 0, cg]

            for i in range(3):
                for j in range(3):
                    x = r0[i, j]
                    for k in range(0, 12, 3):
                        t[i + k, j + k] = x
                        tt[j + k, i + k] = x

            for i in range(12):
                for j in range(12):
                    suma = 0.0
                    for k in range(12):
                        suma += km_local[i, k] * t[k, j]
                    cc[i, j] = suma

            for i in range(12):
                for j in range(12):
                    suma = 0.0
                    for k in range(12):
                        suma += tt[i, k] * cc[k, j]
                    km_local[i, j] = suma

            km_g.append(km_local)
            completo = np.append(fila, ell)
            elementos.append(completo)

    # Ubicación de variables en memoria global:
    gd.elementos = np.array(elementos)
    gd.km_locales = km_g
