Let statement have consits of three components:
1. Variables to be assigned
2. Values to be assigned to corresponding variables
3. Body of the let statement (expression to be evaluated)

```python
class Let:
    var: 'AST'
    e1: 'AST'
    e2: 'AST'

    def __repr__(self) -> str:
        return f"Let {self.var} = {self.e1} in {self.e2})"
```

As we have already implemented the assign statements we can use the same to assign values to variables. Once the assignment is complete we can evaluate the body of the let statement.
On complete evaluation of let statement returns the value of the body. 

```python
case Let(variable as v, value as val, e2):  
    program_env.enter_scope()
    eval(Assign((v,), (val,)), program_env)
    program_env.enter_scope()
    e2_val = eval(e2, program_env)
    program_env.exit_scope()
    program_env.exit_scope()
    return e2_val
```

In case of multiple let statements the value of the last(inner most) let statement is returned.
 

For instance consider the following program:

```
assign c = let a =9 (let b = 45 (a + b));
print(c);
```

Output:
``
54
``


### Parsing let statements
The following is parser for let:
```python
def parse_let(self):
    """parse the let expression
    Returns:
        returns the value of expression after in keyword
    """

    self.lexer.match(Keyword("let"))
    left_part = self.parse_atom()
    self.lexer.match(Operator("="))
    right_part = self.parse_simple()
    self.lexer.match(Bracket("("))
    body = self.parse_simple()
    self.lexer.match(Bracket(")"))
    return Let(left_part, right_part, body)
```



