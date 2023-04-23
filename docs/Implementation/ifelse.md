# If-Elif-Else

`IfElse` definition, `parser_if` and `eval of IfElse` support elif feature.

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