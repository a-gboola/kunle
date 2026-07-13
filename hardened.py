import tkinter as tk
import math
import re

# ---- Security constants ----
MAX_INPUT_LENGTH = 50          # Prevents absurdly long expressions (basic DoS protection)
MAX_FACTORIAL_INPUT = 170      # math.factorial(171) already overflows a float; this keeps it fast and safe
ALLOWED_CHARS_PATTERN = re.compile(r'^[0-9a-z\.\+\-\*/\(\)\^\s]*$')  # Whitelist: only characters our buttons can produce


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("420x600")
        self.root.configure(bg="#202020")

        self.display = tk.Entry(root, font=("Helvetica", 28), bg="#d4d4d2", bd=0, justify="right")
        self.display.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=25, pady=10, padx=10, sticky="nsew")

        self.create_buttons()

    def safe_factorial(self, n):
        """
        Wraps math.factorial with limits so a huge or invalid number
        can't freeze the app or throw an ugly, unhandled crash.
        """
        if n < 0:
            raise ValueError("Factorial of a negative number is undefined")
        if n != int(n):
            raise ValueError("Factorial only works on whole numbers")
        if n > MAX_FACTORIAL_INPUT:
            raise OverflowError("Number too large for factorial")
        return math.factorial(int(n))

    def create_buttons(self):
        # Safe dictionary of math functions available to eval().
        # __builtins__ is disabled below, so this dict is the ONLY thing eval() can call.
        self.safe_env = {
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
            "pi": math.pi,
            "e": math.e
        }

        buttons = [
            ('C', 'DEL', '(', ')'),
            ('sin(', 'cos(', 'tan(', '/'),
            ('asin(', 'acos(', 'atan(', '*'),
            ('7', '8', '9', '-'),
            ('4', '5', '6', '+'),
            ('1', '2', '3', '^'),
            ('log(', 'ln(', 'sqrt(', 'fact('),
            ('0', '.', 'pi', '=')
        ]

        for r, row in enumerate(buttons, start=1):
            for c, text in enumerate(row):
                if text in ['=', 'C', 'DEL']:
                    bg_color = "#ff9500"
                    fg_color = "white"
                elif text in ['/', '*', '-', '+', '^']:
                    bg_color = "#ff9500"
                    fg_color = "white"
                elif text.isalpha() or '(' in text or ')' in text:
                    bg_color = "#505050"
                    fg_color = "white"
                else:
                    bg_color = "#d4d4d2"
                    fg_color = "black"

                btn = tk.Button(self.root, text=text, font=("Helvetica", 16, "bold"),
                                bg=bg_color, fg=fg_color, activebackground="#7a7a7a",
                                borderwidth=0, cursor="hand2",
                                command=lambda t=text: self.on_button_click(t))
                btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)
                self.root.grid_columnconfigure(c, weight=1)
            self.root.grid_rowconfigure(r, weight=1)

    def show_error(self, message="Error"):
        """Clears the display and shows a short, safe error message (no internal details leaked)."""
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, message)

    def on_button_click(self, char):
        if char == 'C':
            self.display.delete(0, tk.END)

        elif char == 'DEL':
            current = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, current[:-1])

        elif char == '=':
            expression = self.display.get()

            # --- Security check 1: reject empty input ---
            if not expression:
                return

            # --- Security check 2: reject overly long input (DoS protection) ---
            if len(expression) > MAX_INPUT_LENGTH:
                self.show_error("Too long")
                return

            # --- Security check 3: whitelist check BEFORE eval() ever runs ---
            # Even though eval() below is restricted, this is a second layer of
            # defense: if a character isn't one our buttons can produce, refuse it.
            if not ALLOWED_CHARS_PATTERN.match(expression):
                self.show_error("Invalid input")
                return

            expression = expression.replace('^', '**')

            try:
                result = eval(expression, {"__builtins__": None}, self.safe_env)

                if isinstance(result, complex):
                    # e.g. sqrt of a negative number
                    raise ValueError("Result is not a real number")

                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                elif isinstance(result, float):
                    result = round(result, 6)

                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))

            except ZeroDivisionError:
                self.show_error("Cannot divide by 0")
            except ValueError as e:
                self.show_error(str(e) if str(e) else "Invalid value")
            except OverflowError:
                self.show_error("Number too large")
            except SyntaxError:
                self.show_error("Invalid expression")
            except Exception:
                # Catch-all for anything unexpected; never show raw Python error details to the user
                self.show_error("Error")

        else:
            # --- Security check 4: don't let input grow past the limit while typing ---
            if len(self.display.get()) >= MAX_INPUT_LENGTH:
                return
            self.display.insert(tk.END, char)


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()