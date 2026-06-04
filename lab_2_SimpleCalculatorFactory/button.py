from abc import ABC, abstractmethod


class Button(ABC):
    @abstractmethod
    def press(self):
        pass

    @abstractmethod
    def get_display_text(self):
        pass


class DigitButton(Button):
    def __init__(self, digit):
        self._digit = digit

    def press(self):
        return str(self._digit)

    def get_display_text(self):
        return str(self._digit)


class OperatorButton(Button):
    def __init__(self, operation):
        self._operation = operation

    def press(self):
        return self._operation

    def get_display_text(self):
        symbols = {"+": "+", "-": "−", "*": "×", "/": "÷"}
        return symbols.get(self._operation, self._operation)


class EqualsButton(Button):
    def press(self):
        return "="

    def get_display_text(self):
        return "="


class ClearButton(Button):
    def press(self):
        return "C"

    def get_display_text(self):
        return "C"


class PercentageButton(Button):
    def press(self):
        return "%"

    def get_display_text(self):
        return "%"


class SignButton(Button):
    def press(self):
        return "±"

    def get_display_text(self):
        return "±"


class SquareButton(Button):
    def press(self):
        return "x²"

    def get_display_text(self):
        return "x²"


class DecimalButton(Button):
    def press(self):
        return "."

    def get_display_text(self):
        return "."


class SinButton(Button):
    def press(self):
        return "sin"

    def get_display_text(self):
        return "sin"


class CosButton(Button):
    def press(self):
        return "cos"

    def get_display_text(self):
        return "cos"


class TanButton(Button):
    def press(self):
        return "tan"

    def get_display_text(self):
        return "tan"


class LnButton(Button):
    def press(self):
        return "ln"

    def get_display_text(self):
        return "ln"


class LogButton(Button):
    def press(self):
        return "log"

    def get_display_text(self):
        return "log"


class SqrtButton(Button):
    def press(self):
        return "sqrt"

    def get_display_text(self):
        return "√x"


class PiButton(Button):
    def press(self):
        return "pi"

    def get_display_text(self):
        return "π"


class EButton(Button):
    def press(self):
        return "e"

    def get_display_text(self):
        return "e"


class PowerButton(Button):
    def press(self):
        return "^"

    def get_display_text(self):
        return "xʸ"