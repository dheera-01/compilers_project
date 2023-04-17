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
    i = eval_literals(eval(indexVal, program_env))
    objectToBeIndexed = eval_literals(program_env.get(identifier.name))
    if(len(objectToBeIndexed) <= i):
        print("Index out of range")

    item = program_env.get(identifier.name)

    ans = (eval_literals(program_env.get(identifier.name)))[i]

    if(isinstance(item, ListLiteral)):
        return NumLiteral(ans)
    elif(isinstance(item, StringLiteral)):
        return StringLiteral(ans)
    else:
        print(f"Indexing not supported for {identifier} of type {type(item)}")
        return None
```

The function first evaluates the indexVal expression using the eval_literals function and stores the result in the variable i. Then, it evaluates the value of the identifier using program_env.get() and stores it in the variable objectToBeIndexed.

Next, it checks if the value of i is greater than or equal to the length of the objectToBeIndexed. If it is, it prints a message saying that the index is out of range.

Then, the function gets the value of item using program_env.get() and stores it in the variable item. It also calculates the indexed value of the identifier using the evaluated value of indexVal and stores it in the variable ans.

Finally, the function checks the type of the item and returns a NumLiteral or StringLiteral object containing the value of the indexed element if it is of the corresponding type. If the type of the item is neither ListLiteral nor StringLiteral, the function prints a message saying that indexing is not supported for the type of the identifier and returns None.

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

