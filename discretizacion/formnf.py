import numpy as np

import discretizacion.datosGenerales as gd  # Usamos gd


def subrutina_form_nf():
    gd.neq = 0

    for i in range(gd.nn):  # Recorre cada nodo
        for j in range(gd.ndim):  # Recorre x, y, z según ndim
            es_restringido = False

            # Busca en las restricciones si hay coincidencia
            for r in gd.restricciones:
                nodo = int(r[0])
                if nodo == i + 1 and int(r[j + 1]) == 1:
                    es_restringido = True
                    break  # ya no es necesario seguir buscando

            if not es_restringido:
                gd.neq += 1
                gd.nf[i, j] = gd.neq
            # si está restringido, queda como 0

    print(gd.nf)
