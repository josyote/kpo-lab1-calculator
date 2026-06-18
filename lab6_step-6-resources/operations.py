from abc import ABC, abstractmethod
import math

# Classe abstraite d'opération
class Operation(ABC):
    @abstractmethod
    def execute(self, a, b=None):
        pass

# Opérations concrètes
class Addition(Operation):
    def execute(self, a, b):
        return a + b

class Subtraction(Operation):
    def execute(self, a, b):
        return a - b

class Multiplication(Operation):
    def execute(self, a, b):
        return a * b

class Division(Operation):
    def execute(self, a, b):
        if b == 0:
            raise ValueError("Division par zéro!")
        return a / b

class Modulo(Operation):
    def execute(self, a, b):
        return a % b

class Power(Operation):
    def execute(self, a, b):
        return a ** b

class SquareRoot(Operation):
    def execute(self, a, b=None):
        if a < 0:
            raise ValueError("Racine carrée d'un nombre négatif!")
        return math.sqrt(a)

class Sine(Operation):
    def execute(self, a, b=None):
        return math.sin(a)

class Cosine(Operation):
    def execute(self, a, b=None):
        return math.cos(a)

class Tangent(Operation):
    def execute(self, a, b=None):
        return math.tan(a)

class NaturalLog(Operation):
    def execute(self, a, b=None):
        if a <= 0:
            raise ValueError("Logarithme non défini pour les nombres non positifs!")
        return math.log(a)


class OperationFactory:
    @staticmethod
    def create_operation(op_type):
        operations = {
            '+': Addition,
            '-': Subtraction,
            '*': Multiplication,
            '/': Division,
            '%': Modulo,
            '^': Power,
            '√': SquareRoot,
            'sin': Sine,
            'cos': Cosine,
            'tan': Tangent,
            'ln': NaturalLog
        }
        return operations.get(op_type)()