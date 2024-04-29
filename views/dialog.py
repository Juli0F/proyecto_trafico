import tkinter as tk
from tkinter import messagebox


class Dialog(tk.Toplevel):
    def __init__(self, parent, title="Informacion", message="Error"):
        super().__init__(parent)
        #self.title("Diálogo")
        messagebox.showinfo(title, message)

