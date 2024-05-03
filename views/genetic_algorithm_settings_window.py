import tkinter as tk

import models.config


class GeneticAlgorithmSettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Configuración del Algoritmo Genético")

        self.population_size = tk.IntVar(value=500)
        self.mutation_rate = tk.DoubleVar(value=0.1)
        self.termination_criteria = tk.StringVar(value="generacion")
        self.num_generations = tk.IntVar(value=100)
        self.target_aptitud = tk.DoubleVar(value=0.9)

        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self)
        main_frame.pack(padx=10, pady=10)

        population_label = tk.Label(main_frame, text="Tamaño de la población:")
        population_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

        population_entry = tk.Entry(main_frame, textvariable=self.population_size)
        population_entry.grid(row=0, column=1, padx=5, pady=5)

        mutation_label = tk.Label(main_frame, text="Tasa de mutación:")
        mutation_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

        mutation_entry = tk.Entry(main_frame, textvariable=self.mutation_rate)
        mutation_entry.grid(row=1, column=1, padx=5, pady=5)

        termination_label = tk.Label(main_frame, text="Criterio de finalización:")
        termination_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)

        termination_combo = tk.OptionMenu(main_frame, self.termination_criteria, "generations", "fitness")
        termination_combo.grid(row=2, column=1, padx=5, pady=5)

        generations_label = tk.Label(main_frame, text="Número de generaciones:")
        generations_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

        generations_entry = tk.Entry(main_frame, textvariable=self.num_generations)
        generations_entry.grid(row=3, column=1, padx=5, pady=5)





        save_button = tk.Button(main_frame, text="Guardar", command=self.save_settings)
        save_button.grid(row=5, column=0, columnspan=2, pady=10)

    def save_settings(self):
        models.config.POBLACION_SIZE = self.population_size.get()
        models.config.TASA_MUTACION = self.mutation_rate.get()
        models.config.GENERACIONES = self.num_generations.get()
        print("Configuracion del algoritmo: ",models.config.POBLACION_SIZE )

        self.destroy()