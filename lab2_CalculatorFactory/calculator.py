import tkinter as tk
from tkinter import font
from abc import ABC, abstractmethod
import math


# ============================================================
# 1. PATRON DE CONCEPTION : ABSTRACT FACTORY
# ============================================================

class Button(ABC):
    """Classe abstraite pour tous les types de boutons"""

    @abstractmethod
    def get_text(self) -> str:
        pass

    @abstractmethod
    def execute(self, calculator) -> str:
        """Exécute l'action du bouton et retourne le résultat"""
        pass

    @abstractmethod
    def get_style(self) -> str:
        """Retourne le style du bouton"""
        pass


class DigitButton(Button):
    """Bouton numérique"""

    def __init__(self, digit: str):
        self._digit = digit

    def get_text(self) -> str:
        return self._digit

    def execute(self, calculator):
        calculator.add_digit(self._digit)
        return self._digit

    def get_style(self) -> str:
        return "number"


class OperatorButton(Button):
    """Bouton d'opération"""

    def __init__(self, operator: str):
        self._operator = operator
        self._symbol_map = {"+": "+", "-": "−", "*": "×", "/": "÷"}

    def get_text(self) -> str:
        return self._symbol_map.get(self._operator, self._operator)

    def execute(self, calculator):
        calculator.set_operation(self._operator)
        return self._operator

    def get_style(self) -> str:
        return "operator"


class EqualsButton(Button):
    """Bouton Égal"""

    def get_text(self) -> str:
        return "="

    def execute(self, calculator):
        calculator.calculate()
        return "="

    def get_style(self) -> str:
        return "equals"


class ClearButton(Button):
    """Bouton Effacer"""

    def get_text(self) -> str:
        return "C"

    def execute(self, calculator):
        calculator.clear_all()
        return "C"

    def get_style(self) -> str:
        return "function"


class DeleteButton(Button):
    """Bouton Supprimer dernier caractère"""

    def get_text(self) -> str:
        return "⌫"

    def execute(self, calculator):
        calculator.delete_last()
        return "⌫"

    def get_style(self) -> str:
        return "function"


class PercentageButton(Button):
    """Bouton Pourcentage"""

    def get_text(self) -> str:
        return "%"

    def execute(self, calculator):
        calculator.percentage()
        return "%"

    def get_style(self) -> str:
        return "operator"


class ToggleSignButton(Button):
    """Bouton Changer de signe"""

    def get_text(self) -> str:
        return "±"

    def execute(self, calculator):
        calculator.toggle_sign()
        return "±"

    def get_style(self) -> str:
        return "function"


class DecimalButton(Button):
    """Bouton Point décimal"""

    def get_text(self) -> str:
        return "."

    def execute(self, calculator):
        calculator.add_decimal()
        return "."

    def get_style(self) -> str:
        return "number"


class PowerButton(Button):
    """Bouton Carré"""

    def get_text(self) -> str:
        return "x²"

    def execute(self, calculator):
        calculator.power()
        return "x²"

    def get_style(self) -> str:
        return "function"


class MemoryClearButton(Button):
    """Bouton Effacer mémoire"""

    def get_text(self) -> str:
        return "MC"

    def execute(self, calculator):
        calculator.memory_clear()
        return "MC"

    def get_style(self) -> str:
        return "memory"


class MemoryRecallButton(Button):
    """Bouton Rappeler mémoire"""

    def get_text(self) -> str:
        return "MR"

    def execute(self, calculator):
        calculator.memory_recall()
        return "MR"

    def get_style(self) -> str:
        return "memory"


class MemoryAddButton(Button):
    """Bouton Ajouter à la mémoire"""

    def get_text(self) -> str:
        return "M+"

    def execute(self, calculator):
        calculator.memory_add()
        return "M+"

    def get_style(self) -> str:
        return "memory"


class MemorySubtractButton(Button):
    """Bouton Soustraire de la mémoire"""

    def get_text(self) -> str:
        return "M-"

    def execute(self, calculator):
        calculator.memory_subtract()
        return "M-"

    def get_style(self) -> str:
        return "memory"


# ============================================================
# 2. PATRON DE CONCEPTION : ABSTRACT FACTORY
# ============================================================

class ButtonFactory(ABC):
    """Factory abstraite pour créer des boutons"""

    @abstractmethod
    def create_button(self, button_type: str, *args) -> Button:
        pass


class StandardButtonFactory(ButtonFactory):
    """Factory concrète pour créer des boutons standards"""

    def create_button(self, button_type: str, *args) -> Button:
        if button_type == "digit":
            return DigitButton(args[0])
        elif button_type == "operator":
            return OperatorButton(args[0])
        elif button_type == "equals":
            return EqualsButton()
        elif button_type == "clear":
            return ClearButton()
        elif button_type == "delete":
            return DeleteButton()
        elif button_type == "percentage":
            return PercentageButton()
        elif button_type == "toggle_sign":
            return ToggleSignButton()
        elif button_type == "decimal":
            return DecimalButton()
        elif button_type == "power":
            return PowerButton()
        elif button_type == "memory_clear":
            return MemoryClearButton()
        elif button_type == "memory_recall":
            return MemoryRecallButton()
        elif button_type == "memory_add":
            return MemoryAddButton()
        elif button_type == "memory_subtract":
            return MemorySubtractButton()
        else:
            raise ValueError(f"Type de bouton inconnu: {button_type}")


# ============================================================
# 3. CALCULATOR ENGINE - LOGIQUE MÉTIER
# ============================================================

class CalculatorEngine:
    """Moteur de calcul - gère la logique métier"""

    def __init__(self):
        self.current_input = "0"
        self.previous_input = ""
        self.operation = None
        self.memory = 0
        self.new_number = True
        self.last_result = None

    def add_digit(self, digit: str):
        """Ajoute un chiffre"""
        if self.new_number or self.current_input == "0":
            self.current_input = digit
            self.new_number = False
        else:
            self.current_input += digit
        return self.current_input

    def add_decimal(self):
        """Ajoute un point décimal"""
        if self.new_number:
            self.current_input = "0."
            self.new_number = False
        elif "." not in self.current_input:
            self.current_input += "."
        return self.current_input

    def set_operation(self, op: str):
        """Définit l'opération"""
        if self.current_input and not self.new_number:
            self.previous_input = self.current_input
            self.operation = op
            self.new_number = True
        return self.operation

    def calculate(self):
        """Effectue le calcul"""
        if not self.operation or not self.previous_input:
            return None

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
                    raise ZeroDivisionError("Division par zéro impossible")
                result = num1 / num2

            # Formatage du résultat
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 10)
                if result == int(result):
                    result = int(result)

            self.current_input = str(result)
            self.operation = None
            self.previous_input = ""
            self.new_number = True
            self.last_result = result

            return result

        except ZeroDivisionError as e:
            raise e
        except Exception:
            raise ValueError("Erreur de calcul")

    def percentage(self):
        """Calcule le pourcentage"""
        try:
            if self.current_input:
                value = float(self.current_input) / 100
                self.current_input = str(value if not value.is_integer() else int(value))
            return self.current_input
        except ValueError:
            return self.current_input

    def toggle_sign(self):
        """Change le signe"""
        if self.current_input and self.current_input != "0":
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
        return self.current_input

    def power(self):
        """Élève au carré"""
        try:
            result = float(self.current_input) ** 2
            if result.is_integer():
                result = int(result)
            self.current_input = str(result)
            return self.current_input
        except ValueError:
            return self.current_input

    def clear_all(self):
        """Réinitialise tout"""
        self.current_input = "0"
        self.previous_input = ""
        self.operation = None
        self.new_number = True
        self.last_result = None

    def delete_last(self):
        """Supprime le dernier caractère"""
        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
        else:
            self.current_input = "0"
            self.new_number = True
        return self.current_input

    def memory_add(self):
        """Ajoute à la mémoire"""
        try:
            self.memory += float(self.current_input)
        except ValueError:
            pass

    def memory_subtract(self):
        """Soustrait de la mémoire"""
        try:
            self.memory -= float(self.current_input)
        except ValueError:
            pass

    def memory_recall(self):
        """Rappelle la mémoire"""
        if self.memory != 0:
            self.current_input = str(self.memory)
            self.new_number = True
        return self.current_input

    def memory_clear(self):
        """Efface la mémoire"""
        self.memory = 0

    def format_number(self, num_str: str) -> str:
        """Formate un nombre avec séparateurs de milliers"""
        try:
            if num_str.startswith("-"):
                return "-" + self.format_number(num_str[1:])
            if len(num_str) > 3:
                groups = []
                while num_str:
                    groups.append(num_str[-3:])
                    num_str = num_str[:-3]
                return " ".join(reversed(groups))
            return num_str
        except:
            return num_str

    def get_formatted_display(self) -> str:
        """Retourne l'affichage formaté"""
        try:
            if "." in self.current_input:
                parts = self.current_input.split(".")
                if parts[0]:
                    parts[0] = self.format_number(parts[0])
                return ".".join(parts)
            return self.format_number(self.current_input)
        except:
            return self.current_input


# ============================================================
# 4. CALCULATOR VIEW - INTERFACE UTILISATEUR
# ============================================================

class CalculatorView:
    """Gère l'interface utilisateur"""

    def __init__(self, root, engine: CalculatorEngine):
        self.root = root
        self.engine = engine
        self.button_factory = StandardButtonFactory()

        # Configuration de la fenêtre
        self.root.title("Калькулятор v2.0 - Factory Pattern")
        self.root.geometry("360x650")
        self.root.configure(bg="#1A1A1A")

        # Polices
        self.display_font = font.Font(family="Segoe UI", size=48, weight="normal")
        self.small_font = font.Font(family="Segoe UI", size=14)
        self.button_font = font.Font(family="Segoe UI", size=18, weight="normal")
        self.memory_font = font.Font(family="Segoe UI", size=12)

        self._setup_ui()
        self._setup_bindings()

    def _setup_ui(self):
        """Configure l'interface utilisateur"""
        main_frame = tk.Frame(self.root, bg="#1A1A1A")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # ========== SECTION AFFICHAGE ==========
        display_container = tk.Frame(main_frame, bg="#1A1A1A", height=160)
        display_container.pack(fill=tk.X, pady=(0, 20))
        display_container.pack_propagate(False)

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

        # Historique
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

        # Couleurs
        colors = {
            "number": {"bg": "#2A2A2A", "fg": "#FFFFFF", "active": "#3A3A3A", "hover": "#353535"},
            "operator": {"bg": "#2D2D2D", "fg": "#6C9EBF", "active": "#3D3D3D", "hover": "#3A3A3A"},
            "function": {"bg": "#252525", "fg": "#E0E0E0", "active": "#353535", "hover": "#303030"},
            "equals": {"bg": "#6C9EBF", "fg": "#FFFFFF", "active": "#5A8AB0", "hover": "#7BADD9"},
            "memory": {"bg": "#252525", "fg": "#E8A87C", "active": "#353535", "hover": "#303030"}
        }

        # Définition des boutons avec la factory
        button_definitions = [
            # Ligne 1: Mémoire
            ("memory_clear", 0, 0), ("memory_recall", 0, 1),
            ("memory_add", 0, 2), ("memory_subtract", 0, 3),
            # Ligne 2: Fonctions
            ("clear", 1, 0), ("delete", 1, 1),
            ("percentage", 1, 2), ("operator", 1, 3, "/"),
            # Ligne 3: 7,8,9,÷
            ("digit", 2, 0, "7"), ("digit", 2, 1, "8"),
            ("digit", 2, 2, "9"), ("operator", 2, 3, "*"),
            # Ligne 4: 4,5,6,-
            ("digit", 3, 0, "4"), ("digit", 3, 1, "5"),
            ("digit", 3, 2, "6"), ("operator", 3, 3, "-"),
            # Ligne 5: 1,2,3,+
            ("digit", 4, 0, "1"), ("digit", 4, 1, "2"),
            ("digit", 4, 2, "3"), ("operator", 4, 3, "+"),
            # Ligne 6: ±,0,.,=
            ("toggle_sign", 5, 0), ("digit", 5, 1, "0"),
            ("decimal", 5, 2), ("equals", 5, 3),
            # Ligne 7: x²
            ("power", 6, 0),
        ]

        # Création des boutons
        for btn_def in button_definitions:
            btn_type = btn_def[0]
            row = btn_def[1]
            col = btn_def[2]

            # Création du bouton via la factory
            if btn_type == "digit":
                button = self.button_factory.create_button("digit", btn_def[3])
            elif btn_type == "operator":
                button = self.button_factory.create_button("operator", btn_def[3])
            else:
                button = self.button_factory.create_button(btn_type)

            # Création de l'interface
            color = colors[button.get_style()]

            frame = tk.Frame(keypad, bg="#0A0A0A")
            frame.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")

            # Commande qui encapsule l'action
            def make_command(btn_obj=button):
                return lambda: self._on_button_click(btn_obj)

            tk_btn = tk.Button(
                frame,
                text=button.get_text(),
                font=self.button_font,
                bg=color["bg"],
                fg=color["fg"],
                activebackground=color["active"],
                activeforeground=color["fg"],
                relief=tk.FLAT,
                bd=0,
                command=make_command(),
                cursor="hand2",
                width=4,
                height=2
            )
            tk_btn.pack(fill=tk.BOTH, expand=True)

            # Effet de survol
            tk_btn.bind("<Enter>", lambda e, b=tk_btn, c=color: b.configure(bg=c["hover"]))
            tk_btn.bind("<Leave>", lambda e, b=tk_btn, c=color: b.configure(bg=c["bg"]))

        # Configuration de la grille
        for i in range(7):
            keypad.grid_rowconfigure(i, weight=1)
        for i in range(4):
            keypad.grid_columnconfigure(i, weight=1)

    def _on_button_click(self, button: Button):
        """Gère le clic sur un bouton"""
        try:
            button.execute(self)
            self._update_view()
        except ZeroDivisionError:
            self._show_error("Division par zéro impossible")
        except ValueError as e:
            self._show_error(str(e))

    def _update_view(self):
        """Met à jour l'affichage"""
        self.display.config(text=self.engine.get_formatted_display())
        self._update_memory_indicator()

    def _update_memory_indicator(self):
        """Met à jour l'indicateur de mémoire"""
        if self.engine.memory != 0:
            self.memory_indicator.config(text="M")
        else:
            self.memory_indicator.config(text="")

    def _show_error(self, message: str):
        """Affiche une erreur"""
        self.history_display.config(text=f"⚠ {message}")
        self.root.after(2000, lambda: self.history_display.config(text=""))

    def _setup_bindings(self):
        """Configure les raccourcis clavier"""
        self.root.bind("<Key>", self._on_key_press)
        self.root.bind("<Return>", lambda e: self._on_button_click(EqualsButton()))
        self.root.bind("<BackSpace>", lambda e: self._on_button_click(DeleteButton()))
        self.root.bind("<Escape>", lambda e: self._on_button_click(ClearButton()))
        self.root.bind("<Delete>", lambda e: self._on_button_click(ClearButton()))

    def _on_key_press(self, event):
        """Gère les entrées clavier"""
        key = event.char

        if key.isdigit():
            self._on_button_click(DigitButton(key))
        elif key == ".":
            self._on_button_click(DecimalButton())
        elif key in "+-*/":
            self._on_button_click(OperatorButton(key))
        elif key == "%":
            self._on_button_click(PercentageButton())
        elif key == "=" or key == "\r":
            self._on_button_click(EqualsButton())

    # Méthodes proxy vers le moteur (pour que les boutons puissent appeler)
    def add_digit(self, digit):
        self.engine.add_digit(digit)

    def add_decimal(self):
        self.engine.add_decimal()

    def set_operation(self, op):
        self.engine.set_operation(op)

    def calculate(self):
        self.engine.calculate()

    def percentage(self):
        self.engine.percentage()

    def toggle_sign(self):
        self.engine.toggle_sign()

    def power(self):
        self.engine.power()

    def clear_all(self):
        self.engine.clear_all()

    def delete_last(self):
        self.engine.delete_last()

    def memory_add(self):
        self.engine.memory_add()

    def memory_subtract(self):
        self.engine.memory_subtract()

    def memory_recall(self):
        self.engine.memory_recall()

    def memory_clear(self):
        self.engine.memory_clear()


# ============================================================
# 5. APPLICATION PRINCIPALE
# ============================================================

class CalculatorApp:
    """Application principale"""

    def __init__(self):
        self.root = tk.Tk()
        self.engine = CalculatorEngine()
        self.view = CalculatorView(self.root, self.engine)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = CalculatorApp()
    app.run()