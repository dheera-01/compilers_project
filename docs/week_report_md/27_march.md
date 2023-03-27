# 27 Feb

## Chirag Sarda(@chirag-25)

### Work Done:
- added the concatenation (`~`) operator to Language


#### Concatenation Operator
Concatenation operator is used to concatenate two datatype. it will return String Literal irrespective of the datatype of the operands. It will not throw an error if the operands are not of the same datatype. Currently working only of `NumLiteral`, `StringLiteral` and `StringLiteral`.

#### Implementation
addition, subtraction and concatenation operator are parsed in the same function `parse_add` in `parser.py`. They have same preference and left to right associativity. So, I have added the concatenation operator in the same function.

```python
def parse_add(self):
    """parse the addition and subtraction operator

    Returns:
        AST: return AST of the addition and subtraction operation
    """
    left = self.parse_mult()

    while True:
        match self.lexer.peek_current_token():

            case Operator(op) if op in "+-~":
                self.lexer.advance()
                # print("before parse_add")
                m = self.parse_mult()
                # print("after parse_add",m)
                left = BinOp(left, op, m)

            case _:
                break

        return left
```

#### Eval
```python
case BinOp(left, "+", right):
    eval_left = eval(left, program_env)
    eval_right = eval(right, program_env)

    try:
        if isinstance(eval_left, FloatLiteral) or isinstance(eval_right, FloatLiteral):
            res = eval_literals(eval_left) + eval_literals(eval_right)
            return FloatLiteral(res)
        elif isinstance(eval_left, NumLiteral) and isinstance(eval_right, NumLiteral):
            res = eval_literals(eval_left) + eval_literals(eval_right)
            return NumLiteral(res)
        else: 
            raise InvalidProgram(
                f"+ not supported between instances of {eval_left} and {eval_right}")
            
    except Exception as e:
        raise InvalidProgram(
            f"+ not supported between instances of {eval_left} and {eval_right}")

# concatenation operation
case BinOp(left, "~", right):
    eval_left = eval(left, program_env)
    eval_right = eval(right, program_env)
    try:
        concat_similar_addition = ["StringLiteral", "NumLiteral", "FloatLiteral"]
        if eval_left.__class__.__name__  in concat_similar_addition and eval_right.__class__.__name__ in concat_similar_addition:
            res = str(eval_literals(eval_left)) + str(eval_literals(eval_right))
            return StringLiteral(res)
        
        raise InvalidProgram(
            f"~ not supported between instances of {eval_left} and {eval_right}")
    
    except Exception as e:
        raise InvalidProgram(
            f"~ not supported between instances of {eval_left} and {eval_right}")
```
Addition was changed to support addition of `NumLiteral` and `FloatLiteral` only. Concatenation operator is added to support concatenation of `NumLiteral`, `StringLiteral` and `FloatLiteral`.


#### Example
```python
print(1+1.4);
print("Hello"~"World"~1~1.5); # "HelloWorld"
```
Output:
```text
2.4
HelloWorld11.5
```

#### Special Use
can be used to convert the the Literal to String Literal.

```python
assign a = 1;
a = 1 ~ "";
print(a);
print(a  + 1);
```

Output, Give error:
```text
1
InvalidProgram: + not supported between instances of StringLiteral("1") and NumLiteral(1)
```


