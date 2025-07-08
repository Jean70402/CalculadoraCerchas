import os

import customtkinter as ctk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from extras.CustomInterface.properties_window import _open_properties_window
from extras.CustomInterface.restricciones_window import open_restrictions_window
import tkinter.messagebox as mb


class PorticoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Visualizador de Pórticos 1D/2D/3D")
        # Inicia maximizado (Windows)
        self._state_before_windows_set_titlebar_color = 'zoomed'
        self.default_prop = {
            "etype": 1,
            "E": 400000,  # MPa
            "A": 100000,  # cm2
            "Iy": 30000,  # cm4
            "Iz": 300000,  # cm4
            "GJ": 300000,  # GJ
            "Gamma": 0
        }

        # — Consola inferior FIRST so that it always reserve the bottom —
        self.frame_bajo = ctk.CTkFrame(self, height=200, corner_radius=0)
        self.frame_bajo.pack(side="bottom", fill="x", pady=(0, 5))
        self.console = ctk.CTkTextbox(
            self.frame_bajo,
            height=200,
            state="disabled",
            font=("Courier", 12)  # tupla válida
        )
        self.console.pack(fill="both", expand=True, padx=5, pady=5)

        # — Contenedor superior (izq + der) ocupa resto de pantalla —
        top_container = ctk.CTkFrame(self)
        top_container.pack(side="top", fill="both", expand=True, padx=5, pady=(5, 0))

        # Panel izquierdo ampliado
        self.frame_izq = ctk.CTkFrame(top_container, width=600, corner_radius=0)
        self.frame_izq.pack(side="left", fill="y", padx=(0, 5), pady=5)
        self.frame_izq.pack_propagate(False)

        # Panel derecho (gráfico)
        self.frame_der = ctk.CTkFrame(top_container, corner_radius=0)
        self.frame_der.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)

        # — Widgets izquierdo —

        # Dimensión con "puntos"
        ctk.CTkLabel(self.frame_izq, text="Dimensión:").pack(anchor="w", pady=(5, 2))
        self.dim_var = ctk.StringVar(value="3D")
        ctk.CTkSegmentedButton(
            self.frame_izq,
            values=["1D", "2D", "3D"],
            variable=self.dim_var,
            command=self._on_dim_change
        ).pack(fill="x", pady=(0, 15))

        # --- Entradas en filas: coords, fuerzas, momentos ---
        # Marcos auxiliares
        self.coords_frame = ctk.CTkFrame(self.frame_izq)
        self.coords_frame.pack(fill="x", pady=(0, 5))
        self.force_frame = ctk.CTkFrame(self.frame_izq)
        self.force_frame.pack(fill="x", pady=(0, 5))
        self.mom_frame = ctk.CTkFrame(self.frame_izq)
        self.mom_frame.pack(fill="x", pady=(0, 5))

        # Creamos dummies que luego rellenamos en _on_dim_change
        self.entries = {}
        # --- Ahora: creamos cada entry dentro de su propio frame ---
        self.entries = {}
        # Coordenadas en coords_frame
        for key in ["X", "Y", "Z"]:
            e = ctk.CTkEntry(self.coords_frame, placeholder_text="0.0")
            self.entries[key] = e
        # Fuerzas en force_frame
        for key in ["F_x", "F_y", "F_z"]:
            e = ctk.CTkEntry(self.force_frame, placeholder_text="0.0")
            self.entries[key] = e
        # Momentos en mom_frame
        for key in ["M_x", "M_y", "M_z"]:
            e = ctk.CTkEntry(self.mom_frame, placeholder_text="0.0")
            self.entries[key] = e

        # Botones de acciones
        ctk.CTkButton(self.frame_izq, text="Añadir Nodo", command=self._add_nodo) \
            .pack(fill="x", pady=(0, 5))

        ctk.CTkLabel(self.frame_izq, text="Conectar/Borrar nodos:") \
            .pack(anchor="w", pady=(10, 2))
        conn_frame = ctk.CTkFrame(self.frame_izq)
        conn_frame.pack(fill="x", pady=(0, 5))
        self.start_var = ctk.StringVar()
        self.end_var = ctk.StringVar()
        self.mnu_start = ctk.CTkOptionMenu(conn_frame, variable=self.start_var, values=["-"])
        self.mnu_end = ctk.CTkOptionMenu(conn_frame, variable=self.end_var, values=["-"])
        self.mnu_start.pack(side="left", expand=True, padx=2)
        self.mnu_end.pack(side="left", expand=True, padx=2)

        ctk.CTkButton(self.frame_izq, text="Conectar nodos", command=self._conectar) \
            .pack(fill="x", pady=(5, 2))

        # — Selector y botones de Borrar Nodo / Borrar Conexión —
        del_frame = ctk.CTkFrame(self.frame_izq)
        del_frame.pack(fill="x", pady=(5,10))

        # Borrar Nodo (mitad izquierda)
        left = ctk.CTkFrame(del_frame)
        left.pack(side="left", fill="x", expand=True, padx=(0,5))
        ctk.CTkLabel(left, text="Nodo:").pack(anchor="w")
        self.delete_var = ctk.StringVar(value="-")
        self.delete_var = ctk.StringVar(value="-")
        self.mnu_delete = ctk.CTkOptionMenu(
            left,
            variable=self.delete_var,
            values=["-"]
        )
        self.mnu_delete.pack(fill="x")

        ctk.CTkButton(left, text="Borrar Nodo", fg_color="red", command=self._borrar) \
            .pack(fill="x", pady=(5,0))

        # Borrar Conexión (mitad derecha)
        right = ctk.CTkFrame(del_frame)
        right.pack(side="left", fill="x", expand=True, padx=(5,0))
        ctk.CTkLabel(right, text="Conexión:").pack(anchor="w")
        self.delete_conn_var = ctk.StringVar(value="-")
        self.delete_conn_var = ctk.StringVar(value="-")
        self.mnu_delete_conn = ctk.CTkOptionMenu(
            right,
            variable=self.delete_conn_var,
            values=["-"]
        )
        self.mnu_delete_conn.pack(fill="x")

        ctk.CTkButton(right, text="Borrar Conexión", fg_color="red", command=self._borrar_conexion) \
            .pack(fill="x", pady=(5,0))



        # — Botones Generar Propiedades / Generar Restricciones —
        gen_frame = ctk.CTkFrame(self.frame_izq)
        gen_frame.pack(fill="x", pady=(10,5))

        btn_prop = ctk.CTkButton(gen_frame, text="Generar Propiedades",
                                 command=lambda:_open_properties_window(self))
        btn_prop.pack(side="left", fill="x", expand=True, padx=(5,0))

        btn_rest = ctk.CTkButton(gen_frame, text="Generar Restricciones",
                                 command=lambda: open_restrictions_window(self))
        btn_rest.pack(side="left", fill="x", expand=True, padx=(5,0))


        # — Contenedor para scroll y asignación de propiedades —
        bar_control_frame = ctk.CTkFrame(self.frame_izq)
        bar_control_frame.pack(fill="both", expand=False, pady=(5, 0))

        # Scroll con checkboxes de barras
        self.bar_prop_frame = ctk.CTkScrollableFrame(
            bar_control_frame, width=350, height=250, corner_radius=0
        )
        self.bar_prop_frame.pack(side="left", fill="both", expand=True, padx=(0, 0))
        self.bar_checks = {}

        # Controles de asignación de etype
        etype_ctrl = ctk.CTkFrame(bar_control_frame)
        etype_ctrl.pack(side="left", fill="y", padx=(5, 0))

        # Frame interno horizontal para label y entry
        etype_row = ctk.CTkFrame(etype_ctrl)
        etype_row.pack(pady=(2, 2))

        ctk.CTkLabel(etype_row, text="etype:").pack(side="left", padx=(0, 5))
        self.etype_var = ctk.StringVar(value="1")
        etype_entry = ctk.CTkEntry(etype_row, textvariable=self.etype_var, width=60)
        etype_entry.pack(side="left")

        ctk.CTkButton(
            etype_ctrl,
            text="Asignar a seleccionadas",
            command=self._asignar_etype
        ).pack(pady=(5, 5))

        ctk.CTkButton(
            etype_ctrl,
            text="Guardar a Excel",
            command=self._save_to_excel
        ).pack(pady=(5, 10))

        # — Gráfico 3D —
        self.fig = Figure(figsize=(5, 5))
        self.ax = self.fig.add_subplot(111, projection='3d')
        for ax_label in ("X", "Y", "Z"):
            getattr(self.ax, f"set_{ax_label.lower()}label")(ax_label)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_der)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Datos
        self.nodos = []
        self.barras = []
        self.loads = []  # para almacenar [Fx,Fy,Fz,Mx,My,Mz] de cada nodo al crearlo
        self.restrictions = []  # lista de dicts con flags de restricción (por ahora vacíos)

        # Vista inicial
        self._on_dim_change("3D")

    def _asignar_etype(self):
        etype = self.etype_var.get()
        if not etype.isdigit():
            return self._write_console("Error: etype debe ser un número entero.")
        etype = int(etype)

        asignadas = []
        for key, var in self.bar_checks.items():
            if var.get():  # si está seleccionado
                var.set(etype)
                asignadas.append(key)

        if asignadas:
            self._write_console(f"etype={etype} asignado a: {', '.join(asignadas)}")
        else:
            self._write_console("No se seleccionaron barras.")

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
        for ax_label in ("X", "Y", "Z"):
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
            "1D": (["X"], ["F_x"], ["M_x"]),
            "2D": (["X", "Y"], ["F_x", "F_y"], ["M_z"]),
            "3D": (["X", "Y", "Z"], ["F_x", "F_y", "F_z"], ["M_x", "M_y", "M_z"]),
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
        labels = [str(i + 1) for i in range(len(self.nodos))]
        vals = labels if labels else ["-"]

        # Menús de selección de nodo
        for menu in (self.mnu_start, self.mnu_end, self.mnu_delete):
            menu.configure(values=vals)
        self.start_var.set(vals[0])
        self.end_var.set(vals[0])
        self.delete_var.set(vals[0])

        # Menú de conexión a borrar
        conn_values = list(self.bar_checks.keys()) or ["-"]
        self.mnu_delete_conn.configure(values=conn_values)
        self.delete_conn_var.set(conn_values[0])



    def _add_nodo(self):
        # lee sólo X,Y,Z si están en pantalla
        vals = {}
        for k in ("X", "Y", "Z"):
            e = self.entries[k]
            if e.winfo_ismapped():
                try:
                    vals[k] = float(e.get())
                except:
                    vals[k] = 0.0
        x, y, z = vals.get("X", 0), vals.get("Y", 0), vals.get("Z", 0)

        nodo = (x, y, z)
        if nodo in self.nodos:
            return self._write_console(f"Error: el nodo {nodo} ya existe.")
        # Leer cargas/momentos del formulario (cadenas vacías → 0.0)
        load = {}
        for comp in ("F_x", "F_y", "F_z", "M_x", "M_y", "M_z"):
            ent = self.entries[comp]
            if ent.winfo_ismapped():
                val = ent.get().strip()
                try:
                    load[comp] = float(val) if val != "" else 0.0
                except ValueError:
                    load[comp] = 0.0
            else:
                load[comp] = 0.0
        self.loads.append(load)

        self.nodos.append(nodo)
        self.ax.scatter(x, y, z, s=50, depthshade=True)
        self.canvas.draw()
        self._write_console(f"Nodo {len(self.nodos)}: {(x, y, z)}")
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

        # 4) Si está bien, crea y dibuja la barra
        self.barras.append((p1, p2))
        # … después de self.barras.append((p1,p2)) y dibujarla …
        self._write_console(f"Conectada barra {i1}↔{i2}")

        # — Añadir un Checkbutton para esta barra en el scrollable frame —
        key = f"{i1}-{i2}"
        if key not in self.bar_checks:
            # Usamos StringVar en vez de IntVar para aceptar cualquier valor
            var = ctk.StringVar(value=str(self.default_prop["etype"]))
            row_frame = ctk.CTkFrame(self.bar_prop_frame)
            row_frame.pack(fill="x", pady=2, padx=5)

            ctk.CTkCheckBox(row_frame, text=f"{key}", variable=var).pack(side="left")
            ctk.CTkLabel(row_frame, text="etype:").pack(side="left", padx=5)
            ctk.CTkEntry(row_frame, textvariable=var, width=40).pack(side="left")

            self.bar_checks[key] = var
            self._update_node_menus()

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

    def _borrar_conexion(self):
        key = self.delete_conn_var.get()
        if key not in self.bar_checks:
            return self._write_console("Error: seleccione una conexión válida.")

        # 1) Eliminar de self.barras
        i1, i2 = map(int, key.split("-"))
        nodo1 = self.nodos[i1-1]
        nodo2 = self.nodos[i2-1]
        # remueve ambos órdenes si existieran
        if (nodo1, nodo2) in self.barras:
            self.barras.remove((nodo1, nodo2))
        if (nodo2, nodo1) in self.barras:
            self.barras.remove((nodo2, nodo1))

        # 2) Eliminar del diccionario y destruir su frame
        # asumimos que en bar_checks guardaste also row_frame como parte del valor
        # pero si no, busca el frame por texto:
        for child in self.bar_prop_frame.winfo_children():
            if isinstance(child, ctk.CTkFrame):
                # contenido "<CheckBox text>" coincide con key
                if any(isinstance(w, ctk.CTkCheckBox) and w.cget("text")==key
                       for w in child.winfo_children()):
                    child.destroy()
                    break
        del self.bar_checks[key]

        # 3) Redibujar gráfico completo
        self.ax.cla()
        for ax_label in ("X","Y","Z"):
            getattr(self.ax, f"set_{ax_label.lower()}label")(ax_label)
        # nodos
        for x,y,z in self.nodos:
            self.ax.scatter(x,y,z, s=50, depthshade=True)
        # barras restantes
        for p1,p2 in self.barras:
            xs, ys, zs = zip(p1,p2)
            self.ax.plot(xs,ys,zs, linewidth=2)
        self.canvas.draw()

        # 4) Mensaje y refresco de menús
        self._write_console(f"Conexión {key} eliminada.")
        self._update_node_menus()


    def _save_to_excel(self):
        carpeta = os.path.dirname(__file__)
        ruta = os.path.join(carpeta+"/ExcelGenerado", "datos.xlsx")
        try:
            with pd.ExcelWriter(ruta, engine="openpyxl") as writer:
                # 1) Elementos
                elems = []
                for key, var in self.bar_checks.items():
                    etype = var.get()
                    i1, i2 = key.split("-")
                    elems.append({"PROPS": etype, "Nodo inicial": int(i1), "Nodo final": int(i2)})
                pd.DataFrame(elems).to_excel(writer, sheet_name="Elementos", index=False)

                # 2) Nodos Coord
                df_n = pd.DataFrame(self.nodos, columns=["X [m]", "Y [m]", "Z [m]"])
                df_n.to_excel(writer, sheet_name="Nodos Coord", index=False)

                # 3) Datos (dimensión)
                dim_num = int(self.dim_var.get().replace("D", ""))
                pd.DataFrame([{"DIM": dim_num}]).to_excel(writer, sheet_name="Datos", index=False)

                # 4) Props (lee tu JSON guardado)
                props_path = os.path.join(carpeta, "properties.json")
                if os.path.isfile(props_path):
                    props = pd.read_json(props_path, orient="index")
                    props.reset_index(inplace=True)
                    props.rename(columns={"index": "etype"}, inplace=True)
                else:
                    props = pd.DataFrame([self.default_prop]).assign(etype=lambda df: df["etype"])
                cols = ["etype", "E", "A", "Iy", "Iz", "GJ", "Gamma"]
                props[cols].to_excel(writer, sheet_name="Props", index=False)

                # 5) Nodos Loads
                loads = []
                for idx, ld in enumerate(self.loads, start=1):
                    if any(ld[c] != 0 for c in ld):
                        row = {"NODO": idx}
                        row.update({k: ld[k] if k in ld else 0 for k in ("F_x", "F_y", "F_z", "M_x", "M_y", "M_z")})
                        loads.append(row)
                pd.DataFrame(loads).to_excel(writer, sheet_name="Nodos Loads", index=False)

                # 6) Restricciones
                restr = []
                for idx, flags in enumerate(self.restrictions, start=1):
                    # flags es un dict {"vx": IntVar, "vy": IntVar, ...}
                    row = {"NODO": idx}
                    for comp, var in flags.items():
                        # extrae el 0/1 real del IntVar
                        row[comp] = 0 if var.get() == 1 else 1
                    restr.append(row)
                pd.DataFrame(restr).to_excel(writer, sheet_name="Restricciones", index=False)
            self._write_console(f"Datos exportados a Excel en:\n  {ruta}")
        except PermissionError:
            mb.showerror(
                "Error al guardar",
                "No se pudo guardar el archivo.\n"
                "Por favor cierre el Excel y vuelva a intentarlo."
            )
        except Exception as e:
            mb.showerror(
                "Error inesperado",
                f"Ocurrió un error al guardar:\n{e}"
            )

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    PorticoApp().mainloop()
