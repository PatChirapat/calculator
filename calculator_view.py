import tkinter as tk
from tkinter import ttk

class CalculatorView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.title("Calculator")
        self.controller = controller
        self.display_text = tk.StringVar()
        self.init_components()

    def init_components(self) -> None:
        # display
        display_frame = self.make_display()

        # history
        history_frame = self.make_history_pad()

        # function
        function_frame = self.make_functions_pad()

        # keypad
        keypad_frame = self.make_keypad()

        # operators
        operator_frame = self.make_operator_pad()

        # stick together both x, y coordinates
        display_frame.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
        history_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        function_frame.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW)
        keypad_frame.grid(row=3, column=0, sticky=tk.NSEW)
        operator_frame.grid(row=3, column=1, sticky=tk.NSEW)

        # expand x, y coordinates
        for i in range(4):
            self.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)

    def make_keypad(self) -> ttk.Frame:
        keypad_frame = ttk.Frame(self)
        keys = list('7894561230.=')
        for index, value in enumerate(keys):
            keypad_row = index // 3
            keypad_col = index % 3
            keypad_button = tk.Button(keypad_frame, text=value, bg="grey",
                                        fg="black", command=lambda
                                        v=value: self.controller.on_key_evaluate(v))
            keypad_button.grid(row=keypad_row, column=keypad_col,
                               sticky=tk.NSEW)

        for i in range(4):
            keypad_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            keypad_frame.grid_columnconfigure(i, weight=1)

        return keypad_frame

    def make_operator_pad(self) -> ttk.Frame:
        operator_frame = ttk.Frame(self)
        operators = ["DEL", "CLR", "*", "/", "+", "-", "^", "(", ")", "mod"]
        for index, values in enumerate(operators):
            operator_row = index
            operator_col = 0
            operator_button = tk.Button(operator_frame, text=values,
                                        bg="orange", fg="black",
                                        command=lambda v=values:
                                        self.controller.on_operator_evaluate(v)
                                        if v != "="
                                        else self.controller.calculate())
            operator_button.grid(row=operator_row, column=operator_col,
                                 sticky=tk.NSEW)

        for i in range(len(operators)):
            operator_frame.grid_rowconfigure(i, weight=1)
            operator_frame.grid_columnconfigure(0, weight=1)

        return operator_frame

    def make_functions_pad(self) -> ttk.Frame:
        function_frame = ttk.Frame(self)
        functions = ["EXP", "ln", "log10", "log2", "sqrt", "!"]
        self.function_combobox = ttk.Combobox(function_frame, values=functions, state='readonly')
        self.function_combobox.grid(row=0, column=0, sticky='news')
        self.function_combobox.current(0)
        self.function_combobox.bind("<<ComboboxSelected>>", self.function_calculation)

        for i in range(len(functions)):
            function_frame.grid_rowconfigure(i, weight=1)
        function_frame.grid_columnconfigure(0, weight=1)

        return function_frame

    def make_history_pad(self) -> ttk.Frame:
        history_frame = ttk.Frame(self)
        history_label = ttk.Label(history_frame, text="History:",
                                  font=('Arial', 12))
        history_label.grid(row=0, column=0, sticky="w")
        self.history_text = tk.Text(history_frame, height=4, width=50,
                                    state='disabled')
        self.history_text.grid(row=1, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(history_frame,
                                  command=self.history_text.yview)
        scrollbar.grid(row=1, column=1, sticky='ns')
        self.history_text['yscrollcommand'] = scrollbar.set

        history_frame.grid_columnconfigure(0, weight=1)
        history_frame.grid_columnconfigure(1, weight=0)

        return history_frame

    def make_display(self) -> ttk.Frame:
        display_frame = ttk.Frame(self)
        display_frame.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
        self.display_entry = tk.Entry(display_frame, textvariable=self.display_text,
                                      font=('Arial', 16), justify='right',
                                      state='readonly', bg="black", fg="yellow")
        self.display_entry.grid(row=0, column=0, sticky="nsew")
        display_frame.grid_columnconfigure(0, weight=1)
        return display_frame

    def function_calculation(self, event):
        selected_function = self.function_combobox.get()
        self.controller.on_function_evaluate(selected_function)

    def display_history(self, history):
        self.history_text.config(state='normal')
        self.history_text.delete('1.0', tk.END)
        self.history_text.insert(tk.END, history)
        self.history_text.config(state='disabled')

    def display_error(self, message):
        self.display_text.set(message)
        self.after(1500, self.controller.on_operator_evaluate, "CLR")