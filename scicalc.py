"""Secure scientific calculator (Tkinter).

The expression evaluator deliberately does not use ``eval``.  It evaluates a
small, documented maths language so pasted input cannot run Python code.
"""

import ast
import math
import operator
import re
import tkinter as tk


MAX_INPUT_LENGTH = 50
MAX_AST_NODES = 100
MAX_AST_DEPTH = 25
MAX_FACTORIAL_INPUT = 170
MAX_POWER_EXPONENT = 10_000
MAX_INTEGER_BITS = 1024
ALLOWED_CHARS_PATTERN = re.compile(r"^[0-9a-z\.\+\-\*/\(\)\^\s]*$")


class CalculatorError(Exception):
    """An expected error that is safe to show in the calculator display."""


class ExpressionEvaluator:
    """Safely evaluate calculator expressions without executing Python."""

    BINARY_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
    }
    UNARY_OPERATORS = {ast.UAdd: operator.pos, ast.USub: operator.neg}

    def __init__(self):
        # Trigonometric input/output is in degrees, like most school calculators.
        self.functions = {
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "asin": lambda x: math.degrees(math.asin(x)),
            "acos": lambda x: math.degrees(math.acos(x)),
            "atan": lambda x: math.degrees(math.atan(x)),
            "log": math.log10,
            "ln": math.log,
            "sqrt": math.sqrt,
            "fact": self.safe_factorial,
        }
        self.constants = {"pi": math.pi, "e": math.e}

    @staticmethod
    def safe_factorial(value):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise CalculatorError("Factorial requires a number")
        if not math.isfinite(value) or value > MAX_FACTORIAL_INPUT:
            raise CalculatorError("Number too large for factorial")
        if value < 0:
            raise CalculatorError("Factorial of a negative number is undefined")
        if isinstance(value, float) and not value.is_integer():
            raise CalculatorError("Factorial only works on whole numbers")
        return math.factorial(int(value))

    @staticmethod
    def _check_number(value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise CalculatorError("Invalid value")
        if isinstance(value, float) and not math.isfinite(value):
            raise CalculatorError("Number too large")
        if isinstance(value, int) and value.bit_length() > MAX_INTEGER_BITS:
            raise CalculatorError("Number too large")
        return value

    def evaluate(self, expression):
        if not isinstance(expression, str) or not expression.strip():
            raise CalculatorError("Invalid expression")
        if len(expression) > MAX_INPUT_LENGTH:
            raise CalculatorError("Input is too long")
        if not ALLOWED_CHARS_PATTERN.fullmatch(expression):
            raise CalculatorError("Invalid input")
        try:
            tree = ast.parse(expression.replace("^", "**"), mode="eval")
        except (SyntaxError, ValueError, MemoryError) as error:
            raise CalculatorError("Invalid expression") from error

        if len(list(ast.walk(tree))) > MAX_AST_NODES or self._depth(tree) > MAX_AST_DEPTH:
            raise CalculatorError("Expression is too complex")
        return self._check_number(self._evaluate_node(tree.body))

    def _depth(self, node):
        children = list(ast.iter_child_nodes(node))
        return 1 + max((self._depth(child) for child in children), default=0)

    def _evaluate_node(self, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
                raise CalculatorError("Invalid value")
            return self._check_number(node.value)
        if isinstance(node, ast.Name):
            if node.id not in self.constants:
                raise CalculatorError("Invalid input")
            return self.constants[node.id]
        if isinstance(node, ast.UnaryOp) and type(node.op) in self.UNARY_OPERATORS:
            return self._check_number(self.UNARY_OPERATORS[type(node.op)](self._evaluate_node(node.operand)))
        if isinstance(node, ast.BinOp) and type(node.op) in self.BINARY_OPERATORS:
            left, right = self._evaluate_node(node.left), self._evaluate_node(node.right)
            if isinstance(node.op, ast.Pow):
                self._check_power(left, right)
            try:
                return self._check_number(self.BINARY_OPERATORS[type(node.op)](left, right))
            except ZeroDivisionError as error:
                raise CalculatorError("Cannot divide by 0") from error
            except OverflowError as error:
                raise CalculatorError("Number too large") from error
            except ValueError as error:
                raise CalculatorError("Invalid value") from error
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id not in self.functions or node.keywords or len(node.args) != 1:
                raise CalculatorError("Invalid function")
            try:
                return self._check_number(self.functions[node.func.id](self._evaluate_node(node.args[0])))
            except CalculatorError:
                raise
            except (ValueError, OverflowError) as error:
                raise CalculatorError("Invalid value") from error
        raise CalculatorError("Invalid expression")

    @staticmethod
    def _check_power(base, exponent):
        if abs(exponent) > MAX_POWER_EXPONENT:
            raise CalculatorError("Exponent too large")
        if base == 0 and exponent < 0:
            raise CalculatorError("Cannot divide by 0")
        if isinstance(base, int) and isinstance(exponent, int) and exponent >= 0:
            if base not in (-1, 0, 1) and base.bit_length() * exponent > MAX_INTEGER_BITS:
                raise CalculatorError("Number too large")


class CalculatorApp:
    """The Tkinter user interface for the secure expression evaluator."""

    def __init__(self, root):
        self.root = root
        root.title("Secure Scientific Calculator")
        root.geometry("420x600")
        root.configure(bg="#202020")
        self.evaluator = ExpressionEvaluator()
        self.display = tk.Entry(root, font=("Helvetica", 28), bg="#d4d4d2", bd=0, justify="right")
        self.display.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=25, padx=10, pady=10, sticky="nsew")
        self.display.bind("<Return>", lambda _event: self.calculate())
        self.create_buttons()

    def create_buttons(self):
        buttons = [
            ("C", "DEL", "(", ")"), ("sin(", "cos(", "tan(", "/"),
            ("asin(", "acos(", "atan(", "*"), ("7", "8", "9", "-"),
            ("4", "5", "6", "+"), ("1", "2", "3", "^"),
            ("log(", "ln(", "sqrt(", "fact("), ("0", ".", "pi", "="),
        ]
        for row_number, row in enumerate(buttons, start=1):
            for column, text in enumerate(row):
                action = text in {"=", "C", "DEL", "/", "*", "-", "+", "^"}
                function = text.isalpha() or "(" in text or text == ")"
                bg = "#ff9500" if action else "#505050" if function else "#d4d4d2"
                fg = "white" if action or function else "black"
                tk.Button(self.root, text=text, font=("Helvetica", 16, "bold"), bg=bg, fg=fg,
                          borderwidth=0, command=lambda value=text: self.on_button_click(value)).grid(
                              row=row_number, column=column, padx=2, pady=2, sticky="nsew")
                self.root.grid_columnconfigure(column, weight=1)
            self.root.grid_rowconfigure(row_number, weight=1)

    def on_button_click(self, value):
        if value == "C":
            self.display.delete(0, tk.END)
        elif value == "DEL":
            self.display.delete(len(self.display.get()) - 1, tk.END)
        elif value == "=":
            self.calculate()
        elif len(self.display.get()) + len(value) <= MAX_INPUT_LENGTH:
            self.display.insert(tk.END, value)

    def calculate(self):
        try:
            result = self.evaluator.evaluate(self.display.get())
            if isinstance(result, float):
                result = int(result) if result.is_integer() else round(result, 8)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
        except CalculatorError as error:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(error))
        except Exception:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Error")


if __name__ == "__main__":
    app_root = tk.Tk()
    CalculatorApp(app_root)
    app_root.mainloop()
