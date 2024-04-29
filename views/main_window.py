import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import time

from models.Type import Type
from models.config import SIZE_OVAL, SIZE_EDGE, COLOR_IN, COLOR_OUT, COLOR_NORMAL, SIZE_ARROW
from views.dialog import Dialog
from views.genetic_algorithm_settings_window import GeneticAlgorithmSettingsWindow
from models.street_system import StreetSystem
from views.edge_properties_window import EdgePropertiesWindow
from views.node_properties_window import NodePropertiesWindow

from controller.algorithm_controller import AlgorithmController



class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Optimización de tráfico")
        self.geometry("1000x600")
        self.node_items = {}
        self.street_system = StreetSystem()
        self.mode = "add_node"
        self.edge_start = None
        self.last_click_time = 0
        self.click_delay = 300
        self.node_menu = tk.Menu(self, tearoff=0)
        self.create_widgets()
        self.create_data_table()
        self.dialogo = None#Dialog(self)

        self.population_size = 0
        self.mutation_rate = 0
        self.num_generation = 0
        self.target_fitness = 0



    def create_widgets(self):
        self.create_menu()
        self.create_canvas()
        self.create_context_menu()
        self.create_analyze_button()

    def create_context_menu(self):
        self.node_menu.add_command(label="Eliminar nodo", command=self.delete_node)
        self.node_menu.add_command(label="Mover nodo", command=self.move_node)
        self.node_menu.add_command(label="Marcar como nodo de entrada", command=self.mark_as_entry_node)
        self.node_menu.add_command(label="Marcar como nodo de salida", command=self.mark_as_exit_node)


    def show_context_menu(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item)
        if "node" in tags:
            self.selected_node = item
            try:
                self.node_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.node_menu.grab_release()
        else:
            self.selected_node = None

    def create_analyze_button(self):
        analyze_button = tk.Button(self, text="Analizar", command=self.analyze)
        analyze_button.pack(side='top', pady=20)

    def analyze(self):
        if self.population_size == 0 or self.mutation_rate == 0 or self.num_generation == 0 or self.target_fitness == 0:
            messagebox.showinfo( "Informacion", "Debe ingresar una configuracion")
            return;

        controller = AlgorithmController()
        controller.convert(self.street_system)
    def delete_node(self):
        if self.selected_node:
            node_id = self.node_items.get(self.selected_node)
            if node_id:
                self.street_system.remove_node(int(node_id))
                self.canvas.delete(self.selected_node)
                for item, item_node_id in self.node_items.items():
                    if item_node_id == node_id:
                        self.canvas.delete(item)
                self.node_items = {k: v for k, v in self.node_items.items() if v != node_id}
                self.draw_system()
                print(f"Nodo {node_id} eliminado")

    def move_node(self):
        if self.selected_node:
            node_id = self.node_items.get(self.selected_node)
            if node_id:
                oval_item = None
                text_item = None
                for item, item_node_id in self.node_items.items():
                    if item_node_id == node_id:
                        if self.canvas.type(item) == "oval":
                            oval_item = item
                        elif self.canvas.type(item) == "text":
                            text_item = item
                if oval_item and text_item:
                    self.canvas.bind("<B1-Motion>", lambda event: self.drag_node(event, node_id, oval_item, text_item))
                    self.canvas.bind("<ButtonRelease-1>", self.drop_node)

    def drag_node(self, event, node_id, oval_item, text_item):
        node = next((node for node in self.street_system.nodes if node['node_id'] == int(node_id)), None)
        if node:
            node['x'] = event.x
            node['y'] = event.y
            self.canvas.coords(oval_item, event.x - 20, event.y - 20, event.x + 20, event.y + 20)
            self.canvas.coords(text_item, event.x, event.y)
            self.draw_system()

    def drop_node(self, event):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def create_data_table(self):
        self.data_frame = ttk.Frame(self)
        self.data_frame.pack(side='right', fill='y', expand=False)

        self.tree = ttk.Treeview(self.data_frame, columns=('ID', 'Tipo', 'Tiempo'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Tipo', text='Tipo')
        self.tree.heading('Tiempo', text='Tiempo o  Capacidad')
        self.tree.pack(side='top', fill='both', expand=True)

        update_button = tk.Button(self.data_frame, text="Actualizar Datos", command=self.update_data_table)
        update_button.pack(side='bottom', pady=10)

    def update_data_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for node in self.street_system.nodes:
            if 'node_id' in node and 'min_time_percentage' in node:
                self.tree.insert('', 'end', values=(node['node_id'], 'Nodo', node['min_time_percentage']))

        for edge in self.street_system.edges:
            if 'edge_id' in edge and 'capacity' in edge:
                self.tree.insert('', 'end', values=(edge['edge_id'], 'Arista', edge['capacity']))
                print("edge:",edge)

    def add_edge(self, start_node, end_node, time):
        edge = {'id': len(self.street_system.edges) + 1, 'start_node': start_node, 'end_node': end_node, 'time': time}
        self.street_system.edges.append(edge)
        print("Arista añadida:", edge)

    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Nuevo", command=self.new_system)
        file_menu.add_command(label="Guardar", command=self.save_system)
        file_menu.add_command(label="Cargar", command=self.load_system)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.quit)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Agregar nodo", command=self.set_mode_add_node)
        edit_menu.add_command(label="Agregar arista", command=self.set_mode_add_edge)
        menu_bar.add_cascade(label="Editar", menu=edit_menu)

        settings_menu = tk.Menu(menu_bar, tearoff=0)
        settings_menu.add_command(label="Configuración del Algoritmo Genético",
                                  command=self.open_genetic_algorithm_settings)
        menu_bar.add_cascade(label="Configuración", menu=settings_menu)

    def open_genetic_algorithm_settings(self):
        settings_ag = GeneticAlgorithmSettingsWindow(self)
        settings_ag.grab_set()
        self.population_size = settings_ag.population_size
        self.mutation_rate = settings_ag.mutation_rate
        self.num_generation = settings_ag.num_generations
        self.target_fitness = settings_ag.target_fitness

    def create_canvas(self):
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind("<Button-3>", self.show_context_menu)  # Botón derecho del ratón

    def new_system(self):
        self.street_system = StreetSystem()
        self.canvas.delete("all")

    def save_system(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json")
        if file_path:
            self.street_system.save(file_path)

    def draw_system(self):
        self.canvas.delete("all")
        self.node_items = {}

        for node in self.street_system.get_nodes():
            x = node['x']
            y = node['y']
            node_id = node['node_id']
            node_type = node.get('node_type', None)
            color = COLOR_IN if node_type == Type.ENTRADA else COLOR_OUT if node_type == Type.SALIDA else COLOR_NORMAL
            oval_item = self.canvas.create_oval(x - SIZE_OVAL, y - SIZE_OVAL, x + SIZE_OVAL, y + SIZE_OVAL, fill=color, outline="black",
                                                tags=("node", str(node_id)))
            text_item = self.canvas.create_text(x , y, text=str(node_id), tags=("node", str(node_id)))
            self.node_items[oval_item] = node_id
            self.node_items[text_item] = node_id

        for edge in self.street_system.get_edges():
            source_node = next(
                node for node in self.street_system.get_nodes() if node['node_id'] == edge['source_node'])
            target_node = next(
                node for node in self.street_system.get_nodes() if node['node_id'] == edge['target_node'])
            x1, y1 = source_node['x'], source_node['y']
            x2, y2 = target_node['x'], target_node['y']
            self.canvas.create_line(x1, y1, x2, y2, arrow="last", width=SIZE_EDGE, arrowshape=SIZE_ARROW)

    def load_system(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            self.street_system.load(file_path)
            self.draw_system()

    def on_canvas_click(self, event):
        current_click_time = int(round(time.time() * 1000))
        if (current_click_time - self.last_click_time) < self.click_delay:
            self.handle_double_click(event)
        else:
            self.after(self.click_delay, self.handle_single_click, event, current_click_time)
        self.last_click_time = current_click_time

    def handle_single_click(self, event, click_time):
        if (click_time == self.last_click_time):
            if self.mode == "add_node":
                node_id = len(self.street_system.get_nodes()) + 1
                node = {'node_id': node_id, 'x': event.x, 'y': event.y}
                self.street_system.add_node(node)
                self.draw_system()
            elif self.mode == "add_edge":
                self.edge_start = (event.x, event.y)
                self.canvas.bind("<Motion>", self.on_canvas_move)
                self.canvas.bind("<Button-1>", self.on_canvas_release)

    def handle_double_click(self, event):
        if self.mode == "add_node":
            self.on_node_double_click(event)
        else:
            self.on_edge_double_click(event)

    def on_canvas_move(self, event):
        self.canvas.delete("edge_preview")
        self.canvas.create_line(self.edge_start[0], self.edge_start[1], event.x, event.y, tags="edge_preview", width=SIZE_EDGE, arrowshape=SIZE_ARROW)

    def on_canvas_release(self, event):
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Button-1>")
        self.canvas.delete("edge_preview")
        source_node = self.find_nearest_node(self.edge_start[0], self.edge_start[1])
        target_node = self.find_nearest_node(event.x, event.y)
        if source_node and target_node:
            edge_id = len(self.street_system.get_edges()) + 1
            edge = {'edge_id': edge_id, 'source_node': source_node['node_id'], 'target_node': target_node['node_id'],
                    'direction': str(source_node['node_id']) + " -> "+ str(target_node['node_id']), 'capacity': 0}
            self.street_system.add_edge(edge)
            self.draw_system()
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def find_nearest_node(self, x, y):
        nodes = self.street_system.get_nodes()
        if nodes:
            nearest_node = min(nodes, key=lambda node: (node['x'] - x) ** 2 + (node['y'] - y) ** 2)
            return nearest_node
        return None

    def set_mode_add_node(self):
        self.mode = "add_node"

    def set_mode_add_edge(self):
        self.mode = "add_edge"

    def on_node_double_click(self, event):
        node = self.find_nearest_node(event.x, event.y)
        if node:
            self.show_node_properties_window(node)

    def on_edge_double_click(self, event):
        edge = self.find_nearest_edge(event.x, event.y)
        print("edge", edge)
        if edge:
            self.show_edge_properties_window(edge)

    def find_nearest_edge(self, x, y):
        edges = self.street_system.get_edges()
        if edges:
            nearest_edge = min(edges, key=lambda edge: self.distance_to_edge(edge, x, y))
            if self.distance_to_edge(nearest_edge, x, y) <= 10:
                return nearest_edge
        return None

    def distance_to_edge(self, edge, x, y):
        source_node = next(node for node in self.street_system.get_nodes() if node['node_id'] == edge['source_node'])
        target_node = next(node for node in self.street_system.get_nodes() if node['node_id'] == edge['target_node'])
        x1, y1 = source_node['x'], source_node['y']
        x2, y2 = target_node['x'], target_node['y']
        numerator = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
        denominator = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
        if denominator != 0:
            return numerator / denominator
        return float('inf')

    def show_node_properties_window(self, node):
        node_properties_window = NodePropertiesWindow(self, node)
        node_properties_window.grab_set()

    def show_edge_properties_window(self, edge):
        edge_properties_window = EdgePropertiesWindow(self, edge)
        edge_properties_window.grab_set()

    def mark_as_entry_node(self):
        node_id = self.canvas.gettags(self.selected_node)[1]
        self.street_system.update_node_type(node_id, Type.ENTRADA)
        self.canvas.itemconfig(self.selected_node, fill=COLOR_IN)

    def mark_as_exit_node(self):
        node_id = self.canvas.gettags(self.selected_node)[1]
        self.street_system.update_node_type(node_id, Type.SALIDA)
        self.canvas.itemconfig(self.selected_node, fill=COLOR_OUT)

