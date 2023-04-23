# Comparison Operations

### Greater Than (`>`) and Less Than (`<`)
Input:
```python
assign i = 5;
if(i > 5)
{
    print("inside if");
} 
elif(i < 5)
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
Output:
`elif 2`


### Equal To (`==`) and Not Equal To (`!=`)
Input:
```python
assign i = 5;
if(i == 5)
{
    print("inside if");
} 
elif(i != 5)
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
Output:
`inside if`


### Less Than or Equal To (`<=`) and Greater Than or Equal To (`>=`)

Input:
```python
assign i = 5;
if(i >= 5)
{
    print("inside if");
} 
elif(i <= 5)
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
Output:
`inside if`

### Logical Operators `and` and `or`

Input:
```python
assign i = 5;
if(i == 5 and i > 4)
{
    print("inside if");
} 
elif(i == 5 or i > 4)
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

Output:
`inside if`


These functions allow for the implementation of comparison operations and logical operators in a programming language, enabling the evaluation of conditional expressions in control flow statements, such as if statements and loops.