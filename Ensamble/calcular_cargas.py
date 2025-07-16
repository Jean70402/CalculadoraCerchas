import numpy as np
import discretizacion.datosGenerales as gd


def calcular_loads():
    #Toma en consideración la eliminación de columnas, igual que en la lectura de datos.
    #Se eliminan en base a las restricciones, definidas anteriormente.
    if gd.ndim == 1 and gd.cer_por == 1:
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

    dim = int(gd.restri)
    nn = int(gd.nn)

    cargas_full = np.zeros((nn, dim))

    for fila in gd.loads.values:
        row = fila.tolist()  # [nodo, Fx, Fy, Fz, Mx, My, Mz]
        for i in sorted(cols_a_borrar, reverse=True):
            del row[i]
        idx = int(row[0]) - 1
        cargas_full[idx, :] = row[1:1 + dim]

    #print("cargas_full:\n", cargas_full)

    #  Aplano a vector columna y sobreescribo gd.loads
    loads_col = cargas_full.flatten()[:, np.newaxis]
    gd.loads = loads_col

    #  Aplanar nf para saber qué DOF están libres
    nf_flat = np.array(gd.nf, dtype=int).flatten()
    gdl_libres = [i for i, v in enumerate(nf_flat) if v != 0]
    gdl_completos = list(nf_flat)

    #  Extraer sólo los libres
    loads_reducido = loads_col[gdl_libres]

    #  Guardar en globals
    gd.gdl_completos = gdl_completos
    gd.loads_reducido = loads_reducido

# print("Cargas reducidas:\n", gd.loads_reducido)
