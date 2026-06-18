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
    # Vérifier si un point décimal existe déjà dans le nombre courant
    expr = self.view_model.current_expression
    # Trouver le dernier nombre dans l'expression
    import re
    numbers = re.findall(r'[\d.]+$', expr)
    if numbers and '.' in numbers[-1]:
        return
    self.view_model.append_char(".")
    self._update_display()


def _on_operator(self, op):
    """Ajoute un opérateur"""
    # Remplacer les symboles d'affichage par les vrais
    op_map = {"×": "*", "−": "-", "÷": "/", "+": "+", "^": "**"}
    real_op = op_map.get(op, op)

    expr = self.view_model.current_expression
    # Si l'expression se termine par un opérateur, le remplacer
    if expr and expr[-1] in '+-*/':
        self.view_model.current_expression = expr[:-1]

    self.view_model.append_char(real_op)
    self._update_display()
    self._update_history()


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
        "e": "e",
    }
    value = func_map.get(func, func)

    # Si un résultat est affiché, recommencer
    if self.view_model.result_shown:
        self.view_model.clear()

    self.view_model.append_char(value)
    self._update_display()
    self._update_history()


def _on_percent(self):
    """Ajoute le pourcentage"""
    self.view_model.append_char("%")
    self._update_display()


def _on_toggle_sign(self):
    """Change le signe"""
    expr = self.view_model.current_expression
    if not expr:
        return

    # Si l'expression est un nombre simple
    try:
        # Trouver le dernier nombre dans l'expression
        import re
        match = re.search(r'([\d.]+)$', expr)
        if match:
            num = match.group(1)
            if expr.endswith(num):
                if expr.startswith('-'):
                    # Enlever le signe moins
                    new_expr = expr[1:]
                else:
                    # Ajouter un signe moins
                    new_expr = '-' + expr
                self.view_model.current_expression = new_expr
                self._update_display()
    except:
        pass


def _on_equals(self):
    """Calcule le résultat"""
    expr = self.view_model.current_expression
    if not expr:
        return

    # Nettoyer l'expression pour l'affichage
    display_expr = expr

    result = self.view_model.calculate(expr)

    # Mettre à jour l'affichage
    self.current_display.set(result)
    self._update_history()

    # Si c'est une erreur, ne pas garder le résultat
    if "Erreur" in result:
        self.view_model.result_shown = False


def _on_clear(self):
    """Efface tout"""
    self.view_model.clear()
    self._update_display()
    self._update_history()


def _on_backspace(self):
    """Supprime le dernier caractère"""
    self.view_model.backspace()
    self._update_display()
    self._update_history()


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
    elif key == "=" or key == "\r":  # Enter
        self._on_equals()
    elif key == "\x08":  # Backspace
        self._on_backspace()