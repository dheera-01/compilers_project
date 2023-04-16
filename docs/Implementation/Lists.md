# Lists


## Class of ListLiteral

First i will show how is the structure of ListLiteral.

```python
@dataclass
class ListLiteral:
    value: list

    def __repr__(self) -> str:
        return f"ListLiteral({self.value})"
```

- This code defines a Python class called ListLiteral that is decorated with the @dataclass decorator. The @dataclass decorator is used to automatically generate several special methods for the class, such as `__init__(), __repr__()`, and others, based on the class attributes defined inside it.

- The ListLiteral class has a single attribute called value, which is expected to be a Python list. The attribute is defined using Python's type hint syntax, which indicates that the attribute should be of type list.

- Now, let's see how the ListLiteral class and the list operations are parsed from program.txt. The list operations for now are created using a "." operation for now.

```python
def parse_atom(self,is_func=False):
        """parse the atomic expression"""
        match self.lexer.peek_current_token():  
            case Identifier(name):
                self.lexer.advance()
                match self.lexer.peek_current_token():
                    case Bracket("["):
                        self.lexer.advance()
                        right_part = self.parse_simple() # parse_simple
                        self.lexer.match(Bracket("]"))

                        return Indexer(Identifier(name), right_part)
                    case Operator("."):
                        self.lexer.advance()
                        match self.lexer.peek_current_token():
                            case Keyword("LEN"):
                                self.lexer.advance()
                                return ListOperations(Identifier(name), "LEN", None, None)
                            case Keyword("TAIL"):
                                self.lexer.advance()
                                return ListOperations(Identifier(name), "TAIL", None, None)
                            case Keyword("HEAD"):
                                self.lexer.advance()
                                return ListOperations(Identifier(name), "HEAD", None, None)
                            case Keyword("APPEND"):
                                self.lexer.advance()
                                self.lexer.match(Bracket("("))
                                right_part = self.parse_atom()
                                self.lexer.match(Bracket(")"))
                                return ListOperations(Identifier(name), "APPEND", right_part, None)
                            case Keyword("POP"):
                                self.lexer.advance()
                                return ListOperations(Identifier(name), "POP", None, None)
```

- The purpose of the parse_atom() method is to parse an "atomic expression" from some input.The method begins with a match statement that checks the type of the next token in the input. .

- If the next token is an identifier, the method advances the lexer and checks the type of the next token again. If the next token is a left bracket ([), the method parses the contents of the brackets by calling parse_simple(), and returns an Indexer object with the identifier and the parsed contents as its arguments. This is used to parse the index of a list.

## How is the ListOperations parsed?

If the next token is a period (.), the method advances the lexer and checks the type of the next token again. Depending on the specific keyword that follows the period, the method returns a ListOperations object with different arguments.

* If the keyword is LEN, the method returns a ListOperations object with the identifier and the string "LEN" as its arguments.

* If the keyword is TAIL, the method returns a ListOperations object with the identifier and the string "TAIL" as its arguments.

* If the keyword is HEAD, the method returns a ListOperations object with the identifier and the string "HEAD" as its arguments.

* If the keyword is APPEND, the method parses the contents of the parentheses by calling parse_atom(), and returns a ListOperations object with the identifier, the string "APPEND", and the parsed contents as its arguments.

* If the keyword is POP, the method returns a ListOperations object with the identifier and the string "POP" as its arguments.

## How is the ListLiteral evaluated?

For evaluating the list literal and list operations, the code is in the eval_for_parser.py.

```python
case ListLiteral(value):
    for i, x in enumerate(value):
        value[i] = eval(x, program_env)
    return program
```
- This code block is a part of the evaluation function that takes a ListLiteral object and evaluates its elements recursively.

- The code block first iterates over the elements of the input list using the enumerate() function, which returns both the index and the corresponding element value. Then for each element, the eval() function is called with two arguments: the first argument is the string representation of the element, and the second argument is the program_env environment that contains the values of all variables defined in the program.

- The eval() function is used to evaluate the string representation of the element as a Python expression in the context of the program_env environment, and the resulting value is stored back in the list at the same index.

- Finally, the updated list is returned, which contains the evaluated values of all the elements of the original input list.

## How is ListLiteral evaluated?
```python
case ListLiteral(value):
    ans = []
    for x in value:
        ans.append(eval_literals(x))
    return ans
```

- The function first initializes an empty Python list ans that will store the evaluated elements. Then, it iterates through each element x in the original list value. For each element, it calls the eval_literals function to evaluate the element and appends the evaluated result to the ans list.

- After iterating through all elements, the function returns the ans list. This returned list contains the evaluated version of the input ListLiteral object.

For the list operations, the eval is handled by the following way below.

```python
case ListOperations(identifier, val, item, indVal):

    if(val == "LEN"):
        listLit = program_env.get(identifier.name)
        lis = listLit.value
        a = NumLiteral(len(lis))
        return a
    elif (val == "HEAD"):
        listLit = program_env.get(identifier.name)
        l = listLit.value
        return l[0]
    elif (val == "TAIL"):
        listLit = program_env.get(identifier.name)
        lis = listLit.value
        return lis[len(lis)-1]
    elif (val == "APPEND"):
        a = program_env.get(identifier.name)
        if(isinstance(a, ListLiteral)):
            a = a.value
        a.append(item)
        a = program_env.get(identifier.name)
        return a
    elif (val == "POP"):
        a = program_env.get(identifier.name)
        if(isinstance(a, ListLiteral)):
            a = a.value
        elem = a.pop()
        
        return elem
    elif (val == "ChangeOneElement"):
        a = program_env.get(identifier.name)    
        if(isinstance(a, ListLiteral)):
            a = a.value
        a[eval_literals(eval(indVal, program_env))] = eval(item, program_env)
    return None
```

- This code block above handles the evaluation of list operations in the input program. It takes a ListOperations object and performs the operation based on the given input arguments.

- The function first checks the value of the val parameter to determine which list operation to perform. If the value is "LEN", the function retrieves the ListLiteral object from the environment using the identifier name, calculates the length of the list using the len() function, and returns it as a NumLiteral object.

- If the value is "HEAD", the function retrieves the ListLiteral object from the environment using the identifier name, extracts the first element from the list, and returns it as a Numliteral object.

- If the value is "TAIL", the function retrieves the ListLiteral object from the environment using the identifier name, extracts the last element from the list, and returns it as a Numliteral object.

- If the value is "APPEND", the function retrieves the list from the environment using the identifier name, appends the item argument to the list, and returns the updated ListLiteral.

- If the value is "POP", the function retrieves the list from the environment using the identifier name, removes and returns the last element of the list using the pop() method and also returns the ListLiteral.

- If the value is "ChangeOneElement", the function retrieves the list from the environment using the identifier name, modifies the element at the index specified by the indVal argument to the value of the item argument.The modified list is then stored back in the environment using the same identifier name.

- Finally, the function returns None if none of the conditions are met.

