import tkinter as tk
from tkinter import font
from model import CalculatorModel
from viewmodel import CalculatorViewModel


class CalculatorView:
    def __init__(self, root, view_model):
        self.root = root
        self.view_model = view_model

        # Configuration de la fenêtre
        self.root.title("Калькулятор MVVM v2.0")
        self.root.geometry("360x700")
        self.root.configure(bg="#1A1A1A")
        self.root.resizable(False, False)

        # Variables pour l'interface
        self.current_display = tk.StringVar(value="0")
        self.history_text = tk.StringVar(value="")

        # Polices
        self.display_font = font.Font(family="Segoe UI", size=40, weight="normal")
        self.history_font = font.Font(family="Segoe UI", size=11)
        self.button_font = font.Font(family="Segoe UI", size=14, weight="normal")

        # Setup UI
        self._setup_ui()
        self._update_display()
        self._setup_bindings()

    def _setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#1A1A1A")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ========== SECTION AFFICHAGE ==========
        display_container = tk.Frame(main_frame, bg="#1A1A1A")
        display_container.pack(fill=tk.X, pady=(0, 15))

        display_frame = tk.Frame(
            display_container,
            bg="#2A2A2A",
            height=130,
            highlightbackground="#3A3A3A",
            highlightthickness=1
        )
        display_frame.pack(fill=tk.X)
        display_frame.pack_propagate(False)

        # Historique
        self.history_label = tk.Label(
            display_frame,
            textvariable=self.history_text,
            font=self.history_font,
            bg="#2A2A2A",
            fg="#888888",
            anchor="e",
            justify="right"
        )
        self.history_label.pack(fill=tk.X, pady=(5, 0), padx=15)

        # Affichage principal
        self.display_label = tk.Label(
            display_frame,
            textvariable=self.current_display,
            font=self.display_font,
            bg="#2A2A2A",
            fg="#FFFFFF",
            anchor="e",
            padx=15
        )
        self.display_label.pack(fill=tk.BOTH, expand=True)

        # ========== SECTION CLAVIER ==========
        keypad = tk.Frame(main_frame, bg="#1A1A1A")
        keypad.pack(fill=tk.BOTH, expand=True)

        # Configuration des couleurs
        colors = {
            "number": {"bg": "#2A2A2A", "fg": "#FFFFFF", "active": "#3A3A3A"},
            "operator": {"bg": "#2D2D2D", "fg": "#6C9EBF", "active": "#3D3D3D"},
            "function": {"bg": "#252525", "fg": "#E0E0E0", "active": "#353535"},
            "equals": {"bg": "#6C9EBF", "fg": "#FFFFFF", "active": "#5A8AB0"},
        }

        # Définition des boutons - 7 lignes x 4 colonnes
        buttons = [
            # Ligne 1: C, ⌫, %, ÷
            ("C", 0, 0, "function"), ("⌫", 0, 1, "function"),
            ("%", 0, 2, "operator"), ("÷", 0, 3, "operator"),

            # Ligne 2: 7, 8, 9, ×
            ("7", 1, 0, "number"), ("8", 1, 1, "number"),
            ("9", 1, 2, "number"), ("×", 1, 3, "operator"),

            # Ligne 3: 4, 5, 6, −
            ("4", 2, 0, "number"), ("5", 2, 1, "number"),
            ("6", 2, 2, "number"), ("−", 2, 3, "operator"),

            # Ligne 4: 1, 2, 3, +
            ("1", 3, 0, "number"), ("2", 3, 1, "number"),
            ("3", 3, 2, "number"), ("+", 3, 3, "operator"),

            # Ligne 5: ±, 0, ., =
            ("±", 4, 0, "function"), ("0", 4, 1, "number"),
            (".", 4, 2, "number"), ("=", 4, 3, "equals"),

            # Ligne 6: sin, cos, tan, √
            ("sin", 5, 0, "function"), ("cos", 5, 1, "function"),
            ("tan", 5, 2, "function"), ("√", 5, 3, "function"),

            # Ligne 7: ln, log, π, ^
            ("ln", 6, 0, "function"), ("log", 6, 1, "function"),
            ("π", 6, 2, "function"), ("^", 6, 3, "operator"),
        ]

        # Création des boutons
        for text, row, col, style in buttons:
            color = colors[style]

            frame = tk.Frame(keypad, bg="#0A0A0A")
            frame.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

            # Déterminer la commande
            if style == "number":
                if text == ".":
                    command = self._on_decimal
                else:
                    command = lambda t=text: self._on_digit(t)
            elif style == "operator":
                command = lambda t=text: self._on_operator(t)
            elif style == "function":
                if text == "C":
                    command = self._on_clear
                elif text == "⌫":
                    command = self._on_backspace
                elif text == "±":
                    command = self._on_toggle_sign
                elif text == "%":
                    command = self._on_percent
                else:
                    command = lambda t=text: self._on_function(t)
            elif style == "equals":
                command = self._on_equals

            btn = tk.Button(
                frame,
                text=text,
                font=self.button_font,
                bg=color["bg"],
                fg=color["fg"],
                activebackground=color["active"],
                activeforeground=color["fg"],
                relief=tk.FLAT,
                bd=0,
                command=command,
                cursor="hand2",
                height=2,
            )
            btn.pack(fill=tk.BOTH, expand=True)

            # Effet de survol
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.configure(bg="#3A3A3A"))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.configure(bg=color["bg"]))

        # Configuration de la grille
        for i in range(7):
            keypad.grid_rowconfigure(i, weight=1)
        for i in range(4):
            keypad.grid_columnconfigure(i, weight=1)

    def _setup_bindings(self):
        """Configure les raccourcis clavier"""
        self.root.bind("<Key>", self._on_key_press)
        self.root.bind("<Return>", lambda e: self._on_equals())
        self.root.bind("<BackSpace>", lambda e: self._on_backspace())
        self.root.bind("<Escape>", lambda e: self._on_clear())

    # ========== MÉTHODES DE L'INTERFACE ==========

    def _update_display(self):
        """Met à jour l'affichage avec la valeur du ViewModel"""
        value = self.view_model.get_display_value()
        if not value:
            value = "0"
        self.current_display.set(value)

    def _update_history(self):
        """Met à jour l'historique"""
        history = self.view_model.get_history()
        if history:
            display = "\n".join(history[-5:])
            self.history_text.set(display)
        else:
            self.history_text.set("")

    # ========== GESTIONNAIRES D'ÉVÉNEMENTS ==========

    def _on_digit(self, digit):
        """Ajoute un chiffre"""
        self.view_model.append_char(digit)
        self._update_display()
        self._update_history()

    def _on_decimal(self):
        """Ajoute un point décimal"""
        self.view_model.append_char(".")
        self._update_display()

    def _on_operator(self, op):
        """Ajoute un opérateur"""
        op_map = {"×": "*", "−": "-", "÷": "/", "+": "+", "^": "**"}
        real_op = op_map.get(op, op)

        expr = self.view_model.current_expression
        # Si l'expression se termine par un opérateur, le remplacer
        if expr and expr[-1] in '+-*/':
            self.view_model.current_expression = expr[:-1]

        self.view_model.append_char(real_op)
        self._update_display()

    def _on_function(self, func):
        """Ajoute une fonction"""
        func_map = {
            "sin": "sin(",
            "cos": "cos(",
            "tan": "tan(",
            "√": "sqrt(",
            "ln": "log(",
            "log": "log10(",
            "π": "pi",
        }
        value = func_map.get(func, func)

        if self.view_model.result_shown:
            self.view_model.clear()

        self.view_model.append_char(value)
        self._update_display()

    def _on_percent(self):
        """Ajoute le pourcentage"""
        self.view_model.append_char("%")
        self._update_display()

    def _on_toggle_sign(self):
        """Change le signe"""
        expr = self.view_model.current_expression
        if not expr or expr == "0":
            return

        # Si l'expression est un nombre simple
        if expr.startswith('-'):
            self.view_model.current_expression = expr[1:]
        else:
            self.view_model.current_expression = '-' + expr
        self._update_display()

    def _on_equals(self):
        """Calcule le résultat"""
        expr = self.view_model.current_expression
        if not expr:
            return

        result = self.view_model.calculate(expr)
        self.current_display.set(result)
        self._update_history()

        if "Erreur" not in result:
            self.view_model.current_expression = result
            self.view_model.result_shown = True
            self.view_model.last_result = result

    def _on_clear(self):
        """Efface tout"""
        self.view_model.clear()
        self._update_display()
        self._update_history()

    def _on_backspace(self):
        """Supprime le dernier caractère"""
        self.view_model.backspace()
        self._update_display()

    def _on_key_press(self, event):
        """Gère les touches du clavier"""
        key = event.char

        if key.isdigit():
            self._on_digit(key)
        elif key == ".":
            self._on_decimal()
        elif key in "+-*/":
            op_map = {"+": "+", "-": "−", "*": "×", "/": "÷"}
            self._on_operator(op_map.get(key, key))
        elif key == "%":
            self._on_percent()
        elif key == "=" or key == "\r":
            self._on_equals()
        elif event.keysym == "BackSpace":
            self._on_backspace()
        elif event.keysym == "Escape":
            self._on_clear()


# ========== MAIN ==========

if __name__ == "__main__":
    root = tk.Tk()
    view_model = CalculatorViewModel()
    view = CalculatorView(root, view_model)
    root.mainloop()