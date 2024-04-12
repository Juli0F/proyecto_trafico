import tkinter as tk
from tkinter import filedialog
from models.street_system import StreetSystem
from gui.edge_properties_window import EdgePropertiesWindow
from gui.node_properties_window import NodePropertiesWindow
import time

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Optimización de tráfico")
        self.geometry("800x600")

        self.street_system = StreetSystem()
        self.mode = "add_node"
        self.edge_start = None
        self.last_click_time = 0
        self.click_delay = 300
        self.create_menu()
        self.create_canvas()


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


    def create_canvas(self):
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def new_system(self):
        self.street_system = StreetSystem()
        self.canvas.delete("all")

    def save_system(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json")
        if file_path:
            self.street_system.save(file_path)

    def load_system(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            self.street_system.load(file_path)
            self.draw_system()

    def draw_system(self):
        self.canvas.delete("all")

        for node in self.street_system.get_nodes():
            x = node['x']
            y = node['y']
            node_id = node['node_id']
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="white", outline="black")
            self.canvas.create_text(x, y, text=str(node_id))

        for edge in self.street_system.get_edges():
            source_node = next(node for node in self.street_system.get_nodes() if node['node_id'] == edge['source_node'])
            target_node = next(node for node in self.street_system.get_nodes() if node['node_id'] == edge['target_node'])
            x1, y1 = source_node['x'], source_node['y']
            x2, y2 = target_node['x'], target_node['y']
            self.canvas.create_line(x1, y1, x2, y2, arrow="last")

    def on_canvas_click(self, event):
        current_click_time = int(round(time.time() * 1000))
        if (current_click_time - self.last_click_time) < self.click_delay:
            # Es un doble clic
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
        self.canvas.create_line(self.edge_start[0], self.edge_start[1], event.x, event.y, tags="edge_preview")

    def on_canvas_release(self, event):
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Button-1>")
        self.canvas.delete("edge_preview")
        source_node = self.find_nearest_node(self.edge_start[0], self.edge_start[1])
        target_node = self.find_nearest_node(event.x, event.y)
        if source_node and target_node:
            edge_id = len(self.street_system.get_edges()) + 1
            edge = {'edge_id': edge_id, 'source_node': source_node['node_id'], 'target_node': target_node['node_id'],
                    'direction': 'uni', 'capacity': 0}
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
