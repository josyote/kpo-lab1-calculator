import math
import re


class CalculatorModel:
    def calculate(self, expression: str) -> str:
        try:
            # Nettoyer l'expression
            expr = expression.strip()

            # Remplacer les symboles d'affichage par les vrais opérateurs
            expr = expr.replace('×', '*')
            expr = expr.replace('÷', '/')
            expr = expr.replace('−', '-')

            # Supprimer les espaces inutiles
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
            expr = expr.replace('^', '**')

            # Gérer le pourcentage
            expr = expr.replace('%', '/100')

            # Nettoyer les parenthèses vides
            expr = expr.replace('()', '')

            # Vérifier que l'expression n'est pas vide
            if not expr:
                return "0"

            # Évaluer l'expression
            result = eval(expr, {"math": math, "__builtins__": {}})

            # Formater le résultat
            if isinstance(result, float):
                if result.is_integer():
                    return str(int(result))
                return str(round(result, 10))
            return str(result)

        except ZeroDivisionError:
            return "Erreur: Division par zéro"
        except SyntaxError as e:
            return f"Erreur: Expression invalide"
        except Exception as e:
            return f"Erreur: {str(e)}"