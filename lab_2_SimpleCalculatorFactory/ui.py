import tkinter as tk
from tkinter import font
from factory import CalculatorButtonFactory
from calculator_logic import CalculatorLogic


class CalculatorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator - Factory Pattern")
        self.root.geometry("320x500")
        self.root.configure(bg="#2C2C2C")
        self.root.resizable(False, False)

        # Initialisation
        self.factory = CalculatorButtonFactory()
        self.logic = CalculatorLogic()

        # Polices
        self.display_font = font.Font(family="Segoe UI", size=36)
        self.button_font = font.Font(family="Segoe UI", size=14)

        self.setup_ui()
        self.setup_keyboard_bindings()

    def setup_ui(self):
        # ========== AFFICHAGE ==========
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
            pady=15,
            relief=tk.FLAT
        )
        self.display_label.pack(fill=tk.BOTH, expand=True)

        # ========== CLAVIER ==========
        buttons_frame = tk.Frame(self.root, bg="#2C2C2C")
        buttons_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Définition des boutons (type, valeur, row, col)
        buttons_config = [
            # Ligne 1 : Fonctions
            ("clear", "C", 0, 0),
            ("percentage", "%", 0, 1),
            ("sign", "±", 0, 2),
            ("square", "x²", 0, 3),

            # Ligne 2
            ("digit", "7", 1, 0),
            ("digit", "8", 1, 1),
            ("digit", "9", 1, 2),
            ("operator", "/", 1, 3),

            # Ligne 3
            ("digit", "4", 2, 0),
            ("digit", "5", 2, 1),
            ("digit", "6", 2, 2),
            ("operator", "*", 2, 3),

            # Ligne 4
            ("digit", "1", 3, 0),
            ("digit", "2", 3, 1),
            ("digit", "3", 3, 2),
            ("operator", "-", 3, 3),

            # Ligne 5
            ("digit", "0", 4, 0),
            ("decimal", ".", 4, 1),
            ("equals", "=", 4, 2),
            ("operator", "+", 4, 3),
        ]

        # Configuration de la grille
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.grid_columnconfigure(j, weight=1)

        # Création des boutons
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
            else:
                continue

            # Styles pour différents types
            if btn_type == "digit":
                bg_color = "#3A3A3A"
                fg_color = "#FFFFFF"
            elif btn_type == "operator":
                bg_color = "#1E3A5F"
                fg_color = "#FFFFFF"
            elif btn_type == "equals":
                bg_color = "#4CAF50"
                fg_color = "#FFFFFF"
            else:  # fonctions
                bg_color = "#555555"
                fg_color = "#FFFFFF"

            btn_widget = tk.Button(
                buttons_frame,
                text=button.get_display_text(),
                font=self.button_font,
                bg=bg_color,
                fg=fg_color,
                activebackground="#666666",
                activeforeground="#FFFFFF",
                relief=tk.FLAT,
                bd=0,
                command=lambda b=button: self.on_button_click(b),
                cursor="hand2"
            )
            btn_widget.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)

            # Effet de survol
            btn_widget.bind("<Enter>", lambda e, b=btn_widget, c="#4A4A4A": b.configure(bg=c))
            btn_widget.bind("<Leave>", lambda e, b=btn_widget, c=bg_color: b.configure(bg=c))

        # Bouton spécial pour le 0 (colspan)
        # déjà géré dans la configuration

    def on_button_click(self, button):
        action = button.press()
        result = None

        if action.isdigit():
            result = self.logic.add_digit(action)
        elif action == ".":
            result = self.logic.add_decimal()
        elif action in ["+", "-", "*", "/"]:
            result = self.logic.set_operation(action)
        elif action == "=":
            result = self.logic.calculate()
        elif action == "C":
            result = self.logic.clear()
        elif action == "±":
            result = self.logic.toggle_sign()
        elif action == "%":
            result = self.logic.percentage()
        elif action == "x²":
            result = self.logic.square()

        if result:
            self.update_display()

    def update_display(self):
        self.display_label.config(text=self.logic.get_display())

    def setup_keyboard_bindings(self):
        self.root.bind("<Key>", self.key_press)
        self.root.bind("<Return>", lambda e: self.on_button_click(
            self.factory.create_button("equals")
        ))
        self.root.bind("<BackSpace>", lambda e: None)  # À implémenter
        self.root.bind("<Escape>", lambda e: self.on_button_click(
            self.factory.create_button("clear")
        ))

    def key_press(self, event):
        key = event.char
        if key.isdigit():
            self.on_button_click(self.factory.create_button("digit", int(key)))
        elif key in "+-*/":
            self.on_button_click(self.factory.create_button("operator", key))
        elif key == ".":
            self.on_button_click(self.factory.create_button("decimal"))
        elif key == "%":
            self.on_button_click(self.factory.create_button("percentage"))