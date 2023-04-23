## Unary Operation

The code snippet provided is part of a larger program that handles unary operations. Unary operations are operations that take only one operand, and in this case, the supported unary operations are "-" (negation) and "+" (identity).

### Negation ("-")
```python
case UnaryOp("-", x):
            try:
                return eval(BinOp(NumLiteral(-1), "*", x), program_env)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: - not supported between instances of {x}")
```

The code snippet handles the negation unary operation ("-"). It takes an operand "x" and performs the negation operation on it. The code uses the `eval()` function to evaluate a binary operation, where the first operand is a numeric literal with a value of -1, the operator is "*", and the second operand is "x". This effectively multiplies "x" by -1, resulting in the negation of "x".

If an exception occurs during the evaluation, it catches the exception and raises an "InvalidProgram" error with a message that specifies the type of error that occurred, along with the type of operands involved in the operation.

### Identity ("+")

```python
case UnaryOp("+", x):
            try:
                return eval(BinOp(NumLiteral(1), "*", x), program_env)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: + not supported between instances of {x}")
```

The code snippet handles the identity unary operation ("+"). It takes an operand "x" and performs the identity operation on it. Similar to the negation operation, it uses the `eval()` function to evaluate a binary operation, where the first operand is a numeric literal with a value of 1, the operator is "*", and the second operand is "x". This results in the same value of "x" being returned, as the identity operation does not change the value of the operand.

If an exception occurs during the evaluation, it catches the exception and raises an "InvalidProgram" error with a message that specifies the type of error that occurred, along with the type of operands involved in the operation.
