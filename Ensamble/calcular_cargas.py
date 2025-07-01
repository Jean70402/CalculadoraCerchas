import numpy as np
import discretizacion.datosGenerales as gd

def calcular_loads():
    dim = int(gd.restri)   # 1, 2 o 3
    nn  = int(gd.nn)

    # Vector global de cargas (nn x dim)
    cargas_full = np.zeros((nn, dim))
    for fila in gd.loads.values:
        idx = int(fila[0]) - 1          # nodo 1 -> índice 0 (1-based)
        cargas_full[idx, :] = fila[1:1+dim]

    #se utiliza la propiedad flatten de numpy para hacerlo de una sola columna
    loads_col = cargas_full.flatten()[:, np.newaxis]
    gd.loads = loads_col

    # Aplanar nf y usarlo como guía para los DOF
    nf_flat = np.array(gd.nf, dtype=int).flatten()
    # nf_flat[i] == 0 -> DOF restringido; !=0 -> DOF libre

    # Índices de DOF libres
    gdl_libres = [i for i, v in enumerate(nf_flat) if v != 0]

    # Para gdl_completos, usamos directamente los valores de nf_flat
    #    (0 para restringidos, >0 para libres)
    gdl_completos = list(nf_flat)

    # Vector reducido, unicamente segun los gdl_libres
    loads_reducido = loads_col[gdl_libres]

    # Guardar en variables globales
    gd.gdl_completos  = gdl_completos
    gd.loads_reducido = loads_reducido

    #print("Cargas reducidas:")
    #print(gd.loads_reducido)
