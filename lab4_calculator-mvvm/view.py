import tkinter as tk
from tkinter import font


class CalculatorView:
    def __init__(self, root, view_model):
        self.root = root
        self.view_model = view_model

        # Configuration de la fenêtre
        self.root.title("Simple Calculator MVVM with Command")
        self.root.geometry("450x700")
        self.root.configure(bg="#f5f6fa")
        self.root.resizable(False, False)

        # Polices
        self.display_font = font.Font(family="Arial", size=24)
        self.history_font = font.Font(family="Arial", size=14)
        self.button_font = font.Font(family="Arial", size=18)

        # Variables pour l'interface
        self.current_display = tk.StringVar(value="")
        self.history_text = tk.StringVar(value="<b>История:</b><br>")

        # Setup UI
        self._setup_ui()
        self._setup_bindings()

    def _setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#f5f6fa")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ========== SECTION AFFICHAGE ==========
        # Champ d'affichage
        self.display = tk.Entry(
            main_frame,
            textvariable=self.current_display,
            font=self.display_font,
            bg="white",
            fg="#2d3436",
            justify="right",
            relief=tk.FLAT,
            state="readonly"
        )
        self.display.config(highlightbackground="#dcdcdc", highlightthickness=1)
        self.display.pack(fill=tk.X, pady=(0, 10), ipady=15)

        # Champ d'historique
        self.history_frame = tk.Frame(
            main_frame,
            bg="white",
            highlightbackground="#dcdcdc",
            highlightthickness=1
        )
        self.history_frame.pack(fill=tk.X, pady=(0, 10))

        self.history_display = tk.Text(
            self.history_frame,
            font=self.history_font,
            bg="white",
            fg="#2d3436",
            height=6,
            relief=tk.FLAT,
            state="disabled"
        )
        self.history_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ========== SECTION CLAVIER ==========
        keypad = tk.Frame(main_frame, bg="#f5f6fa")
        keypad.pack(fill=tk.BOTH, expand=True)

        # Configuration des couleurs
        colors = {
            "default": {"bg": "#ffffff", "fg": "#2d3436", "active": "#e8ecef", "hover": "#e8ecef"},
            "operator": {"bg": "#74b9ff", "fg": "white", "active": "#339af0", "hover": "#339af0"},
            "function": {"bg": "#dfe4ea", "fg": "#2d3436", "active": "#ced4da", "hover": "#ced4da"},
            "equals": {"bg": "#ff7675", "fg": "white", "active": "#ff5e57", "hover": "#ff5e57"},
        }

        # Layout des boutons (identique à l'exemple PyQt)
        button_layout = [
            # Ligne 1: C, ⌫, (, ), ÷
            ('C', 0, 0, 'function'), ('⌫', 0, 1, 'function'), ('(', 0, 2, 'default'), (')', 0, 3, 'default'),
            ('÷', 0, 4, 'operator'),
            # Ligne 2: sin, cos, 7, 8, 9
            ('sin', 1, 0, 'function'), ('cos', 1, 1, 'function'), ('7', 1, 2, 'default'), ('8', 1, 3, 'default'),
            ('9', 1, 4, 'default'),
            # Ligne 3: tan, ln, 4, 5, 6
            ('tan', 2, 0, 'function'), ('ln', 2, 1, 'function'), ('4', 2, 2, 'default'), ('5', 2, 3, 'default'),
            ('6', 2, 4, 'default'),
            # Ligne 4: √, π, 1, 2, 3
            ('√', 3, 0, 'function'), ('π', 3, 1, 'function'), ('1', 3, 2, 'default'), ('2', 3, 3, 'default'),
            ('3', 3, 4, 'default'),
            # Ligne 5: e, ^, 0, ., =
            ('e', 4, 0, 'function'), ('^', 4, 1, 'operator'), ('0', 4, 2, 'default'), ('.', 4, 3, 'default'),
            ('=', 4, 4, 'equals'),
            # Ligne 6: log, %, ×, −, +
            ('log', 5, 0, 'function'), ('%', 5, 1, 'operator'), ('×', 5, 2, 'operator'), ('−', 5, 3, 'operator'),
            ('+', 5, 4, 'operator'),
            # Ligne 7: Undo (occupe 5 colonnes)
            ('Undo', 6, 0, 'function', 5)
        ]

        # Création des boutons
        self.buttons = {}
        for btn in button_layout:
            text = btn[0]
            row = btn[1]
            col = btn[2]
            style = btn[3]
            span = btn[4] if len(btn) > 4 else 1

            color = colors.get(style, colors["default"])

            frame = tk.Frame(keypad, bg="#f5f6fa")
            frame.grid(row=row, column=col, columnspan=span, padx=4, pady=4, sticky="nsew")

            # Texte spécial pour certains boutons
            display_text = text
            if text == '√':
                display_text = "√x"
            elif text == '^':
                display_text = "x^y"

            btn_widget = tk.Button(
                frame,
                text=display_text,
                font=self.button_font,
                bg=color["bg"],
                fg=color["fg"],
                activebackground=color["active"],
                activeforeground=color["fg"],
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                height=2,
            )

            # Si c'est Undo, on ajuste la largeur
            if text == 'Undo':
                btn_widget.config(width=20)

            btn_widget.pack(fill=tk.BOTH, expand=True)

            # Effet de survol
            btn_widget.bind("<Enter>", lambda e, b=btn_widget, c=color: b.configure(bg=c["hover"]))
            btn_widget.bind("<Leave>", lambda e, b=btn_widget, c=color: b.configure(bg=color["bg"]))

            # Commande
            if text == '=':
                command = lambda t=text: self._on_button_click(t)
            elif text == 'C':
                command = lambda t=text: self._on_button_click(t)
            elif text == '⌫':
                command = lambda t=text: self._on_button_click(t)
            elif text == 'Undo':
                command = lambda t=text: self._on_button_click(t)
            else:
                command = lambda t=text: self._on_button_click(t)

            btn_widget.config(command=command)
            self.buttons[text] = btn_widget

        # Configuration de la grille
        for i in range(7):
            keypad.grid_rowconfigure(i, weight=1)
        for i in range(5):
            keypad.grid_columnconfigure(i, weight=1)

    def _setup_bindings(self):
        """Configure les raccourcis clavier"""
        self.root.bind("<Key>", self._on_key_press)
        self.root.bind("<Return>", lambda e: self._on_button_click('='))
        self.root.bind("<BackSpace>", lambda e: self._on_button_click('⌫'))
        self.root.bind("<Escape>", lambda e: self._on_button_click('C'))
        self.root.bind("<Control-z>", lambda e: self._on_button_click('Undo'))

    def _on_button_click(self, char):
        """Gère le clic sur un bouton"""
        char = char.replace('√x', '√').replace('−', '-').replace('×', '*').replace('x^y', '^')

        if char == '=':
            # Émettre le signal calculate
            self.calculate_signal(self.current_display.get())
        elif char == 'C':
            self.clear_signal()
        elif char == '⌫':
            self.backspace_signal()
        elif char == 'Undo':
            self.undo_signal()
        else:
            # Ajouter le caractère à l'affichage
            current_text = self.current_display.get()
            display_char = char.replace('*', '×').replace('-', '−').replace('^', 'x^y')
            self.current_display.set(current_text + display_char)

    # ========== SIGNALS (remplacement des signaux PyQt) ==========

    def calculate_signal(self, expression):
        """Signal pour le calcul"""
        result = self.view_model.calculate(expression)
        self.set_result(result)
        self.update_history(self.view_model.history)

    def backspace_signal(self):
        """Signal pour backspace"""
        self.backspace()
        self.set_result(self.view_model.backspace(self.current_display.get()))

    def clear_signal(self):
        """Signal pour clear"""
        self.clear_display()
        self.view_model.clear()

    def undo_signal(self):
        """Signal pour undo"""
        self.set_result(self.view_model.undo())
        self.update_history(self.view_model.history)

    # ========== MÉTHODES DE L'INTERFACE ==========

    def set_result(self, result: str):
        self.current_display.set(result)

    def update_history(self, history: list):
        self.history_display.config(state="normal")
        self.history_display.delete("1.0", tk.END)
        self.history_display.insert("1.0", "История:\n")
        self.history_display.insert(tk.END, "\n".join(history[-5:]))
        self.history_display.config(state="disabled")

    def clear_display(self):
        self.current_display.set("")
        self.history_display.config(state="normal")
        self.history_display.delete("1.0", tk.END)
        self.history_display.insert("1.0", "История:\n")
        self.history_display.config(state="disabled")

    def backspace(self):
        current_text = self.current_display.get()
        if current_text:
            self.current_display.set(current_text[:-1])

    def _on_key_press(self, event):
        """Gère les touches du clavier"""
        key = event.char

        if key.isdigit():
            self._on_button_click(key)
        elif key == ".":
            self._on_button_click(".")
        elif key in "+-*/":
            op_map = {"+": "+", "-": "−", "*": "×", "/": "÷"}
            self._on_button_click(op_map.get(key, key))
        elif key == "=":
            self._on_button_click("=")
        elif key == "\r":  # Enter
            self._on_button_click("=")