import discretizacion.datosGenerales as gd


def insertarEa(prop):
    e = gd.props[prop - 1][1]
    a = gd.props[prop - 1][2]
    ea = e*a
    return ea
    #ADVERTENCIA: "MODIFICAR ESTO DAÑA TODO EL PROGRAMA "
    #return ea*100

def insertarEiY(prop):
    e = gd.props[prop - 1][1]
    iy = gd.props[prop - 1][3]
    eiy = e*iy
    return eiy

def insertarEiZ(prop):
    e = gd.props[prop - 1][1]
    iz = gd.props[prop - 1][4]
    eiz = e*iz
    return eiz

def insertarG(prop):
    e = gd.props[prop - 1][1]
    poisson = gd.props[prop - 1][5]
    G = e/(2*(1+poisson))
    return G

def insertarA(prop):
    a = gd.props[prop - 1][2]
    return a
