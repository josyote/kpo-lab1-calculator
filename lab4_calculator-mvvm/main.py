import tkinter as tk
from model import CalculatorModel
from viewmodel import CalculatorViewModel
from view import CalculatorView

if __name__ == "__main__":
    root = tk.Tk()

    # Création du ViewModel
    view_model = CalculatorViewModel()

    # Création de la View avec le ViewModel
    view = CalculatorView(root, view_model)

    # Lancement de l'application
    root.mainloop()