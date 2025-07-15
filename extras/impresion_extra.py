
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
    """
    Imprime desplazamientos (dx, dy, dz) y rotaciones (θx, θy, θz)
    sólo para los dof activos.
    `dof` = gd.restri, `ndim` = gd.ndim.
    """
    valores = matriz.flatten()
    n_nodos = len(valores) // dof

    # cuántos disp vs rot
    disp_count = min(ndim, dof)
    rot_count  = dof - disp_count

    labels_disp = ['dx', 'dy', 'dz'][:disp_count]
    labels_rot  = ['θx', 'θy', 'θz'][:rot_count]

    for n in range(n_nodos):
        base = n * dof
        # línea de desplazamientos
        linea_disp = "      "
        for i, et in enumerate(labels_disp):
            linea_disp += f"{et}{n+1} = {valores[base + i]:.5f}    "
        print(linea_disp)

        # línea de rotaciones (si hay)
        if rot_count:
            linea_rot = "      "
            for j, et in enumerate(labels_rot):
                val = valores[base + disp_count + j]
                linea_rot += f"{et}{n+1} = {val:.5f}    "
            print(linea_rot)

    print()


def print_def_y_giro_reaccion(matriz, dof, ndim):
    """
    Imprime reacciones de fuerza (Rx, Ry, Rz) y momento (Mx, My, Mz)
    sólo para los dof activos.
    """
    valores = matriz.flatten()
    n_nodos = len(valores) // dof

    disp_count = min(ndim, dof)
    rot_count  = dof - disp_count

    labels_force = ['Rx', 'Ry', 'Rz'][:disp_count]
    labels_moment= ['Mx', 'My', 'Mz'][:rot_count]

    for n in range(n_nodos):
        base = n * dof
        # línea de fuerzas
        linea_f = "      "
        for i, et in enumerate(labels_force):
            linea_f += f"{et}{n+1} = {valores[base + i]:.5f}    "
        print(linea_f)

        # línea de momentos (si hay)
        if rot_count:
            linea_m = "      "
            for j, et in enumerate(labels_moment):
                val = valores[base + disp_count + j]
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
