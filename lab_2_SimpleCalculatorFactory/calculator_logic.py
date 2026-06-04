class CalculatorLogic:
    def __init__(self):
        self.current_input = "0"
        self.previous_input = ""
        self.operation = None
        self.new_number = True

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

    def get_display(self):
        return self.current_input