from model import CalculatorModel
from commands import CalculateCommand, FunctionCommand, ClearCommand, BackspaceCommand


class CalculatorViewModel:
    def __init__(self):
        self.model = CalculatorModel()
        self.current_expression = ""
        self.history = []
        self.result_shown = False
        self.last_result = ""
        self.command_history = []  # Historique des commandes pour UNDO
        self.max_history = 20

    def calculate(self, expression: str):
        """Calcule une expression et enregistre la commande"""
        if not expression or expression == "0":
            return "0"

        try:
            # Vérifier si c'est une fonction spéciale
            command = None

            # Détecter les fonctions mathématiques
            func_patterns = ['sin', 'cos', 'tan', 'ln', '√', 'log']
            for func in func_patterns:
                if func in expression:
                    try:
                        # Extraire la valeur entre parenthèses
                        import re
                        match = re.search(rf'{func}\(([^)]+)\)', expression)
                        if match:
                            value = float(self.evaluate_simple(match.group(1)))
                            command = FunctionCommand(self.model, func, value)
                        else:
                            # Essayer sans parenthèses
                            value_str = expression.replace(func, '').strip()
                            if value_str:
                                value = float(self.evaluate_simple(value_str))
                                command = FunctionCommand(self.model, func, value)
                    except:
                        pass
                    break

            # Si ce n'est pas une fonction, c'est une expression normale
            if command is None:
                command = CalculateCommand(self.model, expression)

            # Exécuter la commande
            result = command.execute()

            # Ajouter à l'historique des commandes (pour UNDO)
            self.command_history.append(command)
            if len(self.command_history) > self.max_history:
                self.command_history = self.command_history[-self.max_history:]

            # Ajouter à l'historique d'affichage
            display_expr = expression
            display_expr = display_expr.replace('*', '×')
            display_expr = display_expr.replace('/', '÷')
            display_expr = display_expr.replace('-', '−')

            self.history.append(f"{display_expr} = {result}")
            if len(self.history) > 10:
                self.history = self.history[-10:]

            self.current_expression = result if "Erreur" not in result else ""
            self.result_shown = True
            self.last_result = result

            return result

        except Exception as e:
            return f"Erreur: {str(e)}"

    def evaluate_simple(self, expr: str) -> float:
        """Évalue une expression simple sans fonctions"""
        try:
            expr = expr.replace('×', '*')
            expr = expr.replace('÷', '/')
            expr = expr.replace('−', '-')
            expr = expr.replace('^', '**')
            expr = expr.replace('π', '3.14159265359')
            expr = expr.replace('e', '2.71828182846')

            # Supprimer les espaces
            expr = expr.replace(' ', '')

            if not expr:
                return 0.0

            import math
            result = eval(expr, {"math": math, "__builtins__": {}})
            if isinstance(result, float):
                if result.is_integer():
                    return float(int(result))
                return round(result, 10)
            return float(result)
        except:
            return 0.0

    def append_char(self, char: str):
        """Ajoute un caractère à l'expression"""
        if self.result_shown:
            # Si un résultat est affiché, on recommence
            if char in '0123456789.':
                self.current_expression = ""
                self.result_shown = False
            else:
                self.result_shown = False

        # Éviter les doubles opérateurs
        if char in '+-*/^' and self.current_expression and self.current_expression[-1] in '+-*/^':
            self.current_expression = self.current_expression[:-1]

        self.current_expression += char
        return self.current_expression

    def clear(self):
        """Efface tout (utilise ClearCommand)"""
        command = ClearCommand(self)
        self.command_history.append(command)
        if len(self.command_history) > self.max_history:
            self.command_history = self.command_history[-self.max_history:]
        return command.execute()

    def backspace(self):
        """Supprime le dernier caractère (utilise BackspaceCommand)"""
        command = BackspaceCommand(self)
        self.command_history.append(command)
        if len(self.command_history) > self.max_history:
            self.command_history = self.command_history[-self.max_history:]
        return command.execute()

    def undo(self):
        """Annule la dernière commande"""
        if not self.command_history:
            return "0"

        last_command = self.command_history.pop()
        result = last_command.undo()
        self.current_expression = result if result != "0" else ""
        self.result_shown = True
        self.last_result = result

        # Ajouter à l'historique
        self.history.append(f"↩ Annulation: {result}")
        if len(self.history) > 10:
            self.history = self.history[-10:]

        return result

    def get_display_value(self):
        """Retourne la valeur à afficher"""
        if self.result_shown and self.last_result:
            return self.last_result
        return self.current_expression if self.current_expression else "0"

    def get_history(self):
        """Retourne l'historique"""
        return self.history