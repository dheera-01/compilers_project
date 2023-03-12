# 27 Feb

## Rahul Rai(@RahulRai02)

Work done:-
For the last week, i have worked on list declaration without the explicit keyword `list` and indexer for list and string. I have also reviewd the Issue #5 of the project. I have also worked on the documentation of the list declaration, indexer and print.

# List declaration

To declare list, earlier i was using an explicit keyword `list` but now i have removed that keyword and now the list can be declared in the same way as we declare a variable. Example is shown below:-

```python
# INPUT
assign arr = [1, 2, 3, 11, 18];
print(arr);
```
```python
# OUTPUT
[1, 2, 3, 11, 18]
```

For this to happen, i have made changes in the assign function in eval_for_parser.py. 

Detailed description is shown below:-


For declaring a list, We have used the `[]` brackets notation as used in python language. List can be declared in a similar way as we declare a variable. So basically, we are assigning a identifier to a list when `assign` is called.
Following is the class of assign where the changes are made. The value can be either an AST or a list of 'AST'

```python
class Assign:
    v: "AST"
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
        """
        parse the assign expression
        
        Returns:
            Assign: return AST of the assign expression
        """
        self.lexer.match(Keyword("assign"))  # consume the assign keyword
        left_part = self.parse_atom()
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
                self.lexer.match(EndOfLine(";"))
                return Assign(left_part, right_part)
            case _:
                right_part = self.parse_simple()
                self.lexer.match(EndOfLine(";"))
                return Assign(left_part, right_part)
```

# Indexer for list and string

I have added a keyword `index` to index a list or string but now i have removed it and we can index it in the same way as we index a list or string in python. Example is shown below:-

Detailed description is shown below:-

The indexer is responsible for indexing the data structure which is indexable. In our cases, till now we can index a list and a string.

### Syntax

Following is the syntax for indexing a list or a string:-

```python
# INPUT
assign arr = [1, 2, 3, 11, 18];
print(arr);

assign p = arr[3];
print(p);

assign str = "hello";
assign q = str[1];
print(q);
```

```python
#OUTPUT
[1, 2, 3, 11, 18]
11
e
```

### Class for Indexer

We have created class Indexer which takes val as Identifier and the index as AST. Below is the class declaration:-

```python
@dataclass
class Indexer:
    val: Identifier
    index: 'AST'

    def __repr__(self) -> str:
        return f"Indexer({self.val}[{self.index}])"
```

### How is the Indexer class evaluated?
We are using the eval_literals function to evaluate the value of the index and then using that value to index the list or the string. Since we have the identifier we could get the coresponding value from the program_env and then perform the required operations by type checking. Below is the code snippet:-

```python
case Indexer(identifier, indexVal):
            i = eval_literals(indexVal)
            objectToBeIndexed = eval_literals(program_env.get(identifier.name))
            if(len(objectToBeIndexed) <= i):
                print("Index out of range")
            for env in reversed(program_env.envs):
                if identifier.name in env:
                    if(type(program_env.get(identifier.name)) == list):
                        return program_env.get(identifier.name)[i]
                    elif(type(program_env.get(identifier.name)) == StringLiteral):
                        res = eval_literals(program_env.get(identifier.name))[i]
                        return StringLiteral(res)        
                    else:
                        print(f"The Indentifier {identifier} is not iterable")
                        return None
```

If its a list, then get the list coresponding to that identifier and index it. If its a string, then get the string coresponding to that identifier and index it. If it is any other data structure, then it is not iterable.

### How to parse the Indexer class?

We are parsing the index when we encounter a identifier and a ' [ '. We have added that code in parse_atom(self) function in file parser.py. Once we encounter a '[', then move to the next token and parse the expression which is the index value. Then move to the next token and check if it is a ' ] '. If it is not a ' ] ', then raise an error. Below is the code snippet:-

```python 
def parse_atom(self):
        """parse the atomic expression"""
        match self.lexer.peek_current_token():  
            case Identifier(name):
                self.lexer.advance()
                match self.lexer.peek_current_token():
                    case Bracket("["):
                        self.lexer.advance()
                        right_part = self.parse_atom()
                        self.lexer.match(Bracket("]"))
                        return Indexer(Identifier(name), right_part)
                    case _:
                        # self.lexer.advance()
                        return Identifier(name)
            # OTHER CASES IN CODE ON MAIN
            case .......:
                pass
            case ......:
                pass
```

