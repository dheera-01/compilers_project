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

```

On complete execution of for loop returns ```None```.



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