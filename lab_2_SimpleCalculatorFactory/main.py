import tkinter as tk
from ui import CalculatorUI

def main():
    root = tk.Tk()
    app = CalculatorUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()