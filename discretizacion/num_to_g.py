import numpy as np

import discretizacion.datosGenerales as gd  # Usamos gd


def subrutina_num_to_g_g():
    # Transforma en un array el inf_elementos para analizarlo
    # mediante numpy, para obtener la conectividad de los elementos
    gd.conexion_elementos = np.array(gd.conexion_elementos)
    gd.num = gd.conexion_elementos[:, [1, 2]]

    # Inicializar matriz g_g
    gd.g_g = np.zeros((gd.nels, gd.restri*2))

    # Con nf y num se hace una doble iteración anidada, para tomar los grados de libertad
    # de nf y los asigne segun num
    for i in range(gd.nels):
        # Toma los valores de num
        num_i = gd.num[i, 0]
        num_j = gd.num[i, 1]
        for j in range(gd.restri):
            # asigna a las columnas dependiendo de la dimension los valores de nf segun num
            # En 2d, primero se asigna el valor de columna 1, luego 3, luego 2, luego 4.
            gd.g_g[i, j] = gd.nf[num_i, j]
            gd.g_g[i, j + gd.restri] = gd.nf[num_j, j]

        # Diferencia los valores de 0 encontrados en num_to_g
        no_ceros = gd.g_g[i][gd.g_g[i] != 0]
        # Para valores mayores a 0 en num_to_g haya el
        # valor máximo para el nband, de manera iterativa.
        if no_ceros.size > 0:
            nband_new = (no_ceros.max() - no_ceros.min() + 1)
            if nband_new > gd.nband:
                gd.nband = nband_new
    print(gd.num)
    print(gd.g_g)