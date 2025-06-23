import numpy as np
import discretizacion.datosGenerales as gd

def calcular_loads():
    dim = int(gd.ndim)   # 1, 2 o 3
    nn  = int(gd.nn)

    # 1) Vector global de cargas (nn x dim)
    cargas_full = np.zeros((nn, dim))
    for fila in gd.loads.values:
        idx = int(fila[0]) - 1          # nodo 1→índice 0
        cargas_full[idx, :] = fila[1:1+dim]

    loads_col = cargas_full.flatten()[:, np.newaxis]
    gd.loads = loads_col

    # 2) Aplanar nf y usarlo como máscara
    nf_flat = np.array(gd.nf, dtype=int).flatten()
    # nf_flat[i] == 0 → DOF restringido; !=0 → DOF libre

    # 3) Índices de DOF libres
    gdl_libres = [i for i, v in enumerate(nf_flat) if v != 0]

    # 4) Para gdl_completos, usamos directamente los valores de nf_flat
    #    (0 para restringidos, >0 para libres)
    gdl_completos = list(nf_flat)

    # 5) Vector reducido
    loads_reducido = loads_col[gdl_libres]

    # 6) Guardar y mostrar
    gd.gdl_completos  = gdl_completos
    gd.loads_reducido = loads_reducido

    print("Cargas reducidas:")
    print(gd.loads_reducido)
