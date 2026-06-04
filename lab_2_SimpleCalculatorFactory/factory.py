from button import *

class CalculatorButtonFactory:
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
        elif button_type == "decimal":
            return DecimalButton()
        elif button_type == "sin":
            return SinButton()
        elif button_type == "cos":
            return CosButton()
        elif button_type == "tan":
            return TanButton()
        elif button_type == "ln":
            return LnButton()
        elif button_type == "log":
            return LogButton()
        elif button_type == "sqrt":
            return SqrtButton()
        elif button_type == "pi":
            return PiButton()
        elif button_type == "e":
            return EButton()
        elif button_type == "power":
            return PowerButton()
        else:
            raise ValueError(f"Type de bouton inconnu: {button_type}")