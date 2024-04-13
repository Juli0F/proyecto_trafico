import tkinter as tk


class NodePropertiesWindow(tk.Toplevel):
    def __init__(self, parent, node):
        super().__init__(parent)
        self.parent = parent
        self.node = node
        self.title(f"Propiedades del nodo {node['node_id']}")

        self.traffic_light_timings = node.get('traffic_light_timings', {})
        self.min_time_percentage = tk.DoubleVar(value=node.get('min_time_percentage', 0.0))

        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self)
        main_frame.pack(padx=10, pady=10)

        min_time_label = tk.Label(main_frame, text="Porcentaje mínimo de tiempo para semáforos:")
        min_time_label.pack(padx=5, pady=5)
        min_time_entry = tk.Entry(main_frame, textvariable=self.min_time_percentage)
        min_time_entry.pack(padx=5, pady=5)

        self.entry_frame = tk.Frame(main_frame)
        self.entry_frame.pack(padx=5, pady=5)
        self.entries = []
        for i, (edge_id, timing) in enumerate(self.traffic_light_timings.items(), start=1):
            edge_label = tk.Label(self.entry_frame, text=f"Arista {edge_id}: ")
            edge_label.grid(row=i, column=0, padx=5, pady=5)

            entry = tk.Entry(self.entry_frame)
            entry.insert(0, timing)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries.append((edge_id, entry))

        save_button = tk.Button(main_frame, text="Guardar", command=self.save_properties)
        save_button.pack(pady=10)

    def save_properties(self):
        for edge_id, entry in self.entries:
            self.traffic_light_timings[edge_id] = entry.get()

        self.node['traffic_light_timings'] = self.traffic_light_timings
        self.node['min_time_percentage'] = self.min_time_percentage.get()

        self.parent.draw_system()
        self.destroy()
