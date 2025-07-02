
def print_seccion(titulo):
    ancho = 80
    print("\n" + "=" * ancho)
    print(titulo.center(ancho))
    print("=" * ancho + "\n")

import numpy as np

def print_nodos_formato(matriz, ndim):
    etiquetas = ['x', 'y', 'z'][:ndim]
    matriz = matriz.flatten()

    for i in range(0, len(matriz), ndim):
        linea = "      "
        for j in range(ndim):
            linea += f"         {etiquetas[j]}{(i//ndim)+1} = {matriz[i+j]:.5f}           "
        print(linea)
    print()

def print_def_y_giro_extendido(matriz, dof=6):

    etiquetas_disp = ['dx', 'dy', 'dz']
    etiquetas_rot  = ['θx', 'θy', 'θz']
    valores = matriz.flatten()

    n_nodos = len(valores) // dof
    for n in range(n_nodos):
        base = n * dof
        # Desplazamientos
        linea1 = "      "
        for i, et in enumerate(etiquetas_disp):
            linea1 += f"{et}{n+1} = {valores[base + i]:.5f}    "
        # Rotaciones
        linea2 = "      "
        for i, et in enumerate(etiquetas_rot, start=3):
            linea2 += f"{et}{n+1} = {valores[base + i]:.5f}    "

        print(linea1)
        print(linea2)
    print()



def print_elementos_formato_linea(matriz, nels):
    matriz = matriz.flatten()

    for i in range(nels):
        print(f"                          Barra {i + 1}   =   {matriz[i]:.5f}")

def print_def_unit(matriz, nels):
    matriz = matriz.flatten()

    for i in range(nels):
        print(f"                          Deformacion {i + 1}   =   {matriz[i]:.10f}")

def print_seccion_titulo(titulo):
    ancho = 100
    decorador = "═"
    borde = f"{decorador * ancho}"
    titulo_centrado = f"╡ {titulo} ╞".center(ancho, " ")

    print("\n" + borde)
    print(titulo_centrado)
    print(borde + "\n")
