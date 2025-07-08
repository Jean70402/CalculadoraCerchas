import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class PorticoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Visualizador de Pórticos 1D/2D/3D")
        # Inicia maximizado (Windows)
        self.state('zoomed')

        # — Consola inferior FIRST so that it always reserve the bottom —
        self.frame_bajo = ctk.CTkFrame(self, height=200, corner_radius=0)
        self.frame_bajo.pack(side="bottom", fill="x", pady=(0,5))
        self.console = ctk.CTkTextbox(
            self.frame_bajo,
            height=200,
            state="disabled",
            font=("Courier", 12)          # tupla válida
        )
        self.console.pack(fill="both", expand=True, padx=5, pady=5)

        # — Contenedor superior (izq + der) ocupa resto de pantalla —
        top_container = ctk.CTkFrame(self)
        top_container.pack(side="top", fill="both", expand=True, padx=5, pady=(5,0))

        # Panel izquierdo ampliado
        self.frame_izq = ctk.CTkFrame(top_container, width=600, corner_radius=0)
        self.frame_izq.pack(side="left", fill="y", padx=(0,5), pady=5)
        self.frame_izq.pack_propagate(False)

        # Panel derecho (gráfico)
        self.frame_der = ctk.CTkFrame(top_container, corner_radius=0)
        self.frame_der.pack(side="left", fill="both", expand=True, padx=(5,0), pady=5)

        # — Widgets izquierdo —

        # Dimensión con "puntos"
        ctk.CTkLabel(self.frame_izq, text="Dimensión:").pack(anchor="w", pady=(10,2))
        self.dim_var = ctk.StringVar(value="3D")
        ctk.CTkSegmentedButton(
            self.frame_izq,
            values=["1D","2D","3D"],
            variable=self.dim_var,
            command=self._on_dim_change
        ).pack(fill="x", pady=(0,15))

        # --- Entradas en filas: coords, fuerzas, momentos ---
        # Marcos auxiliares
        self.coords_frame = ctk.CTkFrame(self.frame_izq)
        self.coords_frame.pack(fill="x", pady=(0,5))
        self.force_frame  = ctk.CTkFrame(self.frame_izq)
        self.force_frame.pack(fill="x", pady=(0,5))
        self.mom_frame    = ctk.CTkFrame(self.frame_izq)
        self.mom_frame.pack(fill="x", pady=(0,5))

        # Creamos dummies que luego rellenamos en _on_dim_change
        self.entries = {}
        # --- Ahora: creamos cada entry dentro de su propio frame ---
        self.entries = {}
        # Coordenadas en coords_frame
        for key in ["X","Y","Z"]:
            e = ctk.CTkEntry(self.coords_frame, placeholder_text="0.0")
            self.entries[key] = e
        # Fuerzas en force_frame
        for key in ["F_x","F_y","F_z"]:
            e = ctk.CTkEntry(self.force_frame, placeholder_text="0.0")
            self.entries[key] = e
        # Momentos en mom_frame
        for key in ["M_x","M_y","M_z"]:
            e = ctk.CTkEntry(self.mom_frame, placeholder_text="0.0")
            self.entries[key] = e


        # Botones de acciones
        ctk.CTkButton(self.frame_izq, text="Añadir Nodo", command=self._add_nodo) \
            .pack(fill="x", pady=(20,5))

        ctk.CTkLabel(self.frame_izq, text="Conectar/Borrar nodos:") \
            .pack(anchor="w", pady=(10,2))
        conn_frame = ctk.CTkFrame(self.frame_izq)
        conn_frame.pack(fill="x", pady=(0,5))
        self.start_var = ctk.StringVar()
        self.end_var   = ctk.StringVar()
        self.mnu_start = ctk.CTkOptionMenu(conn_frame, variable=self.start_var, values=["-"])
        self.mnu_end   = ctk.CTkOptionMenu(conn_frame, variable=self.end_var,   values=["-"])
        self.mnu_start.pack(side="left", expand=True, padx=2)
        self.mnu_end.pack(side="left",   expand=True, padx=2)

        ctk.CTkButton(self.frame_izq, text="Conectar", command=self._conectar) \
            .pack(fill="x", pady=(5,2))

        # Selector para borrar
        self.delete_var = ctk.StringVar()
        self.mnu_delete = ctk.CTkOptionMenu(
            self.frame_izq,
            variable=self.delete_var,
            values=["-"],
            width=80
        )
        self.mnu_delete.pack(fill="x", pady=(5,10))

        ctk.CTkButton(
            self.frame_izq,
            text="Borrar Nodo",
            fg_color="red",
            command=self._borrar
        ).pack(fill="x")


    # — Gráfico 3D —
        self.fig = Figure(figsize=(5,5))
        self.ax  = self.fig.add_subplot(111, projection='3d')
        for ax_label in ("X","Y","Z"):
            getattr(self.ax, f"set_{ax_label.lower()}label")(ax_label)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_der)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Datos
        self.nodos = []
        self.barras = []

        # Vista inicial
        self._on_dim_change("3D")

    def _write_console(self, txt):
        self.console.configure(state="normal")
        self.console.insert("end", txt + "\n")
        self.console.see("end")
        self.console.configure(state="disabled")
    def _on_dim_change(self, dim):
        # 1) Limpia datos y gráfico
        self.nodos.clear()
        self.barras.clear()
        self.ax.cla()
        for ax_label in ("X","Y","Z"):
            getattr(self.ax, f"set_{ax_label.lower()}label")(ax_label)
        self.canvas.draw()

        # 2) Limpia consola
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        self.console.configure(state="disabled")

        # 3) Oculta (pack_forget) todas las Entry existentes
        for ent in self.entries.values():
            ent.pack_forget()

        # 4) Elimina SOLO las Labels que habíamos creado dinámicamente
        for frame in (self.coords_frame, self.force_frame, self.mom_frame):
            for w in frame.winfo_children():
                if isinstance(w, ctk.CTkLabel):
                    w.destroy()

        # 5) Empaqueta solo los grupos que toque
        mapping = {
            "1D": (["X"],        ["F_x"],       ["M_x"]),
            "2D": (["X","Y"],    ["F_x","F_y"], ["M_z"]),
            "3D": (["X","Y","Z"],["F_x","F_y","F_z"], ["M_x","M_y","M_z"]),
        }
        co, fo, mo = mapping[dim]

        # Coordenadas en una fila
        for key in co:
            lbl = ctk.CTkLabel(self.coords_frame, text=f"{key}:")
            lbl.pack(side="left", expand=True, padx=2)
            ent = self.entries[key]
            ent.pack(in_=self.coords_frame, side="left", expand=True, padx=2)

        # Fuerzas en la siguiente fila
        for key in fo:
            lbl = ctk.CTkLabel(self.force_frame, text=f"{key}:")
            lbl.pack(side="left", expand=True, padx=2)
            ent = self.entries[key]
            ent.pack(in_=self.force_frame, side="left", expand=True, padx=2)

        # Momentos en la fila de abajo
        for key in mo:
            lbl = ctk.CTkLabel(self.mom_frame, text=f"{key}:")
            lbl.pack(side="left", expand=True, padx=2)
            ent = self.entries[key]
            ent.pack(in_=self.mom_frame, side="left", expand=True, padx=2)

        # 6) Resetea menús de nodos
        self._update_node_menus()


    def _update_node_menus(self):
        labels = [str(i+1) for i in range(len(self.nodos))]
        vals = labels if labels else ["-"]

        for menu in (self.mnu_start, self.mnu_end, self.mnu_delete):
            menu.configure(values=vals)
        # reinicia seleccionados
        self.start_var.set(vals[0])
        self.end_var.set(vals[0])
        self.delete_var.set(vals[0])


    def _add_nodo(self):
        # lee sólo X,Y,Z si están en pantalla
        vals = {}
        for k in ("X","Y","Z"):
            e = self.entries[k]
            if e.winfo_ismapped():
                try: vals[k] = float(e.get())
                except: vals[k] = 0.0
        x,y,z = vals.get("X",0), vals.get("Y",0), vals.get("Z",0)

        nodo = (x, y, z)
        if nodo in self.nodos:
            return self._write_console(f"Error: el nodo {nodo} ya existe.")
        self.nodos.append(nodo)
        self.ax.scatter(x,y,z, s=50, depthshade=True); self.canvas.draw()
        self._write_console(f"Nodo {len(self.nodos)}: {(x,y,z)}")
        self._update_node_menus()

    def _conectar(self):
        # Obtiene índices de inicio y fin
        i1 = self.start_var.get()
        i2 = self.end_var.get()

        # 1) Validación básica: deben ser dígitos distintos
        if not (i1.isdigit() and i2.isdigit()):
            return self._write_console("Error: seleccione dos nodos válidos.")
        if i1 == i2:
            return self._write_console("Error: no se puede conectar un nodo consigo mismo.")

        # 2) Convierte a enteros y obtiene las coordenadas
        idx1, idx2 = int(i1) - 1, int(i2) - 1
        # Asegura que los índices estén dentro de rango
        if idx1 < 0 or idx2 < 0 or idx1 >= len(self.nodos) or idx2 >= len(self.nodos):
            return self._write_console("Error: índice de nodo fuera de rango.")

        p1 = self.nodos[idx1]
        p2 = self.nodos[idx2]

        # 3) Previene barras duplicadas (considera ambos órdenes)
        if (p1, p2) in self.barras or (p2, p1) in self.barras:
            return self._write_console(f"Error: la barra {i1}↔{i2} ya existe.")

        # 4) Si todo está bien, crea y dibuja la barra
        self.barras.append((p1, p2))
        xs, ys, zs = zip(p1, p2)
        self.ax.plot(xs, ys, zs, linewidth=2)
        self.canvas.draw()
        self._write_console(f"Conectada barra {i1}↔{i2}")



    def _borrar(self):
        # Obtiene el índice de nodo a borrar desde el selector delete_var
        idx_str = self.delete_var.get()
        if not idx_str.isdigit():
            return self._write_console("Error: seleccione un nodo válido para borrar.")
        idx = int(idx_str) - 1
        # Saca el nodo de la lista y guarda sus coordenadas
        nodo = self.nodos.pop(idx)

        # Redibuja el gráfico: limpia y vuelve a dibujar ejes, nodos y barras existentes
        self.ax.cla()
        # Restaurar etiquetas de ejes
        for ax_label in ("X", "Y", "Z"):
            getattr(self.ax, f"set_{ax_label.lower()}label")(ax_label)
        # Dibujar nodos restantes
        for x, y, z in self.nodos:
            self.ax.scatter(x, y, z, s=50, depthshade=True)
        # Dibujar barras que aún conecten nodos existentes
        nuevas_barras = []
        for p1, p2 in self.barras:
            if p1 in self.nodos and p2 in self.nodos:
                xs, ys, zs = zip(p1, p2)
                self.ax.plot(xs, ys, zs, linewidth=2)
                nuevas_barras.append((p1, p2))
        # Actualizar lista interna de barras
        self.barras = nuevas_barras

        # Refrescar canvas
        self.canvas.draw()

        # Log en consola
        self._write_console(f"Nodo {idx_str} {nodo} eliminado.")

        # Actualizar todos los menús de nodos (start, end, delete)
        self._update_node_menus()


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    PorticoApp().mainloop()
