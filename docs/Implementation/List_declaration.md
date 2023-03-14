# Lists

### List declaration


For declaring a list, We have used the `[]` brackets notation as used in python language. List can be declared in a similar way as we declare a variable. So basically, we are assigning a identifier to a list when `assign` is called.
Following is the class of assign where the changes are made. The value can be either an AST or a list of 'AST'

```python
@dataclass
class Assign:
    v: "AST" or list['AST']
    right:'AST' or list['AST']
    
    def __repr__(self) -> str:
        return f"Assign({self.v} = {self.right})"
```

### How to declare a list?

Here we have made the list declaration in such a way that it can be reassigned as well. Example is shown below:-

```python
# INPUT
assign arr = [1, 3, 5, 11, 29];
print(arr);

arr = [2, 4, 6, 12, 30];
print(arr);
```
```python
#OUTPUT
[1, 3, 5, 11, 29]
[2, 4, 6, 12, 30]
```

Changes are made in assign and update function in file eval_for_parser.py. If the identifier has not been declared till now and it does not exists in program_env, then it is added to program_env. If the identifier is already declared, then it is updated with the new value in the update function. Here we are type checking the value to be a list or not. If it is not a list, then it must be a NumLiteral, StringLiteral, BoolLiteral or FloatLiteral.

```python
case Assign(identifier, right):
            if type(right).__name__ == 'list':
                program_env.add(identifier, right)
                return None
            
            value = eval(right, program_env)
            program_env.add(identifier, value)
            return None

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

### How is the list evaluated?

We are receiving the lists in the form like this:-

```python
[NumLiteral(1), NumLiteral(3), NumLiteral(5)]
```
So we have declared a seperate case in eval_literals function in eval_for_parser.py file. Here we are checking the type of value received. If it is a list which is the `case _` , then we are iterating over the list and appending the values to a new list. This new list is returned.
Code shown below:-


```python
def eval_literals(literal: Value) -> Value_literal:
    match literal:
        case NumLiteral(value):
            return value
        
        case FloatLiteral(value):
            return value

        case StringLiteral(value):
            return value

        case BoolLiteral(Value):
            return Value
        
        # List Literal
        case _ :
            ans = []
            for x in literal:
                ans.append(eval_literals(x))
            return ans

```
And the output is shown below after calling eval_literals:-

```python
[1, 3 , 5]
```

### Parser for list declaration

We have made changes in parse_assign function in parser.py. Once we parse the Keyword 'assign' and the operator '='. After that we can have 2 cases, the next part can be a list or a variable as well. If its a list, then we encounter a '[' and then store the literal in a new declared list and keep skipping the operator ','. We will do this until we encounter a closing bracket ']'. If the next part is a variable, then we will parse it as a variable and return the AST.

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
        return Assign(tuple(assignments_l),tuple(assignments_r))
```

