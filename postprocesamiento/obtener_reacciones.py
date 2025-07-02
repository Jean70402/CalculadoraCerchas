import numpy as np
from numpy import zeros

import discretizacion.datosGenerales as gd
from extras.impresion_extra import print_seccion, print_nodos_formato, print_def_y_giro_extendido


#Armado de kv global, para obtener la matriz kv global
#se asemeja la lógica a formkv, pero tomando en cuenta todos los DOF
def form_kv_global():

    n = len(gd.u_completa)
    bw = len(gd.u_completa)
    rows = bw + 1
    kv = zeros(rows * n)

    for idx in range(len(gd.km_locales)):
        # nodos de elemento
        ni, nj = gd.num[idx]
        ni, nj = int(ni), int(nj)
        # vector de DOFs globales (1-based)
        g = (
                [ni * gd.ndim + d + 1 for d in range(gd.ndim)] +
                [nj * gd.ndim + d + 1 for d in range(gd.ndim)]
        )
        km = gd.km_locales[idx]

        for i in range(2 * gd.ndim):
            for j in range(2 * gd.ndim):
                val_local = km[i][j]
                # desplazamiento en columnas +1
                icd = g[j] - g[i] + 1
                if (icd - 1) >= 0 and (icd - 1) < rows:
                    ival = int(n * (icd - 1) + g[i])
                    kv[ival - 1] += val_local

    gd.kv_global = kv
    #print(kv)
    return kv

#Multiplicación de la matriz en formato de banda con elementos
#Es más sencillo ya que no requiere la transpuesta
def obtenerReacciones():

    # 1) Matriz en banda
    kv = form_kv_global()
    n = len(gd.u_completa)
    bw = len(gd.u_completa)
    rows = bw + 1

    # 2) Multiplicación Kv × u
    u = gd.u_completa
    y = np.zeros_like(u)

    for i in range(n):
        for k in range(rows):
            j = i + k
            if j >= n:
                continue
            kij = kv[k * n + i]
            y[i] += kij * u[j]
            if i != j:
                y[j] += kij * u[i]

    # 3) Reacciones: kv * u - loads
    reacciones = y - gd.loads
    reacciones = np.where(np.abs(reacciones) < 1e-12, 0, np.round(reacciones, 5))

    # 4) Imprimir reacciones
    print_seccion("Las reacciones son (kN):")
    print_def_y_giro_extendido(reacciones, gd.restri)
