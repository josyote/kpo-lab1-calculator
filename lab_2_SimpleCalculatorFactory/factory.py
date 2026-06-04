from button import *
from abc import ABC, abstractmethod

class ButtonFactory(ABC):
    @abstractmethod
    def create_button(self, button_type, value=None):
        pass

class CalculatorButtonFactory(ButtonFactory):
    def create_button(self, button_type, value=None):
        if button_type == "digit":
            return DigitButton(value)
        elif button_type == "operator":
            return OperatorButton(value)
        elif button_type == "equals":
            return EqualsButton()
        elif button_type == "clear":
            return ClearButton()
        elif button_type == "percentage":
            return PercentageButton()
        elif button_type == "sign":
            return SignButton()
        elif button_type == "square":
            return SquareButton()
        # Dans factory.py, ajoutez dans la méthode create_button:
        elif button_type == "decimal":
            return DecimalButton()
        else:
            raise ValueError(f"Type de bouton inconnu: {button_type}")