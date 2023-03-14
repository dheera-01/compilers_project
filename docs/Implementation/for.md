for loop consists of four components:
1. Initialization (assign value to variable)
2. Condition 
3. Increment/Decrement/ Any action to be performed once body is executed
4. Body

For implementing the for loop we lowered the for loop to while loop. Implementation for [while](Implementation/while.md) loop was already done so we used that implementation to implement for loop.

To lower the for loop to while loop we used the following steps:
1. Evaluate initialization
2. Append the Increment/Decrement expression to the body
3. Create a while loop with condition and body
4. Evaluate the while loop

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

On complete execution of for loop we return ```None```.

Example:

```python
for(assign i=1; i<=5; i=i+1;)
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

To know more about about how to use for loop checkout in the usage docs of for.