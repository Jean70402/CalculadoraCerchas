import customtkinter as ctk
import json, os
from json import JSONDecodeError

def _open_properties_window(app):
    """Abre una ventana para generar y guardar propiedades por etype."""
    # Valores por defecto
    defaults = app.default_prop

    # Crear ventana modal
    win = ctk.CTkToplevel(app)
    win.title("Definir Propiedades de Sección")
    win.geometry("400x600")
    win.transient(app)
    win.grab_set()
    win.focus_force()

    # Almacenará los valores ingresados
    props_vars = {}
    for field, val in defaults.items():
        lbl = ctk.CTkLabel(win, text=f"{field}:")
        lbl.pack(anchor="w", padx=10, pady=(10, 0))
        var = ctk.StringVar(value=str(val))
        ent = ctk.CTkEntry(win, textvariable=var)
        ent.pack(fill="x", padx=10, pady=(0, 5))
        props_vars[field] = var

    def _save_props():
        # 1) Lee y convierte los valores de los campos
        raw = {f: v.get() for f, v in props_vars.items()}
        # 2) Separa etype (int) y convierte el resto a float
        try:
            etype = int(raw.pop("etype"))
        except (KeyError, ValueError):
            app._write_console("Error: etype debe ser un entero válido.")
            return

        try:
            data = {f: float(val) for f, val in raw.items()}
        except ValueError:
            app._write_console("Error: todos los campos diferentes a 'etype' deben ser numéricos.")
            return

        # 3) Ruta del JSON
        carpeta = os.path.dirname(__file__)
        ruta = os.path.join(carpeta, "properties.json")

        # 4) Lee contenido (si existe) y maneja JSON vacío o corrupto
        if os.path.isfile(ruta):
            with open(ruta, "r+", encoding="utf-8") as f:
                text = f.read().strip()
                try:
                    allp = json.loads(text) if text else {}
                except JSONDecodeError:
                    allp = {}
                # Actualiza y sobreescribe
                allp[str(etype)] = data
                f.seek(0)
                json.dump(allp, f, indent=2, ensure_ascii=False)
                f.truncate()
        else:
            # Si no existía, crea uno nuevo
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump({str(etype): data}, f, indent=2, ensure_ascii=False)

        app._write_console(f"Propiedades etype={etype} guardadas.")
        win.destroy()

    # Botón de guardar (ya fuera del bucle)
    ctk.CTkButton(win, text="Guardar", command=_save_props).pack(pady=15)
