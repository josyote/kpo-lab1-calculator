from abc import ABC, abstractmethod
from math import sin, cos, tan, log, sqrt, pi, log10, pow
import re


class CalculatorComponent(ABC):
    """Composant abstrait pour le pattern Decorator"""

    @abstractmethod
    def calculate(self, expression: str) -> float:
        pass


class BaseCalculator(CalculatorComponent):
    """Composant concret - Calculatrice de base"""

    def calculate(self, expression: str) -> float:
        try:
            # Sauvegarder l'expression originale pour l'historique
            original_expression = expression

            # Préparation de l'expression
            expr = expression

            # Remplacer les symboles d'affichage par les vrais opérateurs
            expr = expr.replace('×', '*')
            expr = expr.replace('÷', '/')
            expr = expr.replace('−', '-')
            expr = expr.replace('√', 'sqrt')
            expr = expr.replace('^', '**')
            expr = expr.replace('x^y', '**')
            expr = expr.replace(' ', '')

            # Vérification des parenthèses
            if expr.count('(') != expr.count(')'):
                raise ValueError("Parenthèses non équilibrées")

            # Environnement sécurisé avec constantes mathématiques
            safe_dict = {
                'sin': sin, 'cos': cos, 'tan': tan,
                'ln': log, 'sqrt': sqrt,
                'pi': pi, 'e': 2.718281828459045,
                'log': log10
            }

            if not expr:
                return 0.0

            result = eval(expr, {"__builtins__": None}, safe_dict)

            if isinstance(result, float):
                if result.is_integer():
                    return float(int(result))
                return round(result, 10)
            return float(result)

        except ZeroDivisionError:
            raise ValueError("Division par zéro impossible")
        except SyntaxError:
            raise ValueError("Expression invalide")
        except Exception as e:
            raise ValueError(f"Erreur de calcul : {str(e)}")


class HistoryDecorator(CalculatorComponent):
    """Décorateur pour ajouter l'historique"""

    def __init__(self, calculator: CalculatorComponent, history: list):
        self.calculator = calculator
        self.history = history

    def calculate(self, expression: str) -> float:
        result = self.calculator.calculate(expression)

        # Formater l'expression pour l'affichage
        display_expr = expression
        display_expr = display_expr.replace('*', '×')
        display_expr = display_expr.replace('/', '÷')
        display_expr = display_expr.replace('-', '−')
        display_expr = display_expr.replace('**', '^')

        # Formater le résultat
        if isinstance(result, float):
            if result.is_integer():
                result_str = str(int(result))
            else:
                result_str = str(round(result, 8))
        else:
            result_str = str(result)

        history_entry = f"{display_expr} = {result_str}"

        # Éviter les doublons
        if not self.history or self.history[-1] != history_entry:
            self.history.append(history_entry)
            if len(self.history) > 20:
                self.history = self.history[-20:]

        return result


class FormattingDecorator(CalculatorComponent):
    """Décorateur pour formater les résultats"""

    def __init__(self, calculator: CalculatorComponent):
        self.calculator = calculator

    def calculate(self, expression: str) -> float:
        result = self.calculator.calculate(expression)

        if isinstance(result, float):
            if result.is_integer():
                return float(int(result))
            return round(result, 8)
        return result


class ValidationDecorator(CalculatorComponent):
    """Décorateur pour valider les expressions"""

    def __init__(self, calculator: CalculatorComponent):
        self.calculator = calculator

    def calculate(self, expression: str) -> float:
        # Vérifier les parenthèses équilibrées
        if expression.count('(') != expression.count(')'):
            raise ValueError("Parenthèses non équilibrées")

        # Vérifier les opérateurs consécutifs
        if re.search(r'[\+\-\*/]{2,}', expression.replace('−', '-').replace('×', '*').replace('÷', '/')):
            raise ValueError("Opérateurs consécutifs non autorisés")

        return self.calculator.calculate(expression)