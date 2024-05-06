import tkinter as tk
from tkinter import ttk


class ResultsWindow(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)
        self.title("Resultados del Análisis de Tráfico")
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("desde", "hacia", "porcentaje_tiempo", "vehiculos"),
                                 show="headings")
        self.tree.heading("desde", text="Desde Nodo")
        self.tree.heading("hacia", text="Hacia Nodo")
        self.tree.heading("porcentaje_tiempo", text="Porcentaje de Tiempo")
        self.tree.heading("vehiculos", text="Vehículos")
        self.tree.pack(expand=True, fill="both")

    def mostrar_resultados(self, resultados):
        for resultado in resultados:
            self.tree.insert("", "end", values=(resultado["desde"], resultado["hacia"],
                                                resultado["porcentaje_tiempo"], resultado["vehiculos"]))

