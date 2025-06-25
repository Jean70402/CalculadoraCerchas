import numpy as np

#Definiciones de backsubstitution y forward substitution para
#resolver el sistema de matrices, definido en banred
#segun cholesky
def backward_substitution_band(L, bw, y):
    n = len(y)
    x = np.zeros_like(y)

    for i in reversed(range(n)):
        s = y[i]
        for k in range(1, min(bw + 1, n - i)):
            if k < L.shape[0]:  # protección adicional
                s -= L[k, i] * x[i + k]
        x[i] = s / L[0, i]
    return x


def forward_substitution_band(L, bw, b):
    n = len(b)
    y = np.zeros_like(b)

    for i in range(n):
        s = b[i]
        for k in range(1, min(bw + 1, i + 1)):
            if k < L.shape[0]:  # protección adicional
                s -= L[k, i - k] * y[i - k]
        y[i] = s / L[0, i]
    return y

# Resolver L.T x = y (L.T es banda superior)
