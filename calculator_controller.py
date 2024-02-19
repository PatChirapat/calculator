from calculator_model import CalculatorModel
from calculator_view import CalculatorView


class CalculatorController:
    def __init__(self):
        self.model = CalculatorModel()
        self.view = CalculatorView(self)

    def on_key_evaluate(self, key):
        if key != '=':
            self.model.add_display(key)
            self.view.display_text.set(self.model.current_display)
        else:
            if self.model.current_display and self.model.current_display[0] in self.view.function_combobox['values']:
                selected_function = self.view.function_combobox.get()
                self.on_function_evaluate(selected_function)
            else:
                self.model.evaluate_result()
                self.view.display_text.set(self.model.current_display)
                self.view.display_history('\n'.join(self.model.history))

    def on_operator_evaluate(self, operator):
        if operator == "DEL":
            self.model.delete_last_element()
        elif operator == "CLR":
            self.model.clear_display()
        elif operator == "^":
            if self.model.current_display and self.model.current_display[-1].isdigit():
                self.model.add_display("**")
        elif operator == "=":
            self.model.evaluate_result()
        else:
            self.model.add_display(operator)

        self.view.display_text.set(self.model.current_display)

    def on_function_evaluate(self, function):
        current_display = self.model.current_display

        if current_display:
            display_text = f"{function}({current_display})"
            self.view.display_text.set(display_text)

            result = self.model.calculate_function(function)

            history_entry = f"{function}({current_display}) = {result}"
            self.model.history.append(history_entry)
            self.view.display_history('\n'.join(self.model.history))
