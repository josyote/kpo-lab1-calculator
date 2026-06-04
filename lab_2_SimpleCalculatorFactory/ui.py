import tkinter as tk
from tkinter import font
from factory import CalculatorButtonFactory
from calculator_logic import CalculatorLogic


class CalculatorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator - Factory Pattern")
        self.root.geometry("420x650")
        self.root.configure(bg="#2C2C2C")
        self.root.resizable(False, False)

        self.factory = CalculatorButtonFactory()
        self.logic = CalculatorLogic()

        self.display_font = font.Font(family="Segoe UI", size=32)
        self.button_font = font.Font(family="Segoe UI", size=11)

        self.setup_ui()
        self.setup_keyboard_bindings()

    def setup_ui(self):
        # AFFICHAGE
        display_frame = tk.Frame(self.root, bg="#2C2C2C")
        display_frame.pack(fill=tk.X, padx=10, pady=(20, 10))

        self.display_label = tk.Label(
            display_frame,
            text="0",
            font=self.display_font,
            bg="#1E1E1E",
            fg="#FFFFFF",
            anchor="e",
            padx=15,
            pady=20,
            relief=tk.FLAT
        )
        self.display_label.pack(fill=tk.BOTH, expand=True)

        # CLAVIER
        buttons_frame = tk.Frame(self.root, bg="#2C2C2C")
        buttons_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        buttons_config = [
            # Ligne 1 - Fonctions scientifiques
            ("sin", "sin", 0, 0),
            ("cos", "cos", 0, 1),
            ("tan", "tan", 0, 2),
            ("pi", "π", 0, 3),

            # Ligne 2
            ("ln", "ln", 1, 0),
            ("log", "log", 1, 1),
            ("sqrt", "√x", 1, 2),
            ("e", "e", 1, 3),

            # Ligne 3
            ("power", "xʸ", 2, 0),
            ("square", "x²", 2, 1),
            ("percentage", "%", 2, 2),
            ("sign", "±", 2, 3),

            # Ligne 4 - Chiffres + opérateurs
            ("digit", "7", 3, 0),
            ("digit", "8", 3, 1),
            ("digit", "9", 3, 2),
            ("operator", "/", 3, 3),

            # Ligne 5
            ("digit", "4", 4, 0),
            ("digit", "5", 4, 1),
            ("digit", "6", 4, 2),
            ("operator", "*", 4, 3),

            # Ligne 6
            ("digit", "1", 5, 0),
            ("digit", "2", 5, 1),
            ("digit", "3", 5, 2),
            ("operator", "-", 5, 3),

            # Ligne 7
            ("digit", "0", 6, 0),
            ("decimal", ".", 6, 1),
            ("clear", "C", 6, 2),
            ("equals", "=", 6, 3),
        ]

        for i in range(7):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.grid_columnconfigure(j, weight=1)

        for btn_type, btn_text, row, col in buttons_config:
            if btn_type == "digit":
                button = self.factory.create_button("digit", int(btn_text))
            elif btn_type == "operator":
                button = self.factory.create_button("operator", btn_text)
            elif btn_type == "equals":
                button = self.factory.create_button("equals")
            elif btn_type == "clear":
                button = self.factory.create_button("clear")
            elif btn_type == "percentage":
                button = self.factory.create_button("percentage")
            elif btn_type == "sign":
                button = self.factory.create_button("sign")
            elif btn_type == "square":
                button = self.factory.create_button("square")
            elif btn_type == "decimal":
                button = self.factory.create_button("decimal")
            elif btn_type == "sin":
                button = self.factory.create_button("sin")
            elif btn_type == "cos":
                button = self.factory.create_button("cos")
            elif btn_type == "tan":
                button = self.factory.create_button("tan")
            elif btn_type == "ln":
                button = self.factory.create_button("ln")
            elif btn_type == "log":
                button = self.factory.create_button("log")
            elif btn_type == "sqrt":
                button = self.factory.create_button("sqrt")
            elif btn_type == "pi":
                button = self.factory.create_button("pi")
            elif btn_type == "e":
                button = self.factory.create_button("e")
            elif btn_type == "power":
                button = self.factory.create_button("power")
            else:
                continue

            # Couleurs
            if btn_type == "digit":
                bg_color = "#3A3A3A"
            elif btn_type == "operator":
                bg_color = "#1E3A5F"
            elif btn_type == "equals":
                bg_color = "#4CAF50"
            elif btn_type in ["sin", "cos", "tan", "ln", "log", "sqrt", "pi", "e", "power", "square"]:
                bg_color = "#555555"
            else:
                bg_color = "#444444"

            btn_widget = tk.Button(
                buttons_frame,
                text=button.get_display_text(),
                font=self.button_font,
                bg=bg_color,
                fg="#FFFFFF",
                activebackground="#666666",
                relief=tk.FLAT,
                bd=0,
                command=lambda b=button: self.on_button_click(b),
                cursor="hand2"
            )
            btn_widget.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

    def on_button_click(self, button):
        action = button.press()

        if action.isdigit():
            self.logic.add_digit(action)
        elif action == ".":
            self.logic.add_decimal()
        elif action in ["+", "-", "*", "/"]:
            self.logic.set_operation(action)
        elif action == "=":
            self.logic.calculate()
        elif action == "C":
            self.logic.clear()
        elif action == "±":
            self.logic.toggle_sign()
        elif action == "%":
            self.logic.percentage()
        elif action == "x²":
            self.logic.square()
        elif action == "sin":
            self.logic.add_sine()
        elif action == "cos":
            self.logic.add_cosine()
        elif action == "tan":
            self.logic.add_tangent()
        elif action == "ln":
            self.logic.add_ln()
        elif action == "log":
            self.logic.add_log10()
        elif action == "sqrt":
            self.logic.add_square_root()
        elif action == "pi":
            self.logic.add_pi()
        elif action == "e":
            self.logic.add_e()
        elif action == "^":
            self.logic.add_power()

        self.update_display()

    def update_display(self):
        self.display_label.config(text=self.logic.get_display())

    def setup_keyboard_bindings(self):
        self.root.bind("<Key>", self.key_press)
        self.root.bind("<Return>", lambda e: self.on_button_click(self.factory.create_button("equals")))
        self.root.bind("<Escape>", lambda e: self.on_button_click(self.factory.create_button("clear")))

    def key_press(self, event):
        key = event.char
        if key.isdigit():
            self.on_button_click(self.factory.create_button("digit", int(key)))
        elif key in "+-*/":
            self.on_button_click(self.factory.create_button("operator", key))
        elif key == ".":
            self.on_button_click(self.factory.create_button("decimal"))