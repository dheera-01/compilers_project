# Binary operations

```python
# binary operation
        case BinOp(left, "+", right):
            eval_left = eval(left, program_env)
            eval_right = eval(right, program_env)

            try:
                if isinstance(eval_left, StringLiteral) or isinstance(eval_right, StringLiteral):
                    res = str(eval_literals(eval_left)) + str(eval_literals(eval_right))
                    return StringLiteral(res)
                else:
                    res = eval_literals(eval_left) + eval_literals(eval_right)
                    if isinstance(eval_left, FloatLiteral) or isinstance(eval_right, FloatLiteral):
                        return FloatLiteral(res)
                    else:
                        return NumLiteral(res)
            except Exception as e:
                # raise TypeError(f"+ not supported between instances of {type(eval_left).__name__} and {type(eval_right).__name__}")
                raise InvalidProgram(
                    f"+ not supported between instances of {left} and {right}")

        case BinOp(left, "-", right):
            eval_left = eval(left, program_env)
            eval_right = eval(right, program_env)
            try:
                res = eval_literals(eval_left) - eval_literals(eval_right)
                if isinstance(eval_left, FloatLiteral) or isinstance(eval_right, FloatLiteral):
                    return FloatLiteral(res)
                else:
                    return NumLiteral(res)
            except Exception as e:
                raise InvalidProgram(f"TypeError: - not supported between instances of {left} and {right}")

        case BinOp(left, "*", right):
            eval_left = eval(left, program_env)
            eval_right = eval(right, program_env)
            try:
                res = eval_literals(eval_left) * eval_literals(eval_right)
                if isinstance(eval_left, StringLiteral) and isinstance(eval_right, NumLiteral):
                    return StringLiteral(res)
                elif isinstance(eval_left, FloatLiteral) or isinstance(eval_right, FloatLiteral):
                    return FloatLiteral(res)
                else:
                    return NumLiteral(res)
            except Exception as e:
                raise InvalidProgram(f"TypeError: * not supported between instances of {left} and {right}")

        case BinOp(left, "/", right):
            eval_left = eval(left, program_env)
            eval_right = eval(right, program_env)
            try:
                res = eval_literals(eval_left) / eval_literals(eval_right)
                return FloatLiteral(res)
            except ZeroDivisionError as e:
                raise InvalidProgram(f"ZeroDivisionError: division by zero")
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: / not supported between instances of {left} and {right}")

        case BinOp(left, "//", right):
            eval_left = eval(left, program_env)
            eval_right = eval(right, program_env)
            try:
                res = eval_literals(eval_left) // eval_literals(eval_right)
                return NumLiteral(res)
            except ZeroDivisionError as e:
                raise InvalidProgram(
                    f"ZeroDivisionError: floor division by zero")
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: // not supported between instances of {left} and {right}")

        case BinOp(left, "%", right):
            eval_left = eval(left, program_env)
            eval_right = eval(right, program_env)
            try:
                res = eval_literals(eval_left) % eval_literals(eval_right)
                return NumLiteral(res)
            except ZeroDivisionError as e:
                raise InvalidProgram(f"ZeroDivisionError: modulo by zero")
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: % not supported between instances of {left} and {right}")

        case BinOp(left, "**", right):
            eval_left = eval(left, program_env)
            eval_right = eval(right, program_env)
            try:
                res = eval_literals(eval_left) ** eval_literals(eval_right)
                return NumLiteral(res)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: ** not supported between instances of {left} and {right}")

        # concatenation operation
        case BinOp(left, "~", right):
            eval_left = eval(left, program_env)
            eval_right = eval(right, program_env)
            try:
                concat_similar_addition = ["StringLiteral", "NumLiteral", "FloatLiteral"]
                if eval_left.__class__.__name__ in concat_similar_addition and eval_right.__class__.__name__ in concat_similar_addition:
                    res = str(eval_literals(eval_left)) + str(eval_literals(eval_right))
                    return StringLiteral(res)
                raise InvalidProgram(
                    f"~ not supported between instances of {eval_left} and {eval_right}")
            except Exception as e:
                raise TypeError(
                    f"+ not supported between instances of {type(eval_left).__name__} and {type(eval_right).__name__}")
                raise InvalidProgram(
                    f"~ not supported between instances of {eval_left} and {eval_right}")
```

### Addition (`+`):
- Supports addition of numbers (`NumLiteral`), floating-point numbers (`FloatLiteral`), and string literals (`StringLiteral`).
- If both operands are strings, it concatenates them.
- If one operand is a string and the other is a number or float, it converts the number or float to a string and concatenates them.
- Any other combination of operands results in a TypeError.

### Subtraction (`-`):
- Supports subtraction of numbers (`NumLiteral`) and floating-point numbers (`FloatLiteral`).
- Any other combination of operands results in a TypeError.

### Multiplication (`*`):
- Supports multiplication of numbers (`NumLiteral`), floating-point numbers (`FloatLiteral`), and string literals (`StringLiteral`).
- If one operand is a string and the other is a number, it repeats the string by the number of times specified by the number operand.
- Any other combination of operands results in a TypeError.

### Division (`/`):
- Supports division of numbers (`NumLiteral`) and floating-point numbers (`FloatLiteral`).
- Raises a ZeroDivisionError if the divisor is zero.
- Any other combination of operands results in a TypeError.

### Floor Division (`//`):
- Supports floor division of numbers (`NumLiteral`) and floating-point numbers (`FloatLiteral`).
- Raises a ZeroDivisionError if the divisor is zero.
- Any other combination of operands results in a TypeError.

### Modulo (`%`):
- Supports modulo operation on numbers (`NumLiteral`) and floating-point numbers (`FloatLiteral`).
- Raises a ZeroDivisionError if the divisor is zero.
- Any other combination of operands results in a TypeError.

### Exponentiation (`**`):
- Supports exponentiation of numbers (`NumLiteral`) and floating-point numbers (`FloatLiteral`).
- Any other combination of operands results in a TypeError.

### Concatenation (`~`):
- Supports concatenation of numbers (`NumLiteral`), floating-point numbers (`FloatLiteral`), and string literals (`StringLiteral`).
- If both operands are numbers, it concatenates their string representation.
- If both operands are strings, it concatenates them.
- If one operand is a string and the other is a number or float, it converts the number or float to a string and concatenates them.
- Any other combination of operands results in a TypeError.
