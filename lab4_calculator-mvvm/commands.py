from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self) -> float:
        pass

    @abstractmethod
    def undo(self) -> float:
        pass

class AddCommand(Command):
    def __init__(self, receiver, expression: str):
        self.receiver = receiver
        self.expression = expression
        self.result = None

    def execute(self) -> float:
        self.result = self.receiver.evaluate(self.expression)
        return self.result

    def undo(self) -> float:
        return 0  # Retourne une réinitialisation ou une valeur par défaut

class FunctionCommand(Command):
    def __init__(self, receiver, func: str, value: float):
        self.receiver = receiver
        self.func = func
        self.value = value
        self.result = None

    def execute(self) -> float:
        self.result = self.receiver.apply_function(self.func, self.value)
        return self.result

    def undo(self) -> float:
        return 0  # Réinitialisation