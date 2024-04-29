import tkinter as tk


class EdgePropertiesWindow(tk.Toplevel):
    def __init__(self, parent, edge):
        super().__init__(parent)
        self.parent = parent
        self.edge = edge
        self.title(f"Propiedades de la arista {edge['edge_id']}")

        # Variables existentes
        self.direction = tk.StringVar(value=edge.get('direction', ''))
        print("Direccion:", edge.get('direction', ''))
        print("Source:", edge.get('source_node', ''))
        print("Target:", edge.get('target_node', ''))

        self.capacity = tk.IntVar(value=edge.get('capacity', 0))
        self.capacity_min = tk.IntVar(value=edge.get('capacity_min', 0))


        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self)
        main_frame.pack(padx=10, pady=10)

        # Campos existentes
        direction_label = tk.Label(main_frame, text="Dirección:")
        direction_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        direction_entry = tk.Entry(main_frame, textvariable=self.direction)
        direction_entry.grid(row=0, column=1, padx=5, pady=5)

        capacity_label = tk.Label(main_frame, text="Capacidad:")
        capacity_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        capacity_entry = tk.Entry(main_frame, textvariable=self.capacity)
        capacity_entry.grid(row=1, column=1, padx=5, pady=5)

        capacity_label = tk.Label(main_frame, text="Capacidad minima:")
        capacity_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        capacity_entry = tk.Entry(main_frame, textvariable=self.capacity_min)
        capacity_entry.grid(row=2, column=1, padx=5, pady=5)

        save_button = tk.Button(main_frame, text="Guardar", command=self.save_properties)
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

    def save_properties(self):
        self.edge['direction'] = self.direction.get()
        self.edge['capacity'] = self.capacity.get()
        self.edge['capacity_min'] = self.capacity_min.get()

        self.parent.draw_system()
        self.destroy()
