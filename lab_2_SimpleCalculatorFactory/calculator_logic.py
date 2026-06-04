import math


class CalculatorLogic:
    def __init__(self):
        self.current_input = "0"
        self.previous_input = ""
        self.operation = None
        self.new_number = True
        self.pending_power = None

    def add_digit(self, digit):
        if self.new_number or self.current_input == "0":
            self.current_input = str(digit)
            self.new_number = False
        else:
            self.current_input += str(digit)
        return self.current_input

    def add_decimal(self):
        if self.new_number:
            self.current_input = "0."
            self.new_number = False
        elif "." not in self.current_input:
            self.current_input += "."
        return self.current_input

    def set_operation(self, op):
        if self.current_input and not self.new_number:
            self.previous_input = self.current_input
            self.operation = op
            self.new_number = True
        return self.current_input

    def calculate(self):
        if not self.operation or not self.previous_input:
            return self.current_input

        try:
            num1 = float(self.previous_input)
            num2 = float(self.current_input)
            result = 0

            if self.operation == "+":
                result = num1 + num2
            elif self.operation == "-":
                result = num1 - num2
            elif self.operation == "*":
                result = num1 * num2
            elif self.operation == "/":
                if num2 == 0:
                    return "Error"
                result = num1 / num2

            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 10)

            self.current_input = str(result)
            self.operation = None
            self.previous_input = ""
            self.new_number = True
            return self.current_input
        except:
            return "Error"

    def clear(self):
        self.current_input = "0"
        self.previous_input = ""
        self.operation = None
        self.new_number = True
        self.pending_power = None
        return self.current_input

    def toggle_sign(self):
        if self.current_input != "0":
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
        return self.current_input

    def percentage(self):
        try:
            value = float(self.current_input) / 100
            self.current_input = str(int(value) if value.is_integer() else value)
            self.new_number = True
            return self.current_input
        except:
            return self.current_input

    def square(self):
        try:
            value = float(self.current_input) ** 2
            self.current_input = str(int(value) if value.is_integer() else value)
            self.new_number = True
            return self.current_input
        except:
            return self.current_input

    def add_sine(self):
        try:
            value = float(self.current_input)
            result = math.sin(value)
            self.current_input = str(result if result.is_integer() else round(result, 10))
            self.new_number = True
            return self.current_input
        except:
            return "Error"

    def add_cosine(self):
        try:
            value = float(self.current_input)
            result = math.cos(value)
            self.current_input = str(result if result.is_integer() else round(result, 10))
            self.new_number = True
            return self.current_input
        except:
            return "Error"

    def add_tangent(self):
        try:
            value = float(self.current_input)
            result = math.tan(value)
            self.current_input = str(result if result.is_integer() else round(result, 10))
            self.new_number = True
            return self.current_input
        except:
            return "Error"

    def add_ln(self):
        try:
            value = float(self.current_input)
            if value <= 0:
                return "Error"
            result = math.log(value)
            self.current_input = str(result if result.is_integer() else round(result, 10))
            self.new_number = True
            return self.current_input
        except:
            return "Error"

    def add_log10(self):
        try:
            value = float(self.current_input)
            if value <= 0:
                return "Error"
            result = math.log10(value)
            self.current_input = str(result if result.is_integer() else round(result, 10))
            self.new_number = True
            return self.current_input
        except:
            return "Error"

    def add_square_root(self):
        try:
            value = float(self.current_input)
            if value < 0:
                return "Error"
            result = math.sqrt(value)
            self.current_input = str(result if result.is_integer() else round(result, 10))
            self.new_number = True
            return self.current_input
        except:
            return "Error"

    def add_pi(self):
        self.current_input = str(math.pi)
        self.new_number = True
        return self.current_input

    def add_e(self):
        self.current_input = str(math.e)
        self.new_number = True
        return self.current_input

    def add_power(self):
        if self.pending_power is None:
            self.pending_power = float(self.current_input)
            self.current_input = "0"
            self.new_number = True
            return "x^y"
        else:
            try:
                x = self.pending_power
                y = float(self.current_input)
                result = x ** y
                self.current_input = str(int(result) if result.is_integer() else round(result, 10))
                self.pending_power = None
                self.new_number = True
                return self.current_input
            except:
                self.pending_power = None
                return "Error"

    def get_display(self):
        return self.current_input