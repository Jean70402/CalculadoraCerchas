import customtkinter as ctk
def open_restrictions_window(app):
    # ahora “app” es tu PorticoApp, con app.nodos y app.restrictions disponibles
    win = ctk.CTkToplevel(app)
    win.title("Definir Restricciones")
    win.geometry("700x300")
    win.transient(app)      # vincula la modal a la ventana principal
    win.grab_set()           # impide interactuar con la principal hasta cerrar esta
    win.focus_force()        # fuerza el foco en la modal

# para cada nodo en app.nodos (funciona porque solo se llama tras init)
    for idx, _ in enumerate(app.nodos, start=1):
        row = ctk.CTkFrame(win)
        row.pack(fill="x", pady=2, padx=5)
        ctk.CTkLabel(row, text=f"Nodo {idx}").pack(side="left", padx=(0,5))
        flags = {}
        for comp in ("vx","vy","vz","θx","θy","θz"):
            var = ctk.IntVar(value=0)
            chk = ctk.CTkCheckBox(row, text=comp, variable=var, onvalue=1, offvalue=0)
            # oculta según dimensión
            dim = app.dim_var.get()
            if (dim=="1D" and comp not in ("vy","θz")) or \
                    (dim=="2D" and comp not in ("vx","vy","θz")):
                # no pack → queda con valor 1 en app.restrictions
                pass
            else:
                chk.pack(side="left", padx=2)
            flags[comp] = var
        # asegura que app.restrictions tenga entradas previas
        if idx-1 < len(app.restrictions):
            app.restrictions[idx-1] = flags
        else:
            app.restrictions.append(flags)

    def _save_restr():
        app._write_console("Restricciones definidas.")
        win.destroy()

    ctk.CTkButton(win, text="Guardar", command=_save_restr).pack(pady=10)