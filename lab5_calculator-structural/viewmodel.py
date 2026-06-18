from model import CalculatorModel


class CalculatorViewModel:
    def __init__(self):
        self.model = CalculatorModel()
        self.current_expression = ""
        self.result_shown = False
        self.last_result = ""

    def calculate(self, expression: str) -> str:
        if not expression:
            return "0"

        try:
            # Nettoyer l'expression pour éviter les problèmes
            clean_expr = expression
            clean_expr = clean_expr.replace('×', '*')
            clean_expr = clean_expr.replace('÷', '/')
            clean_expr = clean_expr.replace('−', '-')
            clean_expr = clean_expr.replace('^', '**')

            result = self.model.calculate(clean_expr)
            result_str = str(result)

            self.current_expression = result_str
            self.result_shown = True
            self.last_result = result_str

            return result_str

        except ValueError as e:
            error_msg = str(e)
            # Ajouter l'erreur à l'historique
            history = self.model.get_history()
            display_expr = expression
            display_expr = display_expr.replace('*', '×')
            display_expr = display_expr.replace('/', '÷')
            display_expr = display_expr.replace('-', '−')
            display_expr = display_expr.replace('**', '^')

            error_entry = f"{display_expr} = {error_msg}"
            if not history or history[-1] != error_entry:
                history.append(error_entry)
            return f"Erreur: {error_msg}"

    def append_char(self, char: str):
        if self.result_shown:
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

    def backspace(self, current_text: str):
        return current_text[:-1] if current_text else current_text

    def clear(self):
        self.current_expression = ""
        self.result_shown = False
        self.last_result = ""
        self.model.clear_history()
        return ""

    def undo(self):
        history = self.model.get_history()
        if history:
            history.pop()
            self.current_expression = ""
            self.result_shown = False
            self.last_result = ""
            return "0"
        return "0"

    def get_history(self):
        return self.model.get_history()

    def get_display_value(self):
        if self.result_shown and self.last_result:
            return self.last_result
        return self.current_expression if self.current_expression else "0"