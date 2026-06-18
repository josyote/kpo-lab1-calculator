from decorators import CalculatorComponent, BaseCalculator, HistoryDecorator, FormattingDecorator, ValidationDecorator


class CalculatorModel:
    def __init__(self):
        # Création de la calculatrice de base
        self.base_calculator = BaseCalculator()

        # Application des décorateurs
        # L'ordre est important : Validation -> Formatting -> History
        self.history = []
        self.calculator = ValidationDecorator(
            FormattingDecorator(
                HistoryDecorator(self.base_calculator, self.history)
            )
        )

    def calculate(self, expression: str) -> float:
        return self.calculator.calculate(expression)

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []