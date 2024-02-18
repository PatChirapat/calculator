import tkinter as tk


class CalculatorView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.display_text = tk.StringVar()
        self.init_components()

    def init_components(self):
        pass

    def make_kypad(self):
        pass

    def make_operator_pad(self):
        pass

    def key_pressed(self, value):
        pass