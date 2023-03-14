# Strings

## Declaration

### StringLiteral class
`StringLiteral` class is declared which stores the value as the `str`. Strings can be declared using this class and in the `eval_literals` function, the evaluation of `StringLiteral` returns the stored string.
```python
@dataclass
class StringLiteral:
    value: str

    def __repr__(self) -> str:
        return f"StringLiteral(\"{self.value}\")"
```

### Slice class
`Slice` will be declared whenever programmer tries to slice the string objects. It contains 4 members, 1 for storing the string and others for start, end, and step respectively.
```python
@dataclass
class Slice:
    string_var: 'AST'
    start: 'AST'
    end: 'AST'
    step: 'AST'

    def __repr__(self) -> str:
        return f"Slice({self.string_var}[{self.start}:{self.end}:{self.step}])"
```

## Operations on StringLiteral

### Concatenation
2 types of string concatenation are implemented:
1. StringLiteral and StringLiteral
2. (StringLiteral and NumLiteral) or (NumLiteral and StringLiteral)

For implementing the concatenation, same case which is used for 2 numbers is used. Here try-except is used for ruling out the cases where concatenation is not possible. First case is handled by python, only the concatenated string is wrapped in `StringLiteral` before returning.
Second case is checked and then left and right AST is typecasted to python's string for concatenation. Finally wrapped in `StringLiteral` before returning.
```python
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
```

### Multiplication
Our language also supports replicating string certain number of time like python. For example, "Hello"*3 should be "HelloHelloHello".
For implementing the replication, it is checked whether first literal is `StringLiteral` and second is `NumLiteral`, the result is wrapped in `StringLiteral`.

```python
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
```

### Slicing
Strings also support slicing which is implemented using the slicing of the python's strings. This just checks whether all the start, end and step are all numliterals and slicing is done on `StringLiteral`.
```python
case Slice(string_var, start, end, step):
            string_var = eval(string_var, program_env)
            start = eval(start, program_env)
            end = eval(end, program_env)
            step = eval(step, program_env)
            if isinstance(string_var, StringLiteral) and isinstance(start, NumLiteral) and isinstance(end, NumLiteral) and isinstance(step,NumLiteral):
                string_var = eval_literals(string_var)
                start = eval_literals(start)
                end = eval_literals(end)
                step = eval_literals(step)
                res = string_var[start:end:step]
                return StringLiteral(res)
            else:
                raise InvalidProgram(
                    f"TypeError: slice indices must be NumLiteral")
```

### String Indexing
String indexing description is added in implementation/Indexer docs.