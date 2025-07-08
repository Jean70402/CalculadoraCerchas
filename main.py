from Ensamble.calcular_cargas import calcular_loads
from Ensamble.form_kv import form_kv
from Ensamble.pin_jointed import pin_jointed
from Ensamble.rigid_jointed import rigid_jointed
from discretizacion.formnf import subrutina_form_nf
from discretizacion.lecturaDatos import leer_datos_desde_excel
from discretizacion.num_to_g import subrutina_num_to_g_g
from postprocesamiento.calcular_axiales import calcular_axiales
from postprocesamiento.calcular_def_unit import def_unit_y_esfuerzo
from postprocesamiento.deformacion_completa import obtener_mat_def_completa
from postprocesamiento.obtener_reacciones import obtenerReacciones, obtenerAccionesInternas
from postprocesamiento.rigid_calcular_axiales import rigid_calcular_axiales
from resolucion.banred import subrutina_banred
import discretizacion.datosGenerales as gd

def main():
    #print("Escriba [0] para Cercha o [1] para pórtico:")
    #gd.cer_por=input()

    leer_datos_desde_excel()
    subrutina_form_nf()
    subrutina_num_to_g_g()
    rigid_jointed()
    #pin_jointed()
    form_kv()
    calcular_loads()
    subrutina_banred()
    obtener_mat_def_completa()
    #calcular_axiales()
    rigid_calcular_axiales()
    obtenerReacciones()
    def_unit_y_esfuerzo()
    obtenerAccionesInternas()
if __name__ == "__main__":
    main()