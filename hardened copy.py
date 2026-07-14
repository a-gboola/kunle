"""Compatibility launcher for the hardened scientific calculator.

This file used to contain an older copy of the calculator that still used
``eval`` and did not impose numeric-result limits.  Keep one implementation
in ``hardened.py`` so running either filename uses the same safe evaluator.
"""

import tkinter as tk

from hardened import CalculatorApp


if __name__ == "__main__":
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()
