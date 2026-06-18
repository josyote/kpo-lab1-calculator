import tkinter as tk
from view import CalculatorView

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorView(root)
    root.mainloop()