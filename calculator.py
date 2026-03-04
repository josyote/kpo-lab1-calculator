import tkinter as tk
from tkinter import font
import math


class ElegantCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор v1.0")
        self.root.geometry("360x600")
        self.root.configure(bg="#1A1A1A")

        # Variables
        self.current_input = "0"
        self.previous_input = ""
        self.operation = None
        self.memory = 0
        self.new_number = True
        self.last_result = None

        # Polices élégantes
        self.display_font = font.Font(family="Segoe UI", size=48, weight="normal")
        self.small_font = font.Font(family="Segoe UI", size=14)
        self.button_font = font.Font(family="Segoe UI", size=18, weight="normal")
        self.memory_font = font.Font(family="Segoe UI", size=12)

        self.setup_ui()
        self.setup_bindings()

    def setup_ui(self):
        # Frame principal avec effet de profondeur
        main_frame = tk.Frame(self.root, bg="#1A1A1A")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # ========== SECTION AFFICHAGE ==========
        display_container = tk.Frame(main_frame, bg="#1A1A1A", height=160)
        display_container.pack(fill=tk.X, pady=(0, 20))
        display_container.pack_propagate(False)

        # Cadre de l'écran avec effet de verre
        screen_frame = tk.Frame(
            display_container,
            bg="#2A2A2A",
            highlightbackground="#3A3A3A",
            highlightthickness=1
        )
        screen_frame.pack(fill=tk.BOTH, expand=True)

        # Indicateur de mémoire
        self.memory_indicator = tk.Label(
            screen_frame,
            text="",
            font=self.memory_font,
            bg="#2A2A2A",
            fg="#6C9EBF",
            anchor="e"
        )
        self.memory_indicator.pack(fill=tk.X, pady=(5, 0), padx=15)

        # Écran principal
        self.display = tk.Label(
            screen_frame,
            text="0",
            font=self.display_font,
            bg="#2A2A2A",
            fg="#FFFFFF",
            anchor="e",
            padx=15
        )
        self.display.pack(fill=tk.BOTH, expand=True)

        # Petit écran pour les opérations précédentes
        self.history_display = tk.Label(
            screen_frame,
            text="",
            font=self.small_font,
            bg="#2A2A2A",
            fg="#888888",
            anchor="e",
            padx=15
        )
        self.history_display.pack(fill=tk.X, pady=(0, 5))

        # ========== SECTION CLAVIER ==========
        keypad = tk.Frame(main_frame, bg="#1A1A1A")
        keypad.pack(fill=tk.BOTH, expand=True)

        # Configuration des couleurs
        colors = {
            "number": {
                "bg": "#2A2A2A",
                "fg": "#FFFFFF",
                "active": "#3A3A3A",
                "hover": "#353535"
            },
            "operator": {
                "bg": "#2D2D2D",
                "fg": "#6C9EBF",
                "active": "#3D3D3D",
                "hover": "#3A3A3A"
            },
            "function": {
                "bg": "#252525",
                "fg": "#E0E0E0",
                "active": "#353535",
                "hover": "#303030"
            },
            "equals": {
                "bg": "#6C9EBF",
                "fg": "#FFFFFF",
                "active": "#5A8AB0",
                "hover": "#7BADD9"
            },
            "memory": {
                "bg": "#252525",
                "fg": "#E8A87C",
                "active": "#353535",
                "hover": "#303030"
            }
        }

        # Définition des boutons avec des positions
        buttons = [
            # Ligne 1 : Fonctions spéciales
            {"text": "MC", "row": 0, "col": 0, "style": "memory", "cmd": self.memory_clear},
            {"text": "MR", "row": 0, "col": 1, "style": "memory", "cmd": self.memory_recall},
            {"text": "M+", "row": 0, "col": 2, "style": "memory", "cmd": self.memory_add},
            {"text": "M-", "row": 0, "col": 3, "style": "memory", "cmd": self.memory_subtract},

            # Ligne 2 : Fonctions avancées
            {"text": "C", "row": 1, "col": 0, "style": "function", "cmd": self.clear_all},
            {"text": "⌫", "row": 1, "col": 1, "style": "function", "cmd": self.delete_last},
            {"text": "%", "row": 1, "col": 2, "style": "operator", "cmd": self.percentage},
            {"text": "÷", "row": 1, "col": 3, "style": "operator", "cmd": lambda: self.set_operation("/")},

            # Ligne 3
            {"text": "7", "row": 2, "col": 0, "style": "number", "cmd": lambda: self.add_digit("7")},
            {"text": "8", "row": 2, "col": 1, "style": "number", "cmd": lambda: self.add_digit("8")},
            {"text": "9", "row": 2, "col": 2, "style": "number", "cmd": lambda: self.add_digit("9")},
            {"text": "×", "row": 2, "col": 3, "style": "operator", "cmd": lambda: self.set_operation("*")},

            # Ligne 4
            {"text": "4", "row": 3, "col": 0, "style": "number", "cmd": lambda: self.add_digit("4")},
            {"text": "5", "row": 3, "col": 1, "style": "number", "cmd": lambda: self.add_digit("5")},
            {"text": "6", "row": 3, "col": 2, "style": "number", "cmd": lambda: self.add_digit("6")},
            {"text": "−", "row": 3, "col": 3, "style": "operator", "cmd": lambda: self.set_operation("-")},

            # Ligne 5
            {"text": "1", "row": 4, "col": 0, "style": "number", "cmd": lambda: self.add_digit("1")},
            {"text": "2", "row": 4, "col": 1, "style": "number", "cmd": lambda: self.add_digit("2")},
            {"text": "3", "row": 4, "col": 2, "style": "number", "cmd": lambda: self.add_digit("3")},
            {"text": "+", "row": 4, "col": 3, "style": "operator", "cmd": lambda: self.set_operation("+")},

            # Ligne 6
            {"text": "±", "row": 5, "col": 0, "style": "function", "cmd": self.toggle_sign},
            {"text": "0", "row": 5, "col": 1, "style": "number", "cmd": lambda: self.add_digit("0")},
            {"text": ".", "row": 5, "col": 2, "style": "number", "cmd": self.add_decimal},
            {"text": "=", "row": 5, "col": 3, "style": "equals", "cmd": self.calculate},
        ]

        # Création des boutons
        for btn in buttons:
            color = colors[btn["style"]]

            # Création du cadre pour l'effet d'ombre
            frame = tk.Frame(keypad, bg="#0A0A0A")
            frame.grid(row=btn["row"], column=btn["col"], padx=3, pady=3, sticky="nsew")

            button = tk.Button(
                frame,
                text=btn["text"],
                font=self.button_font,
                bg=color["bg"],
                fg=color["fg"],
                activebackground=color["active"],
                activeforeground=color["fg"],
                relief=tk.FLAT,
                bd=0,
                command=btn["cmd"],
                cursor="hand2",
                width=4,
                height=2
            )
            button.pack(fill=tk.BOTH, expand=True)

            # Effet de survol
            button.bind("<Enter>", lambda e, b=button, c=color: b.configure(bg=c["hover"]))
            button.bind("<Leave>", lambda e, b=button, c=color: b.configure(bg=c["bg"]))

        # Configuration des poids de la grille
        for i in range(6):
            keypad.grid_rowconfigure(i, weight=1)
        for i in range(4):
            keypad.grid_columnconfigure(i, weight=1)

    def setup_bindings(self):
        """Configure les raccourcis clavier"""
        self.root.bind("<Key>", self.key_press)

        # Gestion spéciale pour les touches de fonction
        self.root.bind("<Return>", lambda e: self.calculate())
        self.root.bind("<BackSpace>", lambda e: self.delete_last())
        self.root.bind("<Escape>", lambda e: self.clear_all())
        self.root.bind("<Delete>", lambda e: self.clear_all())

    def add_digit(self, digit):
        """Ajoute un chiffre"""
        if self.new_number or self.current_input == "0" or "=" in self.history_display.cget("text"):
            self.current_input = digit
            self.new_number = False
            self.history_display.config(text="")
        else:
            self.current_input += digit
        self.update_display()

    def add_decimal(self):
        """Ajoute un point décimal"""
        if self.new_number or "=" in self.history_display.cget("text"):
            self.current_input = "0."
            self.new_number = False
            self.history_display.config(text="")
        elif "." not in self.current_input:
            self.current_input += "."
        self.update_display()

    def set_operation(self, op):
        """Définit l'opération à effectuer"""
        if self.current_input and not self.new_number:
            self.previous_input = self.current_input
            self.operation = op
            self.new_number = True

            # Afficher l'opération dans l'historique
            op_symbol = {"+": "+", "-": "−", "*": "×", "/": "÷"}.get(op, op)
            self.history_display.config(text=f"{self.current_input} {op_symbol}")

    def calculate(self):
        """Effectue le calcul"""
        if not self.operation or not self.previous_input:
            return

        try:
            num1 = float(self.previous_input)
            num2 = float(self.current_input)
            result = 0

            if self.operation == "+":
                result = num1 + num2
            elif self.operation == "-":
                result = num1 - num2
            elif self.operation == "*":
                result = num1 * num2
            elif self.operation == "/":
                if num2 == 0:
                    self.show_error("Division par zéro impossible")
                    return
                result = num1 / num2

            # Formatage du résultat
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 10)
                if result == int(result):
                    result = int(result)

            # Affichage du résultat
            op_symbol = {"+": "+", "-": "−", "*": "×", "/": "÷"}.get(self.operation)
            self.history_display.config(text=f"{self.previous_input} {op_symbol} {self.current_input} =")
            self.current_input = str(result)
            self.operation = None
            self.previous_input = ""
            self.new_number = True
            self.last_result = result

            self.update_display()

        except ValueError:
            self.show_error("Erreur de calcul")

    def percentage(self):
        """Calcule le pourcentage"""
        try:
            if self.current_input:
                value = float(self.current_input) / 100
                self.current_input = str(value if not value.is_integer() else int(value))
                self.update_display()
        except ValueError:
            pass

    def toggle_sign(self):
        """Change le signe du nombre"""
        if self.current_input and self.current_input != "0":
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
            self.update_display()

    def memory_add(self):
        """Ajoute à la mémoire"""
        try:
            self.memory += float(self.current_input)
            self.update_memory_indicator()
        except ValueError:
            pass

    def memory_subtract(self):
        """Soustrait de la mémoire"""
        try:
            self.memory -= float(self.current_input)
            self.update_memory_indicator()
        except ValueError:
            pass

    def memory_recall(self):
        """Rappelle la valeur en mémoire"""
        if self.memory != 0:
            self.current_input = str(self.memory)
            self.new_number = True
            self.update_display()

    def memory_clear(self):
        """Efface la mémoire"""
        self.memory = 0
        self.update_memory_indicator()

    def update_memory_indicator(self):
        """Met à jour l'indicateur de mémoire"""
        if self.memory != 0:
            self.memory_indicator.config(text="M")
        else:
            self.memory_indicator.config(text="")

    def clear_all(self):
        """Réinitialise tout"""
        self.current_input = "0"
        self.previous_input = ""
        self.operation = None
        self.new_number = True
        self.history_display.config(text="")
        self.update_display()

    def delete_last(self):
        """Supprime le dernier caractère"""
        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
        else:
            self.current_input = "0"
            self.new_number = True
        self.update_display()

    def update_display(self):
        """Met à jour l'affichage"""
        # Formatage avec séparateurs de milliers
        try:
            if "." in self.current_input:
                parts = self.current_input.split(".")
                if parts[0]:
                    parts[0] = self.format_number(parts[0])
                self.display.config(text=".".join(parts))
            else:
                self.display.config(text=self.format_number(self.current_input))
        except:
            self.display.config(text=self.current_input)

    def format_number(self, num_str):
        """Formate un nombre avec séparateurs de milliers"""
        try:
            if num_str.startswith("-"):
                return "-" + self.format_number(num_str[1:])

            # Ajout des séparateurs de milliers
            if len(num_str) > 3:
                groups = []
                while num_str:
                    groups.append(num_str[-3:])
                    num_str = num_str[:-3]
                return " ".join(reversed(groups))
            return num_str
        except:
            return num_str

    def show_error(self, message):
        """Affiche une erreur temporaire"""
        self.history_display.config(text=f"⚠ {message}")
        self.root.after(2000, lambda: self.history_display.config(text=""))

    def key_press(self, event):
        """Gère les entrées clavier"""
        key = event.char

        if key.isdigit():
            self.add_digit(key)
        elif key == ".":
            self.add_decimal()
        elif key in "+-*/":
            op_map = {"+": "+", "-": "-", "*": "×", "/": "÷"}
            self.set_operation(key)
        elif key == "%":
            self.percentage()
        elif key == "=" or key == "\r":
            self.calculate()
        elif event.keysym == "Escape":
            self.clear_all()
        elif event.keysym == "BackSpace":
            self.delete_last()


# Lancement de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = ElegantCalculator(root)
    root.mainloop()