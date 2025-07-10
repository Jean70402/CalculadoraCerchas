import numpy as np
import discretizacion.datosGenerales as gd

def calcular_loads():
    # 0) Determinar qué DOF “muertos” hay (igual que en subrutina_form_nf)
    if   gd.ndim == 1 and gd.cer_por == 1:
        cols_a_borrar = [1, 3, 4, 5]
    elif gd.ndim == 2 and gd.cer_por == 1:
        cols_a_borrar = [3, 4, 5]
    elif gd.cer_por == 0:
        cols_a_borrar = [3, 4, 5]
        if gd.ndim == 1:
            cols_a_borrar += [1, 2]
        elif gd.ndim == 2:
            cols_a_borrar += [2]
    else:
        cols_a_borrar = []

    # 1) Dimensión efectiva (1,2 ó 3 en 3D será 6)
    dim = int(gd.restri)
    nn  = int(gd.nn)

    # 2) Preparo cargas_full con la dimensión “reducida”
    cargas_full = np.zeros((nn, dim))

    # 3) Recorro el DataFrame original, quito columas muertas y lleno cargas_full
    for fila in gd.loads.values:
        row = fila.tolist()           # [nodo, Fx, Fy, Fz, Mx, My, Mz]
        for i in sorted(cols_a_borrar, reverse=True):
            del row[i]                # elimino exactamente la columna i
        idx = int(row[0]) - 1         # nodo → índice 0-based
        cargas_full[idx, :] = row[1:1+dim]

    print("cargas_full:\n", cargas_full)

    # 4) Aplano a vector columna y sobreescribo gd.loads (igual que antes)
    loads_col = cargas_full.flatten()[:, np.newaxis]
    gd.loads  = loads_col

    # 5) Aplanar nf para saber qué DOF están libres
    nf_flat     = np.array(gd.nf, dtype=int).flatten()
    gdl_libres  = [i for i, v in enumerate(nf_flat) if v != 0]
    gdl_completos = list(nf_flat)

    # 6) Extraer sólo los libres
    loads_reducido = loads_col[gdl_libres]

    # 7) Guardar en globals (igual que antes)
    gd.gdl_completos  = gdl_completos
    gd.loads_reducido = loads_reducido

    print("Cargas reducidas:\n", gd.loads_reducido)
