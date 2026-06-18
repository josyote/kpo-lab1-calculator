import math

class CalculatorModel:
    def evaluate(self, expression: str) -> float:
        try:
            # Remplacement des symboles pour eval
            expr = expression.replace('×', '*').replace('−', '-').replace('x^y', '**')
            return eval(expr, {"__builtins__": None}, {"sin": math.sin, "cos": math.cos, "tan": math.tan, "ln": math.log, "sqrt": math.sqrt, "pi": math.pi, "e": math.e, "log": math.log10})
        except Exception as e:
            raise ValueError(f"Erreur de calcul : {str(e)}")

    def apply_function(self, func: str, value: float) -> float:
        try:
            if func == 'sin':
                return math.sin(value)
            elif func == 'cos':
                return math.cos(value)
            elif func == 'tan':
                return math.tan(value)
            elif func == 'ln':
                return math.log(value)
            elif func == '√':
                return math.sqrt(value)
            elif func == 'log':
                return math.log10(value)
            else:
                raise ValueError("Fonction non supportée")
        except Exception as e:
            raise ValueError(f"Erreur dans la fonction {func} : {str(e)}")