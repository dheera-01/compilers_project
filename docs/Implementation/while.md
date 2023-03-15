# While Loops

While loops consists of two components, first is condition and second is the body. While condtions evaluates to true we execute the body. 
Body is a block of code that is executed repeatedly until the condition evaluates to false. After completion while loop returns ```None```. 

To implement the repetitive nature of while loop we used inbuilt python while loop. First we tried it using recursion but when tested this implementation against infinite loop, the maximum recursion depth of python exceeded.

We can see exact implementation of while loop by looking at the code below.

```python
 case While(cond, body):
    c = eval(cond, program_env, environment)
    while (eval_literals(c) == True) :
        program_env.enter_scope()
        eval(body, program_env ,environment)
        program_env.exit_scope()
        c = eval(cond, program_env, environment)
    return None
```

Whenever we enter a while loop we create a new scope. Once evalaution of while loop is done we destroy this scope. 

### Parsing while loop

 ```python
 def parse_while(self):
        """parse while statement
        Returns:
            while AST: return AST of while loop
        """
        self.lexer.match(Keyword("while"))
        # print(self.lexer.peek_current_token())
        cond = self.parse_simple()  # parse the condition
        # print("cond", cond)
        while_body = self.parse_block()
        return While(cond, while_body)
```

## Example

```
assign i=1;
while(i<=5)
{
    print(i);
    i=i+1;
}
```

Output:

```python
1
2
3
4
5
```


To know more about about how to use while loop checkout [this](usage/while.md).
