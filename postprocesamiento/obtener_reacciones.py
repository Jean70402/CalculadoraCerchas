import numpy as np
from numpy import zeros

import discretizacion.datosGenerales as gd
from extras.impresion_extra import print_seccion, \
    print_def_y_giro_reaccion


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
                [ni * gd.restri + d + 1 for d in range(gd.restri)] +
                [nj * gd.restri + d + 1 for d in range(gd.restri)]
        )
        km = gd.km_locales[idx]

        for i in range(2 * gd.restri):
            for j in range(2 * gd.restri):
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
    print_def_y_giro_reaccion(reacciones, gd.restri,gd.ndim)

def obtenerAccionesInternas():

    r     = gd.restri                  # DOF por nodo (2D→3, 3D→6)
    ndof  = 2 * r                       # DOF totales por elemento
    nels  = gd.nels                     # número de elementos
    def_u = gd.mat_def_u.flatten()      # vector de deformaciones activas

    # Inicializo un array para guardar TODAS las acciones
    matrizReacciones = np.zeros((ndof, nels))

    for idx in range(nels):
        # 1) Extraer eld (deformaciones del elemento) vía g_g
        eld = np.zeros((ndof, 1))
        g   = gd.g_g[idx].astype(int)   # g_g fila (1-based para def_u)
        for i in range(ndof):
            if g[i] != 0:
                eld[i, 0] = def_u[g[i] - 1]

        # 2) Calcular acciones locales
        k_loc = gd.km_locales[idx]      # (ndof×ndof)
        f_loc = k_loc @ eld             # (ndof×1)

        # 3) Redondear y cero y casi ceros
        f_loc = np.where(np.abs(f_loc) < 1e-12, 0, np.round(f_loc, 7))

        # 4) Guardar en la matriz completa
        matrizReacciones[:, idx] = f_loc.flatten()

        # 5) Imprimir para este elemento
        print_seccion(f"Acciones internas — elemento {idx+1}:")
        print(f_loc.flatten(), "\n")
