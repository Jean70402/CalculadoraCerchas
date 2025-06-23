import numpy as np
import discretizacion.datosGenerales as gd
from extras.impresion_extra import print_seccion, print_nodos_formato


def form_global():
    total_dof = gd.nn * gd.ndim
    K = np.zeros((total_dof, total_dof))

    for idx in range(len(gd.km_locales)):
        # en lugar de inf_elementos, tomo la conexión de num
        ni, nj = gd.num[idx]              # ej: [2, 4]
        ni = int(ni)
        nj = int(nj)

        # armo la lista de DOFs físicos
        phys = (
                [ni * gd.ndim + d for d in range(gd.ndim)] +
                [nj * gd.ndim + d for d in range(gd.ndim)]
        )

        km = gd.km_locales[idx]           # 2*ndim × 2*ndim

        # ensamblado incondicional
        for a in range(2 * gd.ndim):
            for b in range(2 * gd.ndim):
                K[phys[a], phys[b]] += km[a][b]

    gd.kg = K
    print(gd.kg)

def obtenerReacciones():
    form_global()

    reacciones = (gd.kg @ gd.u_completa) - gd.loads

    # Redondear a 2 decimales y eliminar residuos numéricos cercanos a cero
    reacciones = np.where(np.abs(reacciones) < 1e-12, 0, np.round(reacciones, 5))
    print_seccion("Las reacciones son (kN):")
    print_nodos_formato(reacciones, gd.ndim)
