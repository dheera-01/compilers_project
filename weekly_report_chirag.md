#Weekly Report - 13 March 23

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

`Link`: 


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