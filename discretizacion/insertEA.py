import discretizacion.datosGenerales as gd


def insertarEa(prop):
    e = gd.props[prop - 1][1]
    a = gd.props[prop - 1][2]
    ea = e*a
    return ea
    #ADVERTENCIA: "MODIFICAR ESTO DAÑA TODO EL PROGRAMA "
    #return ea*100


def insertarA(prop):
    a = gd.props[prop - 1][2]
    return a
