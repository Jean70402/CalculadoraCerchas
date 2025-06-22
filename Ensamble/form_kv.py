from numpy import zeros

import discretizacion.datosGenerales as gd


def form_kv(full_matrix=False):
    n = int(gd.neq)
    bw = int(gd.nband)
    # Si pedimos matriz completa, la inicializamos n×n;
    # si no, el vector banda
    if full_matrix:
        kv = zeros((n, n))
    else:
        rows = bw + 1
        kv = zeros(rows * n)

    for contador1 in range(len(gd.g_g)):
        g = gd.g_g[contador1, :]
        for i in range(2 * gd.ndim):
            if g[i] != 0:
                for j in range(2 * gd.ndim):
                    if g[j] != 0:
                        val_local = gd.km_locales[contador1][i][j]
                        if full_matrix:
                            # Índices de fila y columna en la matriz completa
                            fila = int(g[i]) - 1
                            col = int(g[j]) - 1
                            kv[fila, col] += val_local
                        else:
                            # Mismo código banda de antes
                            icd = g[j] - g[i] + 1
                            if (icd - 1) >= 0:
                                ival = int(n * (icd - 1) + g[i])
                                kv[ival - 1] += val_local

    # Ajuste final sólo para banda en 1D
    if (not full_matrix) and gd.ndim == 1 and kv[-1] == 0.0:
        kv = kv[:-1]

    # Guardamos en gd.kv; si necesitas también la completa,
    # podrías usar gd.K_full = kv cuando full_matrix=True
    gd.kv = kv
    print(gd.kv)
