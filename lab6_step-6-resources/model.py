from operations import OperationFactory
import math


class CalculatorModel:
    def __init__(self):
        self.operation_factory = OperationFactory()

    def evaluate(self, expression: str) -> float:
        try:
            # Normalisation de l'expression
            expr = expression.replace('×', '*')
            expr = expr.replace('÷', '/')
            expr = expr.replace('−', '-')
            expr = expr.replace('^', '**')
            expr = expr.replace('√', 'math.sqrt')
            expr = expr.replace('sin', 'math.sin')
            expr = expr.replace('cos', 'math.cos')
            expr = expr.replace('tan', 'math.tan')
            expr = expr.replace('ln', 'math.log')
            expr = expr.replace('π', 'math.pi')
            expr = expr.replace('e', 'math.e')
            expr = expr.replace(' ', '')

            if not expr:
                return 0.0

            result = eval(expr, {"math": math, "__builtins__": {}})

            if isinstance(result, float):
                if result.is_integer():
                    return float(int(result))
                return round(result, 8)
            return float(result)

        except ZeroDivisionError:
            raise ValueError("Division par zéro impossible")
        except Exception as e:
            raise ValueError(f"Erreur de calcul: {str(e)}")