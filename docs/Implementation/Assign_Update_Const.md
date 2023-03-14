# Assign, Update and Const

`assign` keyword is used for assignment. Following class is instantiated whenever parser detects a assign.

```python
@dataclass
class Assign:
    v: "AST" or list['AST']
    right:'AST' or list['AST']
    
    def __repr__(self) -> str:
        return f"Assign({self.v} = {self.right})"
```
`Assign` class has 2 members where v stores the Identifier and right stores the AST which can be any expression. Following is the Identifier class which stores the name of the Identifier
```python
@dataclass
class Identifier:
    name: str
    is_mutable: bool = True

    def __repr__(self) -> str:
        return f"Identifier({self.name})"
```
By default, `is_mutable` is set to `True`. Whenever `const` keyword is used infront of `assign`, then `is_mutable` is set to `False`.

## Parser for assign and const
Following function is called after parser detects a `assign` keyword. This function parses a Identifier and "=" and an expression. After matching the "=", we are handling 3 cases that the remaining part can be the following:-
1. List --> assign arr = [1, 2, 3];
2. Variable --> assing a = 1;
3. Multiple assignment of variable --> assign `a = 1, b = 2, c = 3;`

```python
    def parse_assign(self):
        self.lexer.match(Keyword("assign"))
        assignments_l = []
        assignments_r = []
        while True:
            # self.lexer.advance()
            left_part = self.parse_atom()
            assignments_l.append(left_part)
            self.lexer.match(Operator("="))

            match self.lexer.peek_current_token():
                case Bracket("["):
                    self.lexer.advance()
                    right_part = []
                    while True:
                        match self.lexer.peek_current_token():
                            case Bracket("]"):
                                self.lexer.advance()
                                break
                            case Operator(","):
                                self.lexer.advance()
                            case _:
                                right_part.append(self.parse_simple())
                    assignments_r.append(right_part)
                case _:
                    right_part = self.parse_simple()
                    assignments_r.append(right_part)

            match self.lexer.peek_current_token():
                case Operator(op) if op in ",":
                    self.lexer.match(Operator(","))
                    continue
                case _:
                    break

        self.lexer.match(EndOfLine(";"))
        return Assign(tuple(assignments_l),tuple(assignments_r))

```
We have 2 lists assignments_l and assignments_r, the assignments_l stores the identifiers and assignments_r stores the values. We have declared these lists in order to handle multiple assignments. For example, take `assign a = 1, b = 3, c = 4;`. In this we are assigning the first variable with 1 and then checking if there exists a ',', skip it and continue and then again do that for b and then c. If there is no ',' then break the loop. After the loop is broken, we are returning the Assign object with the tuple of identifiers and tuple of values.

For list, we are checking for the Bracket '[' and if is not present then we are sure that it must be a variable. So we are parsing the simple expression and storing it in assignments_r.


Everthing is same as above in whenever 'const' keyword is parsed except that `is_mutable = False`.

```python
def parse_const(self):
        """paster the immutable assign expression
        Returns:
            Assign: return AST of the immutable assign expression
        """
        self.lexer.match(Keyword("const"))
        self.lexer.match(Keyword("assign"))
        assignments_l = []
        assignments_r = []
        while True:
            # self.lexer.advance()
            left_part = self.parse_atom()
            left_part.is_mutable = False
            assignments_l.append(left_part)
            self.lexer.match(Operator("="))

            # 2 cases: 1. assign to a variable 2. assign to a list
            match self.lexer.peek_current_token():
                case Bracket("["):
                    # Till you dont encounter a closing bracket, keep parsing the expression and store the literals
                    # in a list and skip the operator ","
                    self.lexer.advance()
                    right_part = []
                    while True:
                        match self.lexer.peek_current_token():
                            case Bracket("]"):
                                self.lexer.advance()
                                break
                            case Operator(","):
                                self.lexer.advance()
                            case _:
                                right_part.append(self.parse_simple())
                    assignments_r.append(right_part)
                case _:
                    right_part = self.parse_simple()
                    assignments_r.append(right_part)

            match self.lexer.peek_current_token():
                case Operator(op) if op in ",":
                    self.lexer.match(Operator(","))
                    continue
                case _:
                    break

        self.lexer.match(EndOfLine(";"))
        return Assign(tuple(assignments_l), tuple(assignments_r))

```

The above function is only used for assigning it to identifiers. For updating, we have a separate function `parse_update` which is as follows. The update expression handles the following cases `= -= += *= /= %= //= **=` for updation.

```python
def parse_update(self):
        """parse the update expression
        Returns:
            Update: return AST of the update expression
        """
        left_part = self.parse_atom()
        
        assignment_operator_list = "= -= += *= /= %= //= **=".split()
        op = self.lexer.peek_current_token()
        if not isinstance(op, Operator):
            raise InvalidProgram(f"Syntax Error: Expected an assignment operator but got {op}")
        if op._operator not in assignment_operator_list:
            raise InvalidProgram(f"Syntax Error: {op} not a valid assignment operator")
        self.lexer.advance() # consuming the assignment operator

        match self.lexer.peek_current_token():
            case Bracket("["):
                self.lexer.advance()
                right_part = []
                while True:
                    match self.lexer.peek_current_token():
                        case Bracket("]"):
                            self.lexer.advance()
                            break
                        case Operator(","):
                            self.lexer.advance()
                        case _:
                            right_part.append(self.parse_simple())
                self.lexer.match(EndOfLine(";"))
                return Update(left_part, op, right_part)
            case _:
                right_part = self.parse_simple()
                self.lexer.match(EndOfLine(";"))
                return Update(left_part, op, right_part)
```

***NOTE: We cannot update the variables using the syntax of multiple assignments***



## Eval for Assign and Update
Once the assign object and Update object is constructed, it falls in the below cases that is either assign or update.

In the assign case, we are checking the type of the right part. If its a list, then we are adding the identifier and the list to the environment. Else it is the case of a variable and multiple assignments to variables and then adding them to the environment.

```python
case Assign(identifier, right):
    for i, ident in enumerate(identifier):
        if type(right[i]).__name__ == 'list':
            program_env.add(ident, right[i])
        else:
            # print(right[i])
            value = eval(right[i], program_env)
            # print(value)
            program_env.add(ident, value)
    return None
```

In the update case, we are type checking, if its a list, then we are updating the identifier with the list. Else we are checking the operator and then based on the operator, we are updating the identifier's value.

***Note: We are not handling multiple updation to variables in update.***


```python
case Update(identifier, op, right):
    if type(right).__name__ == 'list':
        program_env.update(identifier, right)
        return None

    value = eval(right, program_env)
    if op._operator == "=":
        program_env.update(identifier, value)
    else:# op is +=, -=, *=, /=, %=, **= (binop of first to second last char)
        v = eval(BinOp(identifier, op._operator[: len(op._operator) -1], right), program_env)
        program_env.update(identifier, v)
    return None 
```

