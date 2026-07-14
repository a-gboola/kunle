import unittest

from hardened import CalculatorError, ExpressionEvaluator, MAX_INPUT_LENGTH


class ExpressionEvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.evaluator = ExpressionEvaluator()

    def assert_error(self, expression, expected):
        with self.assertRaisesRegex(CalculatorError, expected):
            self.evaluator.evaluate(expression)

    def test_evaluates_supported_math(self):
        self.assertEqual(self.evaluator.evaluate("2 + 3 * 4"), 14)
        self.assertEqual(self.evaluator.evaluate("fact(5)"), 120)
        self.assertAlmostEqual(self.evaluator.evaluate("sin(90)"), 1.0)

    def test_rejects_python_execution_syntax(self):
        self.assert_error("__import__('os').system('whoami')", "Invalid input")
        self.assert_error("(1).__class__", "Invalid input")
        self.assert_error("lambda: 1", "Invalid input")

    def test_handles_arithmetic_and_domain_errors(self):
        self.assert_error("1 / 0", "Cannot divide by 0")
        self.assert_error("sqrt(-1)", "Invalid value")
        self.assert_error("fact(3.5)", "whole numbers")

    def test_enforces_resource_and_overflow_limits(self):
        self.assert_error("2^2000", "Number too large")
        self.assert_error("2^10001", "Exponent too large")
        self.assert_error("fact(171)", "too large")
        self.assert_error("1" * (MAX_INPUT_LENGTH + 1), "Too long")


if __name__ == "__main__":
    unittest.main()
