# Declaration
This defines an Abstract Syntax Tree (AST) for a programming language, where each class represents a different node in the tree. 

### AST None
1. `Sequence`: Represents a sequence of statements, stored as a list of AST nodes.
2. `NumLiteral`: Represents a numeric literal (integers)
3. `StringLiteral`: Represents a string literal
4. `FloatLiteral`: Represents a floating-point number literal
5. `BoolLiteral`: Represents a boolean(True False)literal
6. `Keyword`: Represents a keywords or our language.
7. `Identifier`: Represents an identifier, stored as a string. Also includes a boolean flag for indicating whether the identifier is mutable or not.
8. `Operator`: Represents an operator, stored as a string. 
9. `Bracket`: Represents a bracket `(){}[]`, stored as a string. 
10. `Comments`: Represents a comment, stored as a string. 
11. `EndOfLine`: Represents the end of a line, stored as a string `;`.
12. `EndOfFile`: Represents the end of a file, stored as a string `EOF`.
13. `Binop`: Represents a binary operator expression, consisting of a `left`hand operand, an `operator`, and a `right` hand operand.
14. `UnaryOp`: Represents a unary operator expression, consisting of an `operator` and an `operand`.
15. `ComparisonOp`: Represents a comparison operator expression, consisting of a `left` hand operand, a comparison `operator`, and a `right` hand operand.
16. `Let`: Represents a let expression, consisting of an `assign` for storing the assignment expression and an expression `e2` to evaluate after the assignment.
17. `Print`: Represents a print statement, consisting of a `value` to print.
18. `Slice`: Represents a slice expression, consisting of a string variable `string_var`, a `start` index, an `end` index, and a `step`.
19. `IfElse`: Represents an if-else statement, consisting of a `condition`, a `if_body` to evaluate if the condition is true, a j`elif_body` list for else if clauses, and an optional `else` clause.
20. `While`: Represents a while loop, consisting of a `condition` and a `body` to evaluate while the condition is true.
21. `Assign`: Represents an assignment, consisting of a variable `v` and a `right`, value assign to it.
22. `Update`: Represents an update operation, consisting of a `variable`, an `operator`, and a value as `right` to update it with.
23. `For`: Represents a for loop, consisting of three expressions `exp1` for initialization, `condition` for executing the code block, and `exp2` for updating and a body to evaluate for each iteration of the loop.

###Error Handling
1. `InvalidProgram`, error class for an invalid program 
2. `KeyError`, error class for a key errors 
3. `End0fLineError`, error class for end of line error 

###Environment
`Environment`, a class for storing variables and their values in a dictionary 
`envs` a list of dictionaries to store environments 
- `init` initializes the `envs` list with an empty dictionary 
- `enter_scope()` enters a new scope by appending an empty dictionary to `envs` 
- `exit_scope()` exits the current scope by removing the last dictionary from `envs` 
- `add(identifier, value)` adds a new variable to the current scope 
- `update(identifier, value)` updates the value of a variable in the current scope 
- `get(name)` gets the value of a variable  
