# Comparison Operations

```python
# comparison operation
        case ComparisonOp(x, ">", const):
            try:
                if eval_literals(eval(x, program_env)) > eval_literals(eval(const, program_env)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: > not supported between instances of {x} and {const}")

        case ComparisonOp(x, "<", const):
            try:
                if eval_literals(eval(x, program_env)) < eval_literals(eval(const, program_env)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: < not supported between instances of {x} and {const}")

        case ComparisonOp(x, "==", const):
            try:
                if eval_literals(eval(x, program_env)) == eval_literals(eval(const, program_env)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: == not supported between instances of {x} and {const}")

        case ComparisonOp(x, "!=", const):
            try:
                if eval_literals(eval(x, program_env)) != eval_literals(eval(const, program_env)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: != not supported between instances of {x} and {const}")

        case ComparisonOp(x, "<=", const):
            try:
                if eval_literals(eval(x, program_env)) <= eval_literals(eval(const, program_env)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: <= not supported between instances of {x} and {const}")

        case ComparisonOp(x, ">=", const):
            try:
                if eval_literals(eval(x, program_env)) >= eval_literals(eval(const, program_env)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: >= not supported between instances of {x} and {const}")
        
        case ComparisonOp(cond1, "and", cond2):
            try:
                if eval_literals(eval(cond1, program_env)) and eval_literals(eval(cond2, program_env)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: and not supported between instances of {cond1} and {cond2}")
        
        case ComparisonOp(cond1, "or", cond2):
            try:
                if eval_literals(eval(cond1, program_env)) or eval_literals(eval(cond2, program_env)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: or not supported between instances of {cond1} and {cond2}")
```

### Greater Than (`>`) and Less Than (`<`)

The functions `ComparisonOp(x, ">", const)` and `ComparisonOp(x, "<", const)` implement the greater than and less than comparison operations, respectively. They first evaluate the values of `x` and `const` using the `eval` function with the given `program_env` environment. Then, they compare the evaluated values using the `>` and `<` operators, respectively. If the comparison is true, the function returns a `BoolLiteral(True)`; otherwise, it returns a `BoolLiteral(False)`. If any exceptions occur during the evaluation or comparison, a `TypeError` is raised with an appropriate error message.

### Equal To (`==`) and Not Equal To (`!=`)

The functions `ComparisonOp(x, "==", const)` and `ComparisonOp(x, "!=", const)` implement the equal to and not equal to comparison operations, respectively. They follow a similar logic as the greater than and less than operations, but use the `==` and `!=` operators for comparison.

### Less Than or Equal To (`<=`) and Greater Than or Equal To (`>=`)

The functions `ComparisonOp(x, "<=", const)` and `ComparisonOp(x, ">=", const)` implement the less than or equal to and greater than or equal to comparison operations, respectively. They follow a similar logic as the greater than and less than operations, but use the `<=` and `>=` operators for comparison.

### Logical Operators `and` and `or`

The functions `ComparisonOp(cond1, "and", cond2)` and `ComparisonOp(cond1, "or", cond2)` implement the logical `and` and `or` operations, respectively. They first evaluate the values of `cond1` and `cond2` using the `eval` function with the given `program_env` environment. Then, they perform a logical `and` or `or` operation on the evaluated values, respectively. If the logical operation is true, the function returns a `BoolLiteral(True)`; otherwise, it returns a `BoolLiteral(False)`. If any exceptions occur during the evaluation or logical operation, a `TypeError` is raised with an appropriate error message.

These functions allow for the implementation of comparison operations and logical operators in a programming language, enabling the evaluation of conditional expressions in control flow statements, such as if statements and loops.
