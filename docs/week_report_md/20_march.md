# Weekly Report - 13 March 23

## @chirag-25
Reviewed and updated documentation.

## Dheeraj Yadav(@dheera-01)
Reviewed and updated documentation.

## Rahul Rai(@RahulRai02)
Reviewed and updated documentation.

## Sankskriti Sarkar(@Sanskriti-56)

### **Handling multiple assignments using update-**
In our previous code, update was only used to change value of a single variable, so I have tried to modify it to allow updation of multiple variables in single statement.
```
case Update(assignments, program_env):
    updated_vars = []
    for identifier, op, right in assignments:
        if type(right).__name__ == 'list':
            program_env.update(identifier, right)
        else:
            value = eval(right, program_env)
            if op._operator == "=":
                program_env.update(identifier, value)
            else:
                v = eval(BinOp(identifier, op._operator[: len(op._operator) -1], right), program_env)
                program_env.update(identifier, v)
        updated_vars.append(identifier)
    return updated_vars
```    

Here, I have used assignments which is a list of tuples that contains an identifier, operator and its corresponding right hand side which I have iterated on using a for loop, then, I am checking case by case if RHS is a list or a single value, accordingly I am calling  update.
Also, all these updated variables are added to a list  ' updated_vars'.
#### Parser code-
```
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

    # Parse the right-hand side of the assignment
    right_parts = []
    right_parts.append(self.parse_simple())
    while self.lexer.peek_current_token() == Operator(","):
        self.lexer.advance() # consuming the comma
        right_parts.append(self.parse_simple())

    self.lexer.match(EndOfLine(";"))
    updates = [Update(left_part, op, right_part) for right_part in right_parts]
    if len(updates) == 1:
        return updates[0]
    else:
        return MultipleUpdates(updates)
```    
right_parts is a list, to contain all values in RHS,we store all updated values in a list 'updates', MultipleUpdates() is an AST node that has updates as its children.

## @Sandeep-Desai
Reviewed and updated documentation.