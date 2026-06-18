import math
import re


class CalculatorModel:
    def evaluate(self, expression: str) -> float:
        """Évalue une expression mathématique"""
        try:
            # Nettoyer l'expression
            expr = expression.strip()

            # Remplacer les symboles d'affichage par les vrais opérateurs
            expr = expr.replace('×', '*')
            expr = expr.replace('÷', '/')
            expr = expr.replace('−', '-')
            expr = expr.replace('^', '**')

            # Supprimer les espaces
            expr = expr.replace(' ', '')

            # Remplacer les fonctions mathématiques
            expr = expr.replace('sin', 'math.sin')
            expr = expr.replace('cos', 'math.cos')
            expr = expr.replace('tan', 'math.tan')
            expr = expr.replace('ln', 'math.log')
            expr = expr.replace('log', 'math.log10')
            expr = expr.replace('√', 'math.sqrt')
            expr = expr.replace('π', 'math.pi')
            expr = expr.replace('e', 'math.e')

            # Gérer le pourcentage
            expr = expr.replace('%', '/100')

            # Nettoyer les parenthèses vides
            expr = expr.replace('()', '')

            if not expr:
                return 0.0

            # Évaluer l'expression
            result = eval(expr, {"math": math, "__builtins__": {}})

            if isinstance(result, float):
                if result.is_integer():
                    return float(int(result))
                return round(result, 10)
            return float(result)

        except ZeroDivisionError:
            raise ValueError("Division par zéro impossible")
        except Exception as e:
            raise ValueError(f"Expression invalide: {str(e)}")

    def apply_function(self, func: str, value: float) -> float:
        """Applique une fonction mathématique à une valeur"""
        try:
            func_map = {
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'ln': math.log,
                '√': math.sqrt,
                'log': math.log10,
                'pi': lambda x: math.pi,
                'e': lambda x: math.e,
            }

            if func in func_map:
                result = func_map[func](value)
                if isinstance(result, float):
                    if result.is_integer():
                        return float(int(result))
                    return round(result, 10)
                return float(result)
            else:
                raise ValueError(f"Fonction non supportée: {func}")

        except Exception as e:
            raise ValueError(f"Erreur dans la fonction {func}: {str(e)}")