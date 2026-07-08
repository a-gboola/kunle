import tkinter as tk
import math

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("420x600")
        self.root.configure(bg="#202020")

        # The main screen/display of the calculator
        self.display = tk.Entry(root, font=("Helvetica", 28), bg="#d4d4d2", bd=0, justify="right")
        self.display.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=25, pady=10, padx=10, sticky="nsew")

        self.create_buttons()

    def create_buttons(self):
        # We create a safe dictionary of math functions for the app to use when calculating.
        # This converts user inputs from degrees to radians automatically for trig functions.
        self.safe_env = {
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "asin": lambda x: math.degrees(math.asin(x)),
            "acos": lambda x: math.degrees(math.acos(x)),
            "atan": lambda x: math.degrees(math.atan(x)),
            "log": math.log10,      # Base 10 logarithm
            "ln": math.log,         # Natural logarithm
            "sqrt": math.sqrt,
            "fact": math.factorial,
            "pi": math.pi,
            "e": math.e
        }

        # The layout of the calculator buttons
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

        # Loop through the layout and generate the buttons dynamically
        for r, row in enumerate(buttons, start=1):
            for c, text in enumerate(row):
                
                # Style colors based on button type
                if text in ['=', 'C', 'DEL']:
                    bg_color = "#ff9500" # Orange for actions
                    fg_color = "white"
                elif text in ['/', '*', '-', '+', '^']:
                    bg_color = "#ff9500" # Orange for standard operators
                    fg_color = "white"
                elif text.isalpha() or '(' in text or ')' in text:
                    bg_color = "#505050" # Dark grey for scientific functions
                    fg_color = "white"
                else:
                    bg_color = "#d4d4d2" # Light grey for numbers
                    fg_color = "black"

                btn = tk.Button(self.root, text=text, font=("Helvetica", 16, "bold"), 
                                bg=bg_color, fg=fg_color, activebackground="#7a7a7a", 
                                borderwidth=0, cursor="hand2",
                                command=lambda t=text: self.on_button_click(t))
                btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)
                
                # Allow columns to expand evenly
                self.root.grid_columnconfigure(c, weight=1)
            
            # Allow rows to expand evenly
            self.root.grid_rowconfigure(r, weight=1)

    def on_button_click(self, char):
        """Handles what happens when a button is clicked."""
        if char == 'C':
            # Clear screen
            self.display.delete(0, tk.END)
        
        elif char == 'DEL':
            # Delete last character
            current = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, current[:-1])
        
        elif char == '=':
            # Calculate the result
            try:
                expression = self.display.get()
                
                # Python uses ** for exponents, but ^ is standard for calculators
                expression = expression.replace('^', '**')
                
                # Evaluate the math expression securely using our defined math environment
                result = eval(expression, {"__builtins__": None}, self.safe_env)
                
                self.display.delete(0, tk.END)
                
                # Clean up the output formatting
                if isinstance(result, float) and result.is_integer():
                    result = int(result) # Remove .0 from whole numbers
                elif isinstance(result, float):
                    result = round(result, 6) # Round long decimals
                    
                self.display.insert(tk.END, str(result))
            
            except Exception:
                # If the math is invalid (e.g., dividing by zero or missing a parenthesis)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        
        else:
            # Insert the button's text into the display
            self.display.insert(tk.END, char)

if __name__ == "__main__":
    # Initialize and run the application
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()