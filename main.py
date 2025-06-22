from Ensamble.pin_jointed import pin_jointed
from discretizacion.formnf import subrutina_form_nf
from discretizacion.lecturaDatos import leer_datos_desde_excel
from discretizacion.num_to_g import subrutina_num_to_g_g


def main():
    leer_datos_desde_excel()
    subrutina_form_nf()
    subrutina_num_to_g_g()
    pin_jointed()

if __name__ == "__main__":
    main()