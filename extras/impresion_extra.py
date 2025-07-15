
def print_seccion(titulo):
    ancho = 80
    print("\n" + "=" * ancho)
    print(titulo.center(ancho))
    print("=" * ancho + "\n")


def print_nodos_formato(matriz, ndim):
    etiquetas = ['x', 'y', 'z'][:ndim]
    matriz = matriz.flatten()

    for i in range(0, len(matriz), ndim):
        linea = "      "
        for j in range(ndim):
            linea += f"         {etiquetas[j]}{(i//ndim)+1} = {matriz[i+j]:.5f}           "
        print(linea)
    print()
def print_def_y_giro_extendido(matriz, dof, ndim):

    valores = matriz.flatten()
    n_nodos = len(valores) // dof

    # Labels según ndim
    if ndim == 1:
        labels_disp = ['dy']
        labels_rot  = ['θz']
    elif ndim == 2:
        labels_disp = ['dx', 'dy']
        # solo hay rotación en z si dof == 3
        labels_rot  = ['θz'] if dof == 3 else []
    else:
        labels_disp = ['dx', 'dy', 'dz']
        # tantas rotaciones como dof extra sobre los 3 desplazamientos
        n_rot = max(0, dof - 3)
        labels_rot  = ['θx', 'θy', 'θz'][:n_rot]

    for n in range(n_nodos):
        base = n * dof
        # línea de desplazamientos
        linea_disp = "      "
        for i, et in enumerate(labels_disp):
            linea_disp += f"{et}{n+1} = {valores[base + i]:.5f}    "
        print(linea_disp)

        # línea de rotaciones, si las hay
        if labels_rot:
            linea_rot = "      "
            for j, et in enumerate(labels_rot):
                val = valores[base + len(labels_disp) + j]
                linea_rot += f"{et}{n+1} = {val:.5f}    "
            print(linea_rot)

    print()


def print_def_y_giro_reaccion(matriz, dof, ndim):

    valores = matriz.flatten()
    n_nodos = len(valores) // dof

    # Labels según ndim
    if ndim == 1:
        labels_force  = ['Rx']
        labels_moment = ['Ry']
    elif ndim == 2:
        labels_force  = ['Rx', 'Ry']
        # momento solo en z si dof == 3
        labels_moment = ['Mz'] if dof == 3 else []
    else:
        labels_force  = ['Rx', 'Ry', 'Rz']
        # tantos momentos como dof extra sobre los 3 fuerzas
        n_mom = max(0, dof - 3)
        labels_moment = ['Mx', 'My', 'Mz'][:n_mom]

    for n in range(n_nodos):
        base = n * dof
        # línea de fuerzas
        linea_f = "      "
        for i, et in enumerate(labels_force):
            linea_f += f"{et}{n+1} = {valores[base + i]:.5f}    "
        print(linea_f)

        # línea de momentos, si los hay
        if labels_moment:
            linea_m = "      "
            for j, et in enumerate(labels_moment):
                val = valores[base + len(labels_force) + j]
                linea_m += f"{et}{n+1} = {val:.5f}    "
            print(linea_m)

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
