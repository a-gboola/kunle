# Secure Calculator Threat Model

**Implementation:** `scicalc.py`

**Security goal:** calculate only the supported mathematical language while
protecting the host, calculator availability, and result integrity.

## Scope and assets

The application accepts calculator expressions through a Tkinter entry field and returns a numeric result. Protected assets are: the user's machine and files, application availability, and the integrity of calculation results. The calculator runs locally and has no network, authentication, or persistent-data boundary.

## Trust boundaries and attackers

Text entered or pasted into the display is untrusted. An attacker is anyone able to use the calculator or supply text for a user to paste. They may try Python-code execution, malformed expressions, extreme numeric inputs, or inputs that force expensive parsing or arithmetic.

## Risks and mitigations

| Risk | Example | Mitigation |
| --- | --- | --- |
| Code execution | `__import__('os')`, attributes, comprehensions | Expressions are parsed with `ast`; the evaluator accepts only numeric literals, five arithmetic operators, two unary operators, listed constants, and one-argument listed functions. `eval` is not used. |
| Parser or CPU exhaustion | deeply nested parentheses or chained operations | A 50-character input limit, 100-node AST limit, and 25-level AST-depth limit bound parse and evaluation work. |
| Memory exhaustion | `999999**999999` | Integer bit length and exponent magnitude are capped before expensive integer exponentiation. |
| Numeric overflow / non-finite values | `10^10000`, `1e309` | Every result is checked for finite floats and a bounded integer size. Overflow becomes a safe calculator message. |
| Domain and arithmetic exceptions | `1/0`, `sqrt(-1)`, `log(0)` | Expected exceptions are converted to concise user-safe messages; an outer GUI boundary suppresses unexpected internal details. |
| Factorial resource use | `fact(1000000)` | Only whole, non-negative values up to 170 are accepted. |

## Residual risk and maintenance

The calculator intentionally supports only its documented expression language; unsupported Python syntax must remain rejected. New operators or functions must be explicitly added to `ExpressionEvaluator`, receive limits where their work can grow, and receive negative/security tests. The local GUI process remains subject to operating-system-level compromise outside this application's scope.

## Verification evidence

`test_scicalc.py` verifies expected calculations and the security boundaries:
code-execution syntax, division by zero, invalid mathematical domains,
factorial constraints, non-finite values, oversized powers, and overlong input.
Run it with:

```powershell
python -m unittest -v test_scicalc.py
```
