# Weekly Report - 13 March 23

## @chirag-25
- Made an ide for our complier
- Added and and or operator in our complier
- Added elif feature in the existing else if branch
- Added update statements
- Solved the issue with end of line feature in the parser
- test cases for lexer, parser and eval
- Documentation of parser


### IDE
This is a Streamlit-based IDE for running code using our compiler. The IDE consists of a main page and a sidebar.

Main Page:
- Title: `IDE for Our Complier`
- Text area for entering the code
- Button `Run` for running the code
- Text area for displaying the output of the code

Sidebar:
- `File uploader` for uploading a text file containing the code
- `Text input` for entering the name of the downloaded file
- `Download` button for downloading the code in a text file

The main logic of the IDE is as follows:

- Import necessary modules and libraries, including Streamlit, and the custom modules eval_for_parser which evaluates the code using our compiler.
- Set up the main page and the sidebar using the Streamlit library.
- Define the behavior of the "Run" button, which calls the eval_for_parser module to evaluate the input code using our compiler and displays the output in the output text area.
- Define the behavior of the download button, which saves the input code to a text file using the entered file name.

Overall, this IDE provides a simple and user-friendly interface for running code using our compiler and saving it to a text file for later use. It also give displays errors if grammar or syntax are not correct.

`Link`: https://dheera-01-compilers-project-playground-3e3vjx.streamlit.app


### and, or operator
```python
def parse_and(self):
    """parse the and Operator

    Returns:
        AST: return the AST of the and operator
    """  
    left = self.parse_cmp()
    while True:
        match self.lexer.peek_current_token():
            case Operator(op) if op == "and":
                self.lexer.advance()
                right = self.parse_cmp()
                left = ComparisonOp(left, op, right)
            case _:
                break
    return left
    pass

def parse_or(self):
    """parse the or operator

    Returns:
        AST: return AST of the or operator
    """
    
    left = self.parse_and()
    while True:  
        match self.lexer.peek_current_token():
            case Operator(op) if op == "or":
                self.lexer.advance()
                right = self.parse_and()
                left =  ComparisonOp(left, op, right)
            case _:
                break
    return left
```

These two functions are part of a Parser class and are used to parse logical expressions that use the `and` and `or` operators.

`parse_and()`: Parses the `and` operator and returns the corresponding AST 
`parse_or()`: Parses the `or` operator and returns the corresponding AST.
Both functions use a while loop and the match statement to repeatedly parse sub-expressions until the entire expression has been parsed.
`and` has higher precedence than `or`.`parse_and` call other functions, `parse_cmp()` as they are below in precedence. 

Usage
```python
assign i = 1;
# and has high precedence 
if(i == 0  and i == 1 or i > -1)
{
    print("Inside if");
}
else
{
    print("Inside else");
}
```
Output
```python
Inside if
```


### update statement
```python
@dataclass
class Update:
    variable: "AST"
    _operator: Operator # +=, -=, *= etc are all valid assignment operators
    right: "AST"
```
This code defines the `Update` class, which is used to represent an update expression in the abstract syntax tree (AST) of our programming language. An update expression is a type of assignment expression that updates the value of a variable by performing an operation with its current value and a new value.
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
    
    right_part = self.parse_simple()
    self.lexer.match(EndOfLine(";"))
    return Update(left_part, op, right_part)

def parse_expr(self):
    """parse the expression

    Returns:
        AST: return AST of the expression
    """
    match self.lexer.peek_current_token():
        # update statements
        case c if isinstance(c, Identifier):
            return self.parse_update()
```
The `parse_update` method parses the update expression, which represents assignments with operators such as `=, +=, -=, *= /= **= //= %=`. It first parses the left part of the expression (the identifier being assigned to), then checks if the current token is an assignment operator. If it is, it advances the lexer, parses the right part of the expression, and finally returns an Update AST node with the left, operator, and right parts.

The `parse_expr` method is responsible for parsing general expressions. It first checks if the current token is an identifier (which would indicate an update expression), and if it is, calls `parse_update`. 

```python
case Update(identifier, op, right):
    value = eval(right, program_env, environment)
    if op._operator == "=":
        program_env.update(identifier, value)
    else:# op is +=, -=, *=, /=, %=, **= (binop of first to second last char)
        v = eval(BinOp(identifier, op._operator[: len(op._operator) -1], right), program_env, environment)
        program_env.update(identifier, v)
    return None 
```
This code block handles the evaluation and assignment of values for an `Update AST` node in the interpreter.

It first evaluates the right-hand side expression using the current program environment(which contains the current values of all variables).

If the assignment operator is simply `=`, it updates the value of the left-hand side identifier with the evaluated value.

If the assignment operator is a compound assignment operator such as `+=`, `-=` etc., it constructs a new `BinOp AST` node with the left-hand side identifier, the corresponding binary operator (e.g. `+ for +=`), and the evaluated right-hand side expression. It then evaluates this `BinOp` AST node and updates the value of the left-hand side identifier with the resulting value.

The function returns `None` because the `Update AST` node does not have a value in and of itself - its purpose is to modify the value of a variable.

Usage
```python
assign i = 5;
#assign i = 9;# will give error
#i = i + j; #will give error
assign j = 6;
i += j;
print(i);
print(j);
```
Output
```python
11
6
```

### elif feature

`IfElse` definition, `parser_if` and `eval of IfElse` was updated to support elif feature.

```python
@dataclass
class IfElse:
    condition: ComparisonOp
    if_body: Sequence
    elif_body: list(["AST"])
    else_body: Sequence
```
`elif_body` is added which is a list of `IfElse` objects. The `IfElse` object. The `elif_body` list is empty if there are no elif blocks in the if-else statement.

```python
def parse_if(self):
    self.lexer.match(Keyword("if"))
    c = self.parse_simple()  # parse the condition which is a simple expression
    if_branch = self.parse_block()
    # single if statement
    if self.lexer.peek_current_token() != Keyword("else") and self.lexer.peek_current_token() != Keyword("elif"):
        return IfElse(c, if_branch)
    elif_list = []
    while self.lexer.peek_current_token() == Keyword("elif"):
        self.lexer.advance()
        elif_condition = self.parse_simple()
        elif_body = self.parse_block()
        elif_list.append(IfElse(elif_condition, elif_body))            
    
    # if and elif are allowed without else  
    if self.lexer.peek_current_token() != Keyword("else"):
        return IfElse(c, if_branch, elif_list)
    
    self.lexer.match(Keyword("else"))
    else_branch = self.parse_block()
    return IfElse(c, if_branch, elif_list, else_branch)
```
The `parse_if()` method is responsible for parsing an if-else statement and returning an AST object of the parsed statement. The `parse_if()` method returns an AST object of the parsed if-else statement. The AST object can be used later for evaluating the statement during program evaluation.

The `parse_if()` method first matches the if keyword using a lexer object and then parses the condition of the statement using the `parse_simple()` method. The method then parses the body of the if block using the `parse_block()` method.
If there are no `elif` or `else` blocks following the `if` block, the method returns an IfElse object containing the condition and the `if_branch` body.

If there are one or more `elif` blocks following the `if` block (if `elif` is used before if then that case is also handled with will give error), the method uses a loop to parse each `elif` block. For each `elif` block, the method matches the `elif` keyword using the lexer object, parses the condition of the `elif` and then parses the body of the `elif` block. 
After parsing all the `elif` blocks, the method checks if there is an `else` block following the `if-elif` blocks. If there is no `else` block, the method returns an IfElse object containing the condition, `if_body` and `elif_list`. This is for the case when there is an `if-elif` block without an `else` block.

If there is an `else` block, the method matches the `else` keyword using the lexer object, parses the body of the `else` block using the `parse_block()` method. The method then returns an IfElse object containing the `c` condition, `if_branch` body, `elif_list`, and `else_branch`.
Overall, the `parse_if()` method is responsible for parsing and constructing the AST object for an if-else statement.

``` python
case IfElse(condition_ast, if_ast, elif_list ,else_ast):
    condition_res = eval(condition_ast, program_env, environment)
    if eval_literals(condition_res) == True:
        program_env.enter_scope()
        eval(if_ast, program_env, environment)
        program_env.exit_scope()
        return None
    
    if len(elif_list) != 0:
        for elif_ast in elif_list:
            elif_condition = eval(elif_ast.condition, program_env, environment )
            if eval_literals(elif_condition) == True:
                program_env.enter_scope()
                eval(elif_ast.if_body, program_env, environment)
                program_env.exit_scope()
                return None
    
    if else_ast != None:
        program_env.enter_scope()
        eval(else_ast, program_env, environment)
        program_env.exit_scope()
        return None
    return None
            
```
The above code evaluates the condition AST object using the `eval()` and then checks if the evaluated condition is True by calling the eval_literals() function. If the condition is True, it enters a `new scope` and evaluates the if block AST object using the `eval()` function in that scope. It then `exit the scope` and returns None.

If there `elif` blocks in the `elif_list`, the code iterates through each `elif` block AST object, evaluates the condition using the `eval()` function, and checks if it is True using the eval_literals() function. If the condition is True for any elif block, the code enters a new scope, evaluates the corresponding if block AST object, exits the scope, and returns None.

The code then checks if there is an `else` block AST object. If there is, it enters a new scope, evaluates the else block AST object using the `eval()` function, exits the scope, and returns None.

Usage
```python
assign i = 5;
if(i>5)
{
    print("inside if");
} 
elif(i == 4)
{
    print("elif 1");
}
elif(i == 5)
{
    print("elif 2");
}
else
{
    print("else");
}
```
Output
```python
elif 2
```

## Dheeraj Yadav(@dheera-01)

### Work Done
- Documentation: Implementation and usage docs of strings, assign, const, and variable scoping(environment). Issue reference [#7](https://github.com/dheera-01/compilers_project/issues/7).
- Eval fix: Eval was returning the values of python's datatype. Fixed issue [#5](https://github.com/dheera-01/compilers_project/issues/5).
- Disallow mutable variables to change type. Issue reference [#11](https://github.com/dheera-01/compilers_project/issues/11).
- Added a python script for testing all the added testcases in a single run and see the report. Issue reference [#12](https://github.com/dheera-01/compilers_project/issues/12).
- Added first 4 euler questions as testcases and their expected output for above script. Issue reference [#22](https://github.com/dheera-01/compilers_project/issues/22).
- Fixed the Multiple assign parser. [Commit reference](https://github.com/dheera-01/compilers_project/commit/d1ff5277f74526aa2b130330690ce3401bd32f93).
- Reviewed everyone's code and merged features logically from different branches into development. Resolved errors which evolved due to conflicts in the feature implementation. Following are some significant commits related to this work:
  - https://github.com/dheera-01/compilers_project/commit/e5869a7ef2674daff3816f2ab57fb5fdcc5be790
  - https://github.com/dheera-01/compilers_project/commit/0745aa483be8f5ab240f3d8b2d7cdb53a3075d0b
  - https://github.com/dheera-01/compilers_project/commit/bf4dd015e7db1e4f5ba069fc1754dfeb5af671c1
  - https://github.com/dheera-01/compilers_project/commit/cf78937fdebf784728567bf706a26cbdb9be9785
  - https://github.com/dheera-01/compilers_project/commit/3c6e46e0a48064c595f3aff41d2aa34380f7f1c1
  - https://github.com/dheera-01/compilers_project/commit/383d6bf9e6196c1be4d34a4b94c828e3bf44878f

## Rahul Rai(@RahulRai02)

Work done:-
For the last week, i have worked on list declaration without the explicit keyword `list` and indexer for list and string. I have also reviewd the Issue #5 of the project. I have also worked on the documentation of the list declaration, indexer and print.

### List declaration

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

#### How to declare a list?

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

#### Parser for list declaration

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

### Indexer for list and string

I have added a keyword `index` to index a list or string but now i have removed it and we can index it in the same way as we index a list or string in python. Example is shown below:-

Detailed description is shown below:-

The indexer is responsible for indexing the data structure which is indexable. In our cases, till now we can index a list and a string.

#### Syntax

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

#### Class for Indexer

We have created class Indexer which takes val as Identifier and the index as AST. Below is the class declaration:-

```python
@dataclass
class Indexer:
    val: Identifier
    index: 'AST'

    def __repr__(self) -> str:
        return f"Indexer({self.val}[{self.index}])"
```

#### How is the Indexer class evaluated?
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

#### How to parse the Indexer class?

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

## Sankskriti Sarkar(@Sanskriti-56)

# Correcting parallel let :-
The final corrected code for parallel let which is logically same as assigning values to multiple variables in one statement has been pushed into the repository. The modification for eval_for_parser file and parser_1 is as given below:

```python
case Assign(left, right):
        
            curr_env = program_env.envs[-1]
            if isinstance(left, tuple):  # check if left-hand side is a tuple(for multiple assignments)
    
                value = [eval(i, program_env, environment) for i in right]
       
                for i, identifier in enumerate(left):
                    if identifier.name in curr_env:
                        program_env.update(identifier, value[i])
                    else:
                        program_env.add(identifier, value[i])
        
                return None
        
            else:  # left-hand side is a single identifier
        
       
                value = eval(right, program_env, environment)
        
                if left.name in curr_env:
                    program_env.update(left, value)
                else:
                    program_env.add(left, value)
                return None
```

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

The code above implements parallel let in following form:
assign x = 4, y = 6*5, z = "HelloWorld!", w = [1,2,3,4];    

# Implementing unary boolifying operator
For declaration.py

```python
@dataclass
class Boolify:
    operand: 'AST'

    def __repr__(self) -> str:
        return f"Boolify({self.operand})"

    def __bool__(self):
        if isinstance(self.operand, StringLiteral):
            return bool(self.operand.value)
        elif isinstance(self.operand, NumLiteral):
            return bool(self.operand.value)
        else:
            raise InvalidException
_bool method checks if operand is string or number then accordingly if it is empty or 0 it returns False else it returns True_            
```

For eval_for_parser.py

```python
case Boolify(e):
    return bool(eval(e, program_env, environment))
```
