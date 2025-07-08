import customtkinter as ctk
def _open_properties_window(app):
    """Abre una ventana para generar y guardar propiedades por etype."""
    # Valores por defecto
    defaults = app.default_prop
    # Crear ventana modal
    win = ctk.CTkToplevel(app)
    win.title("Definir Propiedades de Sección")
    win.geometry("400x600")
    win.transient(app)      # vincula la modal a la ventana principal
    win.grab_set()           # impide interactuar con la principal hasta cerrar esta
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
        # Convierte tipos
        data = {f: (int(v.get()) if f == "etype" else float(v.get()))
                for f, v in props_vars.items()}
        # Guarda en JSON
        import json, os
        carpeta = os.path.dirname(__file__)
        ruta = os.path.join(carpeta, "properties.json")
        # Si ya existe, leemos y añadimos
        if os.path.isfile(ruta):
            with open(ruta, "r+") as f:
                allp = json.load(f)
                allp[str(data["etype"])] = data
                f.seek(0)
                json.dump(allp, f, indent=2)
                f.truncate()
        else:
            with open(ruta, "w") as f:
                json.dump({str(data["etype"]): data}, f, indent=2)
        app._write_console(f"Propiedades etype={data['etype']} guardadas.")
        win.destroy()

    # Botón de guardar
    ctk.CTkButton(win, text="Guardar", command=_save_props) \
        .pack(pady=15)
