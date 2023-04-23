# Boolify

Equivalent to python's `bool`.
```python
case Boolify(e):
            return BoolLiteral(bool(eval_literals(eval(e, program_env))))
```