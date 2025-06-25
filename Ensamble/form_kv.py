from numpy import zeros

import discretizacion.datosGenerales as gd


def form_kv():
    #Inicializa los valores de uso, el numero de ecuaciones y la banda
    n = int(gd.neq)
    bw = int(gd.nband)
    #El tamaño de banda es +1 para tomar la principal.
    rows = bw + 1
    kv = zeros(rows * n)
    #recorre un contador en las matrices g
    for contador1 in range(len(gd.g_g)):
        g = gd.g_g[contador1, :]
        #Recorre una vez para el valor de i
        for i in range(2 * gd.ndim):
            #El valor no está restringido
            if g[i] != 0:
                #Recorre segunda vez
                for j in range(2 * gd.ndim):
                    #El valor no es 0
                    if g[j] != 0:
                        #Recupera el valor de km segun g
                        val_local = gd.km_locales[contador1][i][j]
                        icd = g[j] - g[i] + 1
                        #Si está en la banda superior, añadir, sino no.
                        if (icd - 1) >= 0:
                            #Asigna la posición del elemento recuperado
                            ival = int(n * (icd - 1) + g[i])
                            #Escribe en kv el valor encontrado
                            kv[ival - 1] += val_local

    # Ajuste final sólo para banda en 1D
    if  gd.ndim == 1 and kv[-1] == 0.0:
        kv = kv[:-1]
    gd.kv = kv
    #print(gd.kv)
