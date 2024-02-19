"""main.py"""
from calculator_controller import CalculatorController

if __name__ == '__main__':
    """display use interface"""
    app = CalculatorController()
    app.view.mainloop()
