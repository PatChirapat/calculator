"""controller for the calculator"""
from calculator_model import CalculatorModel
from calculator_view import CalculatorView


class CalculatorController:
    def __init__(self):
        self.model = CalculatorModel()
        self.view = CalculatorView(self)

    def on_key_evaluate(self, key):
        """handle the evaluation of the key"""
        if key != '=':
            self.model.add_display(key)
            self.view.display_text.set(self.model.current_display)
        else:
            expression = self.model.current_display

            if any(op in expression for op in
                   self.view.function_combobox['values']):
                selected_function = self.view.function_combobox.get()
                self.on_function_evaluate(selected_function)
            else:
                try:
                    result = eval(expression)
                    self.view.display_text.set(result)
                    history_entry = f"{expression} = {result}\n"
                    self.model.history.append(history_entry)
                    self.view.display_history(history_entry)
                    self.model.clear_display()
                    self.view.display_entry.config(bg="black", fg="yellow")
                except Exception as e:
                    self.view.display_text.set("Error")
                    self.view.display_entry.config(bg="red", fg="red")
                    self.view.display_error("Invalid expression")
                    self.view.play_error_sound()
                    self.view.after(1500, self.view.stop_error_sound)
                    self.view.after(1500, self.view.display_entry.config,
                                    {"bg": "black", "fg": "yellow"})

    def on_operator_evaluate(self, operator):
        """handle the evaluation of the operator"""
        if operator == "DEL":
            self.model.delete_last_element()
        elif operator == "CLR":
            self.model.clear_display()
        elif operator == "^":
            if self.model.current_display and self.model.current_display[-1].isdigit():
                self.model.add_display("**")
        elif operator == "mod":
            self.model.add_display("%")
        elif operator == "=":
            self.model.evaluate_result()
        else:
            self.model.add_display(operator)

        self.view.display_text.set(self.model.current_display)

    def on_function_evaluate(self, function):
        """handle the evaluation of the function"""
        current_display = self.model.current_display

        if current_display:
            display_text = f"{function}({current_display})"
            self.view.display_text.set(display_text)

            result = self.model.calculate_function(function)

            history_entry = f"{function}({current_display}) = {result}"
            self.model.history.append(history_entry)
            self.view.display_history('\n'.join(self.model.history))
