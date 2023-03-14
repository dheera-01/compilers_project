for loop consists of four components:
1. Initialization (assign value to variable)
2. Condition 
3. Increment/Decrement/ Any action to be performed once body is executed
4. Body

For implementing the for loop we lowered the for loop to python while loop. 

To lower the for loop to while loop we used the following steps:
1. Evaluate initialization and condition 
2. Enter the loop if condition is true
3. Evalaute the update statement 
4. Revaluate condtions and go to step 2


We can understand the implementation of for loop by looking at the code below.


```python
 case For(exp1, condition, exp2, body): 
     program_env.enter_scope() 
     eval(exp1, program_env) 
     cond=eval(condition,program_env) 
  
     while(cond==BoolLiteral(True)): 
         program_env.enter_scope() 
         eval(body,program_env) 
         eval(exp2,program_env) 
         cond=eval(condition,program_env) 
         program_env.exit_scope() 
  
     program_env.exit_scope() 
     return None 

```

On complete execution of for loop returns ```None```.


### Parsing the for loop

```python
def parse_for(self):
        """parse for statement
        Returns:
            For: return AST of for loop
        """
        self.lexer.match(Keyword("for"))
        self.lexer.match(Bracket("("))
        initial = self.parse_expr()
        cond = self.parse_simple()
        self.lexer.match(EndOfLine(";"))
        termination = self.parse_expr()
        self.lexer.match(Bracket(")"))
        for_body = self.parse_block()
        # print(self.lexer.peek_current_token())
        return For(initial, cond, termination, for_body)
```


Example:

```python
for(assign i=1; i<=5; i=i+1)
{
    print(i);
};
```
Output:

```python
1
2
3
4
5
```

To know more about about how to use for loop checkout [this](usage/for.md).
