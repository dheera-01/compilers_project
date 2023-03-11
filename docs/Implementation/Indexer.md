#  Indexer

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

