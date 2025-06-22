import numpy as np
import discretizacion.datosGenerales as gd

def calcular_loads():
    dim = gd.ndim        # 1, 2 o 3
    nn = gd.nn           # número total de nodos

    # DataFrame con columnas [NODO, carga1, carga2, ... carga_dim]
    loads_df = gd.loads

    # 1) Inicializa todo en cero
    cargas = np.zeros((nn, dim), float)

    # 2) Índices (0-based) y valores de carga extraídos de loads_df
    nodos   = loads_df['NODO'].astype(int).to_numpy() - 1
    valores = loads_df.iloc[:, 1:1+dim].to_numpy().astype(float)

    # 3) Asigna en bloque
    cargas[nodos, :] = valores

    # 4) Vector global
    gd.loads = cargas.flatten()[:, None]

    # 5) GDL completos y libres (igual que antes)
    gdl_completos = [
        (i*dim + j) if gd.coord_nodos[i][j] == 1 else 0
        for i in range(nn)
        for j in range(dim)
    ]
    gd.gdl_completos = gdl_completos
    gd.gdl_libres = [g for g in gdl_completos if g != 0]

    # 6) Vector reducido: sólo las cargas que vienen en el Excel
    gd.loads_reducido = valores.flatten()[:, None]

    # --- Salida de comprobación ---
    print("\nVector global de cargas (completo):")
    print(gd.loads)
    print("\nVector de cargas reducido (sólo nodos cargados):")
    print(gd.loads_reducido)
