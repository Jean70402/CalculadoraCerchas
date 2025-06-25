import numpy as np

import discretizacion.datosGenerales as gd
from resolucion.backsub import backward_substitution_band, forward_substitution_band


def subrutina_banred():

    n = gd.neq
    bk = np.array(gd.kv)
    # filas = número real de diagonales almacenadas
    rows = bk.size // n
    # ancho de banda efectivo
    bw_eff = rows - 1

    # sólo tomo esa porción útil
    bk_band = bk[: rows * n]
    bk_ordenado = bk_band.reshape(rows, n)

    L = cholesky_band(bk_ordenado, bw_eff)
    b = gd.loads_reducido.flatten()
    y = forward_substitution_band(L, bw_eff, b)
    x = backward_substitution_band(L, bw_eff, y)
    gd.mat_def_u = x.reshape(-1, 1)
    result_cm = np.round(gd.mat_def_u * 100, 5)
    #print("Deformaciones (cm): \n", result_cm)


'''
Se utiliza la teoría de cholesky para resolver matrices en formato de banda
simétricas positivas, se busca una matriz L tal que:
L*L^T=A
siendo A la matriz bandeada simétrica

Forward substitution
Encuentra un "y" tal que L*y=b
donde b es la matriz que se quiere multiplicar para obtener el resultado
entonces b es la matriz de fuerzas reducidas

Backward substitution
Se resuelve el sistema de multiplicación con la inversa
se busca un x tal que L^T*x=y

con el "y" identificado de forward y la L^T del primer paso de hallar L
Se resuelve el sistema y da de resultado la deformación

'''
def cholesky_band(band, bw):
    n = band.shape[1]
    L = np.zeros_like(band)
    for j in range(n):
        sum_diag = 0.0
        for k in range(1, bw + 1):
            if j - k < 0 or k >= band.shape[0]:
                break
            sum_diag += L[k, j - k] ** 2
        L[0, j] = np.sqrt(band[0, j] - sum_diag)

        for i in range(1, bw + 1):
            if j + i >= n or i >= band.shape[0]:
                break
            sum_off = 0.0
            for k in range(1, bw - i + 1):
                if j - k < 0 or j + i - k < 0 or (k + i) >= band.shape[0] or k >= band.shape[0]:
                    break
                sum_off += L[k, j - k] * L[k + i, j - k]
            L[i, j] = (band[i, j] - sum_off) / L[0, j]
    return L
