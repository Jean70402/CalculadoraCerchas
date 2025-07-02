import discretizacion.datosGenerales as gd  # Usamos gd


def subrutina_form_nf():
    gd.neq = 0
    gd.restri = len(gd.restricciones[0])-1
    columnas_a_borrar = []
    if gd.ndim == 1 and gd.cer_por==1:
        columnas_a_borrar = [1, 3, 4, 5]
    elif gd.ndim == 2 and gd.cer_por==1:
        columnas_a_borrar = [3, 4, 5]

    if gd.cer_por==0:
        columnas_a_borrar = [4, 5, 6]
        if gd.ndim == 1:
            columnas_a_borrar += [2, 3]
        elif gd.ndim == 2:
            columnas_a_borrar += [3]

    for fila in gd.restricciones:
        for i in sorted(columnas_a_borrar, reverse = True):
            del fila[i]


    for i in range(gd.nn):  # Recorre cada nodo
        for j in range(gd.restri):  # Recorre x, y, z según ndim
            es_restringido = False

            # Busca en las restricciones si hay coincidencia
            for r in gd.restricciones:
                nodo = int(r[0])
                if nodo == i + 1 and int(r[j + 1]) == 0:
                    es_restringido = True
                    break  # ya no es necesario seguir buscando

            if not es_restringido:
                gd.neq += 1
                gd.nf[i, j] = gd.neq
            # si está restringido, queda como 0
    #print("nf:")
    #print(gd.nf)
