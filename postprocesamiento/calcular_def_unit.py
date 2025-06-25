import math

import numpy as np

import discretizacion.datosGenerales as gd  # Usamos gd
from discretizacion.insertEA import insertarEa, insertarA
from extras.impresion_extra import print_seccion, print_def_unit, print_elementos_formato_linea


def def_unit_y_esfuerzo():
    # vectores vacios para deformacion y esfuerzos
    deform_unit = []
    esfuerzos = []

    # Recorremos elementos, segun conexiones
    for idx, fila in enumerate(gd.conexion_elementos):
        # Deformación unitaria ε = (u2 - u1) / L
        u_loc = gd.u_locales[idx]  # array (2×1 en 1D/2D; 6×1 en 3D)
        delta = float(u_loc[-1, 0] - u_loc[0, 0])
        L = float(gd.longitudes[idx, 0])
        eps = delta / L
        deform_unit.append(eps)

        # Esfuerzo σ = N / A
        N = float(gd.axiales[idx])  # fuerza axial [kN]
        A = insertarA(fila[0])  # área [cm²]
        #print(N)
        sigma = N / A
        esfuerzos.append(sigma)

    # Guardar y mostrar
    gd.deform_unit = (np.array(deform_unit).reshape(-1, 1))*-1
    gd.esfuerzo = np.array(esfuerzos).reshape(-1, 1)

    print_seccion("Deformaciones unitarias ε:")
    print_def_unit(gd.deform_unit, gd.nels)

    print_seccion("Esfuerzos σ (kN/cm²):")
    print_elementos_formato_linea(gd.esfuerzo, gd.nels)