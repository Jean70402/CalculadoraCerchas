import math
import numpy as np
import discretizacion.datosGenerales as gd
from discretizacion.insertEA import insertarEa
from extras.impresion_extra import print_seccion, print_elementos_formato_linea

def rigid_calcular_axiales():
    axiales = []
    u_locales = []
    longitudes = []

    for idx, fila in enumerate(gd.conexion_elementos):
        nodo_i = fila[1]
        nodo_j = fila[2]
        coords_i = gd.coord_nodos[nodo_i][:3]
        coords_j = gd.coord_nodos[nodo_j][:3]

        # --- 1D ---
        if gd.ndim == 1:
            x1 = coords_i[0]
            x2 = coords_j[0]
            ell = abs(x2 - x1)
            longitudes.append(ell)
            ea = insertarEa(fila[0])
            ea_L = ea / ell

            conex = gd.num[idx]  # [dofi, dofj]
            u_global = np.array([
                gd.u_completa[conex[0], 0],
                gd.u_completa[conex[1], 0]
            ]).reshape(2, 1)

            u_local = u_global
            u_locales.append(u_local.copy())
            axial = ea_L * (u_local[1] - u_local[0])
            axiales.append(0.0 if abs(axial) < 1e-8 else axial.item())

        # --- 2D ---
        elif gd.ndim == 2:
            x1, y1 = coords_i[0], coords_i[1]
            x2, y2 = coords_j[0], coords_j[1]
            dx, dy = x2 - x1, y2 - y1
            ell = math.sqrt(dx ** 2 + dy ** 2)
            longitudes.append(ell)

            cos, sen = dx / ell, dy / ell
            T = np.array([
                [cos, sen, 0, 0],
                [0, 0, cos, sen]
            ])

            conex = gd.g_g[idx].astype(int)  # DOFs globales
            u_global = np.zeros((4, 1))
            for i in range(4):
                if conex[i] != 0:
                    u_global[i, 0] = gd.u_completa[conex[i] + 1, 0]

            u_local = T @ u_global
            u_locales.append(u_local.copy())
            ea = insertarEa(fila[0])
            ea_L = ea / ell
            axial = ea_L * (u_local[0] - u_local[1])
            axiales.append(0.0 if abs(axial) < 1e-8 else axial.item())

        # --- 3D ---
        elif gd.ndim == 3:
            x1, y1, z1 = coords_i
            x2, y2, z2 = coords_j
            dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
            ell = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
            longitudes.append(ell)

            lx, ly, lz = dx / ell, dy / ell, dz / ell
            T = np.array([
                [lx, ly, lz, 0, 0, 0],
                [0, 0, 0, lx, ly, lz]
            ])

            nodo_i, nodo_j = gd.num[idx]
            dofs_i = [nodo_i * 6 + i for i in range(3)]  # ux, uy, uz
            dofs_j = [nodo_j * 6 + i for i in range(3)]
            dofs = dofs_i + dofs_j

            u_global = np.zeros((6, 1))
            for i, dof in enumerate(dofs):
                if gd.gdl_completos[dof] != 0:
                    u_global[i, 0] = gd.u_completa[dof, 0]

            u_local = T @ u_global
            u_locales.append(u_local.copy())
            ea = insertarEa(fila[0])
            ea_L = ea / ell
            axial = ea_L * (u_local[0] - u_local[1])
            axiales.append(0.0 if abs(axial) < 1e-8 else axial.item())

    # Almacenamiento en gd
    gd.axiales = np.array(axiales)[:, np.newaxis]
    gd.u_locales = u_locales
    gd.longitudes = np.array(longitudes).reshape(-1, 1)

    # Impresión
    print_seccion("Los axiales son (kN): ")
    print_elementos_formato_linea(gd.axiales, gd.nels)
