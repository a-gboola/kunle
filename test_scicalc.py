"""Tests for the secure scientific calculator."""

import unittest

from scicalc import CalculatorError, ExpressionEvaluator, MAX_INPUT_LENGTH


class ExpressionEvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.calculator = ExpressionEvaluator()

    def assert_calculator_error(self, expression, message):
        with self.assertRaisesRegex(CalculatorError, message):
            self.calculator.evaluate(expression)

    def test_scientific_functions(self):
        self.assertEqual(self.calculator.evaluate("2 + 3 * 4"), 14)
        self.assertEqual(self.calculator.evaluate("fact(5)"), 120)
        self.assertAlmostEqual(self.calculator.evaluate("sin(90)"), 1.0)
        self.assertAlmostEqual(self.calculator.evaluate("sqrt(81) + log(100)"), 11.0)

    def test_rejects_code_execution_attempts(self):
        self.assert_calculator_error("__import__('os').system('whoami')", "Invalid input")
        self.assert_calculator_error("(1).__class__", "Invalid input")
        self.assert_calculator_error("lambda: 1", "Invalid input")

    def test_handles_edge_cases_and_overflow(self):
        self.assert_calculator_error("1 / 0", "Cannot divide by 0")
        self.assert_calculator_error("sqrt(-1)", "Invalid value")
        self.assert_calculator_error("(-4)^0.5", "Invalid value")
        self.assert_calculator_error("fact(3.5)", "whole numbers")
        self.assert_calculator_error("2^2000", "Number too large")
        self.assert_calculator_error("2^10001", "Exponent too large")
        self.assert_calculator_error("1e309", "Number too large")
        self.assert_calculator_error("1" * (MAX_INPUT_LENGTH + 1), "too long")


if __name__ == "__main__":
    unittest.main()
