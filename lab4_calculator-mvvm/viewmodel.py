from model import CalculatorModel
from commands import AddCommand, FunctionCommand

class CalculatorViewModel:
    def __init__(self):
        self.model = CalculatorModel()
        self.history = []
        self.command_history = []

    def calculate(self, expression: str):
        try:
            # Vérifier si l'expression contient une fonction (sin, cos, etc.)
            if any(func in expression for func in ['sin', 'cos', 'tan', 'ln', '√', 'log']):
                # Extraction de la fonction et de la valeur
                for func in ['sin', 'cos', 'tan', 'ln', '√', 'log']:
                    if func in expression:
                        value = float(expression.replace(func, '').strip('()'))
                        command = FunctionCommand(self.model, func, value)
                        break
            else:
                command = AddCommand(self.model, expression)

            result = command.execute()
            self.command_history.append(command)
            self.history.append(f"{expression} = {result}")
            return str(result)
        except Exception as e:
            self.history.append(f"{expression} = Erreur: {str(e)}")
            return f"Erreur: {str(e)}"

    def backspace(self, current_text: str):
        return current_text[:-1] if current_text else current_text

    def clear(self):
        self.history = []
        self.command_history = []
        return ""

    def undo(self):
        if not self.command_history:
            return "0"
        last_command = self.command_history.pop()
        result = last_command.undo()
        self.history.append(f"Undo: {result}")
        return str(result)