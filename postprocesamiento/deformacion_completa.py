import numpy as np

import discretizacion.datosGenerales as gd  # Usamos gd
from extras.impresion_extra import print_seccion, print_def_y_giro_extendido


#Función para encontrar la matriz de deformación completa, añadiendo
#ceros en los gdl.
def obtener_mat_def_completa():
    u = gd.mat_def_u  # vector columna con las deformaciones activas
    u_completa = []

    # Contador para recorrer el vector u (solo los gdl activos)
    contador_u = 0
    #Bucle para colocar valores de 0 en la matriz de deformaciones
    #En los grados de libertad restringidos.
    for gdl in gd.gdl_completos:
        if gdl == 0:
            u_completa.append(0.0)
        else:
            u_completa.append(u[contador_u, 0])
            contador_u += 1

    # Convertimos a array columna
    print_seccion("Las deformaciones (cm) son:")
    gd.u_completa = np.array(u_completa).reshape(-1, 1)
    result_cm = np.round(gd.u_completa * 100, 5)
    #print_nodos_formato(result_cm, gd.ndim)
    print_def_y_giro_extendido(result_cm, gd.restri,gd.restri)
