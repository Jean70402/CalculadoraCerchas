import math

import numpy as np

import discretizacion.datosGenerales as gd  # Usamos gd
from discretizacion.insertEA import insertarEa, insertarA
from extras.impresion_extra import print_seccion, print_nodos_formato, print_elementos_formato_linea, \
    print_def_unit



def calcular_axiales():
    # define una lista de matriz vacia para elementos y para los km generados:
    axiales = []
    u_locales = []
    longitudes = []

    # Iteración para recuperar valores de elementos y calcular las longitudes
    for idx, fila in enumerate(gd.conexion_elementos):
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
            longitudes.append(ell)
            ea = insertarEa(fila[0])
            ea_L = ea / ell
            #Obtener conexiones para conocer los nodos conectados, según
            # estos, colocar la matriz de rotación correspondiente.
            conex = gd.num[idx]
            # print("conex:", conex)
            u_global = np.zeros((2, 1))

            for i in range(2):
                u_global[i, 0] = gd.u_completa[conex[i], 0]  # asigna valor desde u_completa

            #print("Uglobal:")
            #print(u_global)
            u_local = u_global
            u_locales.append(u_local.copy())
            axial = ea_L * (u_local[1] - u_local[0])
            if abs(axial) < 1e-8:
                axial = 0.0
            else:
                axial = axial.item()
            axiales.append(axial)

        # detalle para 2 dimensiones
        if gd.ndim == 2:
            # Toma de datos de las posiciones de nodos conectados
            x1 = coords_j[0]
            y1 = coords_j[1]
            x2 = coords_i[0]
            y2 = coords_i[1]
            # Cálculo de la longitud
            ell = math.sqrt((x2 - x1) * 2 + (y2 - y1) * 2)
            longitudes.append(ell)
            # Cálculo de senos y cosenos
            cos = (x2 - x1) / ell
            sen = (y2 - y1) / ell
            #matris de rotación para elemento.
            mat_angulo = np.array([
                [cos, sen, 0, 0],
                [0, 0, cos, sen]
            ])
            #print(mat_angulo)
            #Obtener conexiones para conocer los nodos conectados, según
            # estos, colocar la matriz de rotación correspondiente.
            conex = gd.g_g[idx]  # por ejemplo: array([0., 0., 3., 4.])
            conex = conex.astype(int)  # aseguramos enteros para índices

            u_global = np.zeros((2 * gd.ndim, 1))  # inicializa vector columna con ceros

            for i in range(2 * gd.ndim):
                if conex[i] != 0:
                    u_global[i, 0] = gd.u_completa[conex[i] + 1, 0]  # asigna valor desde u_completa
            #print(u_global)
            u_local = mat_angulo @ u_global
            u_locales.append(u_local.copy())
            ea = insertarEa(fila[0])
            ea_L = ea / ell
            axial = ea_L * (u_local[0] - u_local[1])
            if abs(axial) < 1e-8:
                axial = 0.0
                axiales.append(axial)
            else:
                axiales.append(axial.item())

        if gd.ndim == 3:
            # 1) Extraemos nodos i/j

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
            longitudes.append(ell)

            mat_angulo = np.array([
                [xl,yl,zl, 0, 0,0],
                [0, 0,0, xl,yl,zl]
            ])
            nodo_i, nodo_j = gd.num[idx]

            # para cada nodo, sus 3 DOFs consecutivos: [ux,uy,uz]
            nodos = [nodo_i, nodo_j]

            # vamos a llenar un “conexión verdadera” de 6 índices
            conex_true = []
            for n in nodos:
                base = n*3
                # DOF x, y, z
                conex_true += [base+0, base+1, base+2]
            # ahora creamos u_global extrayendo de u_completa
            u_global = np.zeros((6,1))
            for k, dof_glob in enumerate(conex_true):
                # si está libre (gdl_completos[dof_glob]==1) tomamos el valor,
                # si no, dejamos 0
                if gd.gdl_completos[dof_glob] != 0:
                    u_global[k,0] = gd.u_completa[dof_glob,0]
            #print(u_global)

            u_local = mat_angulo @ u_global
            u_locales.append(u_local.copy())
            ea = insertarEa(fila[0])
            ea_L = ea / ell
            axial = ea_L * (u_local[0] - u_local[1])
            if abs(axial) < 1e-8:
                axial = 0.0
                axiales.append(axial)
            else:
                axiales.append(axial.item())

    axiales = np.array(axiales)[:, np.newaxis]
    gd.axiales = axiales
    gd.u_locales = u_locales
    gd.longitudes = np.array(longitudes).reshape(-1, 1)
    print_seccion("Los axiales son (kN): ")
    print_elementos_formato_linea(axiales, gd.nels)
