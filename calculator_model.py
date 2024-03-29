"""model for the calculator application."""
import math


class CalculatorModel:
    def __init__(self):
        self.current_display = ""
        self.history = []
        self.keys = list('7894561230.=')
        self.operators = ["DEL", "CLR", "*", "/", "-", "^", "(", ")", "mod"]
        self.functions = {
            "EXP": lambda x: math.exp(float(x)),
            "ln": lambda x: math.log(float(x)),
            "log10": lambda x: math.log10(float(x)),
            "log2": lambda x: math.log2(float(x)),
            "sqrt": lambda x: math.sqrt(float(x)),
            "!": lambda x: math.factorial(int(x))
        }

    def add_display(self, value):
        """add value"""
        self.current_display += str(value)

    def add_decimal(self):
        """add decimal point"""
        if "." not in self.current_display:
            self.current_display += "."

    def calculate_operator(self, operator):
        """calculate operator"""
        if operator in self.operators:
            self.current_display += operator

    def calculate_function(self, func):
        """calculate function"""
        try:
            if func in self.functions:
                if func == "sqrt":
                    if self.current_display:
                        result = self.functions[func](eval(self.current_display))
                        self.current_display = str(result)
                        return result
                else:
                    result = self.functions[func](float(self.current_display))
                    self.current_display = str(result)
                    return result
        except Exception as e:
            raise ValueError("Invalid expression")

    def delete_last_element(self):
        """delete last element"""
        if len(self.current_display) != 0:
            if self.current_display[-1] in self.operators:
                self.current_display = self.current_display[:-1]
            else:
                while self.current_display and not self.current_display[-1].isdigit():
                    self.current_display = self.current_display[:-1]
                self.current_display = self.current_display[:-1]

    def clear_display(self):
        """clear display"""
        self.current_display = ""

    def evaluate_result(self):
        """evaluate result"""
        try:
            result = eval(self.current_display)
            self.history.append(self.current_display + " = " + str(result))
            self.current_display = str(result)
        except Exception as e:
            raise ValueError("Invalid expression")
