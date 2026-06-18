from model import CalculatorModel


class CalculatorViewModel:
    def __init__(self):
        self.model = CalculatorModel()
        self.current_expression = ""
        self.history = []
        self.result_shown = False
        self.last_result = ""

    def calculate(self, expression: str):
        if not expression or expression == "0":
            return "0"

        try:
            result = self.model.calculate(expression)

            # Ajouter à l'historique avec affichage formaté
            display_expr = expression
            display_expr = display_expr.replace('*', '×')
            display_expr = display_expr.replace('/', '÷')
            display_expr = display_expr.replace('-', '−')

            self.history.append(f"{display_expr} = {result}")

            # Garder seulement les 10 derniers
            if len(self.history) > 10:
                self.history = self.history[-10:]

            self.current_expression = result if "Erreur" not in result else ""
            self.result_shown = True
            self.last_result = result

            return result

        except Exception as e:
            return f"Erreur: {str(e)}"

    def append_char(self, char: str):
        if self.result_shown:
            # Si un résultat est affiché et on appuie sur un chiffre, on recommence
            if char in '0123456789.':
                self.current_expression = ""
                self.result_shown = False
            else:
                # Sinon on continue sur le résultat
                self.result_shown = False

        # Ne pas ajouter d'espaces
        self.current_expression += char
        return self.current_expression

    def clear(self):
        self.current_expression = ""
        self.history = []
        self.result_shown = False
        self.last_result = ""
        return self.current_expression, self.history

    def backspace(self):
        if self.current_expression:
            self.current_expression = self.current_expression[:-1]
        return self.current_expression

    def get_history(self):
        return self.history

    def get_display_value(self):
        if self.result_shown and self.last_result:
            return self.last_result
        return self.current_expression if self.current_expression else "0"