import tkinter as tk
from model import CalculatorModel
from viewmodel import CalculatorViewModel
from view import CalculatorView

if __name__ == "__main__":
    root = tk.Tk()
    view_model = CalculatorViewModel()
    view = CalculatorView(root, view_model)
    root.mainloop()