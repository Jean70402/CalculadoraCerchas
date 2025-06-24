from numpy import zeros

import discretizacion.datosGenerales as gd


def form_kv():
    n = int(gd.neq)
    bw = int(gd.nband)
    rows = bw + 1
    kv = zeros(rows * n)

    for contador1 in range(len(gd.g_g)):
        g = gd.g_g[contador1, :]
        for i in range(2 * gd.ndim):
            if g[i] != 0:
                for j in range(2 * gd.ndim):
                    if g[j] != 0:
                        val_local = gd.km_locales[contador1][i][j]


                        icd = g[j] - g[i] + 1
                        if (icd - 1) >= 0:
                            ival = int(n * (icd - 1) + g[i])
                            kv[ival - 1] += val_local

    # Ajuste final sólo para banda en 1D
    if  gd.ndim == 1 and kv[-1] == 0.0:
        kv = kv[:-1]
    gd.kv = kv
    #print(gd.kv)
