# Weekly Report - 10 April 23

## @chirag-25
Worked on the user defined datatype.

### User defined data type

`struct` class is made for user defined datatype

#### Class Attributes
`name`: A string that holds the name of the user defined datatype.
`fields`: A list that holds the fields of the user defined datatype. Each field is represented as a list containing an `Identifier` and a `Value`.

#### Methods
`get(self, key: Identifier) -> Value`
The get method is used to retrieve the value of a specific field in the `Struct` instance. It takes an `Identifier` as an argument, which represents the name of the field to retrieve. If the field is found in the `fields` list, its value is returned. Otherwise, a `KeyError` is raised, indicating that the field does not exist in the `Struct` instance.


```python
@dataclass
class Struct:
    name: str # string of python
    fields: list
    
    def get(self, key: Identifier):
        """get the value of a field in the struct

        Args:
            key (Identifier): the name of the field

        Returns:
            Value: the value of the field
        """ 
        for field in self.fields:
            if field[0] == key:
                return field[1]
        raise KeyError(f"Struct {self.name} does not have a attribute named {key}")

    def __repr__(self) -> str:
        field_string = ''
        for field in self.fields:
            field_string += f"{field}, "
        return f"Struct {self.name} begin\n{field_string}end"

```

#### Parsing a Struct

Now `parse_atom` function handles three cases:

If the current token is an identifier, it checks for the next token to determine if the identifier is being used for indexing,  accessing a struct field, or as a simple identifier.
- If the identifier is being used for indexing, it recursively calls `parse_simple` to parse the right-hand side of the indexing expression, creates an `Indexer` node in the AST with the identifier and the right-hand side as its children, and returns the node.
- If the identifier is being used for accessing the struct field (like constructors). It then creates a Struct node in the AST with the function name and the arguments as its children, and returns the node.
- If the identifier is being used as a simple identifier, it returns an Identifier node with the identifier name.

Created new function for `parse_struct` parsing struct. It parses the struct expression and returns a Struct node in the AST.

- Match the `struct` keyword using the lexer and raise a Syntax Error if it's not found.
- Peek the current token and raise a `Syntax Error` if it's not an `Identifier`.
- Get the name of the struct and advance the lexer.
- Match the opening curly brace `{` using the lexer and raise a `Syntax Error` if it's not found.
- Loop through each field of the struct and parse its `name` and value if it's provided.
- Append each field to the list of fields in the `Struct` instance.
- Match the closing curly brace `}` using the lexer and raise a `Syntax Error` if it's not found.
- Match the semicolon `;` using the lexer and raise a `Syntax Error` if it's not found.
- Return the Struct instance.

```python

def parse_atom(self):
    """parse the atomic expression"""
    match self.lexer.peek_current_token():  
        case Identifier(name):
            self.lexer.advance()
            match self.lexer.peek_current_token():
                case Bracket("["): # indexing
                    self.lexer.advance()
                    # right_part = self.parse_atom() # parse_simple
                    right_part = self.parse_simple() # parse_simple
                    self.lexer.match(Bracket("]"))
                    return Indexer(Identifier(name), right_part)
                case Bracket("("): # for parsing Student("hello", 1 , 3)
                    self.lexer.advance()                            
                    ind = 0
                    f = []
                    while True:
                        # if ind >= len(f):
                        #     raise Exception("Too many arguments")
                        temp = [Identifier('NULL')]
                        temp.append(self.parse_simple())
                        f.append(temp)
                        ind = ind + 1
                        if self.lexer.peek_current_token() == Bracket(")"):
                            self.lexer.advance()
                            break
                        self.lexer.match(Operator(","))
                    # print(f"user defined data type {user_defined_data_types}") 
                    return Struct(name, f)    
                case Operator("."):
                    pass
                case _: for # parsing simple identifier like a
                    # self.lexer.advance()
                    return Identifier(name)

def parse_struct(self):
    """parse the struct expression
    """
    
    self.lexer.match(Keyword("struct"))
    data_type = self.lexer.peek_current_token()
    assert isinstance(data_type, Identifier), f"Syntax Error: Expected an identifier but got {data_type}"
    data_type = data_type.name
    self.lexer.advance() # consume the token of identifier
    self.lexer.match(Bracket("{"))
    field = []
    while True:
        temp = []
        pt = self.lexer.peek_current_token() # peek token
        assert isinstance(pt, Identifier), f"Syntax Error: Expected an identifier but got {pt}"
        self.lexer.advance() # consume the token of identifier
        temp.append(pt)
        temp.append(None)
        if self.lexer.peek_current_token() == Operator("="):
            self.lexer.advance()
            temp[1] = self.parse_simple()
        field.append(temp)
        if self.lexer.peek_current_token() == Bracket("}"):
            break
        self.lexer.match(Operator(","))
    
    self.lexer.match(Bracket("}"))
    self.lexer.match(EndOfLine(";"))
    return Struct(data_type, field)
    pass


def parse_expr(self):
    """parse the expression

    Returns:
        AST: return AST of the expression
    """
    match self.lexer.peek_current_token():
            return self.parse_print()
        case Keyword("struct"):
```


#### Evaluation part

`Struct(name, fields)` creates a new instance of a user-defined struct type if it doesn't exist yet in the `user_defined_data_types` dictionary (it is storing the schema of the user defined data type). If the struct type already exists, it creates a deep copy (as we cannot change the schema, we need different instance) of the struct type and updates its field values with the values specified in the fields list. The function returns the new or updated struct object.

`Indexer(identifier, indexVal)` was update to incorporate accessing the struct variables. It checks if the variable is an instance of a user-defined struct type and if it is, it returns the value of the specified field in the struct. If the variable is an instance of a list or a string, it returns the value at the specified index. If the index is out of range, it raises an `InvalidProgram exception`. If the variable is not iterable, it raises a `TypeError`.


```python
case Struct(name, fields):
    # print(f"\nInside eval struct: {program}")
    if name not in user_defined_data_types:
        user_defined_data_types[name] = Struct(name, fields)
        print(f"user defined datatype: \n{user_defined_data_types}")
        return None
    struct_object = copy.deepcopy(user_defined_data_types[name])
    for i in range(len(fields)):
        struct_object.fields[i][1] = fields[i][1]
    return struct_object

case Indexer(identifier, indexVal):
    # print(f"identifier: {identifier}, indexVal: {indexVal}")
    if not isinstance(indexVal, Identifier):
        i = eval_literals(eval(indexVal, program_env))
    else:
        i = indexVal            
    objectToBeIndexed = eval(program_env.get(identifier.name), program_env)
    if isinstance( objectToBeIndexed, Struct):
        return objectToBeIndexed.get(i)
    if(len(objectToBeIndexed.value) <= i):
        raise InvalidProgram(f"Index out of range")
    if isinstance(objectToBeIndexed, ListLiteral):
        return objectToBeIndexed.value[i]
    if isinstance(objectToBeIndexed, StringLiteral):
        return StringLiteral(objectToBeIndexed.value[i]) 
    raise InvalidProgram(f"TypeError: {identifier} is not iterable")
```


#### Example
```python
struct Student {name, roll, std};
assign s = Student("John", 20110048);
s[std] = "13";
assign t = Student("chirag", 20110047, "12");
t[std] = "10";
print(s);
print(t);
print(t[roll]);
```

#### Output
```python
Struct Student begin
['name', 'John'], ['roll', 20110048], ['std', '13'],
end
Struct Student begin
['name', 'chirag'], ['roll', 20110047], ['std', '10'],
end
20110047
```



## Dheeraj Yadav(@dheera-01)
Completed static typechecking module. Wrote unit tests for type checking covering different edge cases.
Wrote unit tests for lexer and parser.

## Rahul Rai(@RahulRai02)

Completed the list feature implementation with features like POP, APPEND, HEAD, TAIL, LEN and element assignment working.
Changed code in order to handle multidimensional list.
For now, using explict keywords for pop, append etc because there is no other way since our language in not object oriented.

## @Sandeep-Desai
Completed function feature of the language. 
Wrote parser for functions and solved some errors related to the same. 
Previously there was an issue with the return statement, which was fixed. 
Now functions can have multiple return statements. 
Also, recursive functions are done. Tested for cases like Fibonacci, factorial, and odd-even.

## Sankskriti Sarkar(@Sanskriti-56)
I am working on implementing bytecode generation for arithmetic operations, the logic of the code is corect however due to some reason, the code is going to case BUG whenever it is run,I suspect that the reason behind this is incorrect integration of parser with bytecode generator.
