# Print

Print takes the value as an AST so we can print the evaluated value of the AST. The cases include NumLiteral, StringLiteral, Identifier, BoolLiteral, FloatLiteral and list. If the value is not of type NumLiteral, StringLiteral, Identifier, BoolLiteral, FloatLiteral or list, then it will raise an error.

```python
#INPUT:

# PRINT STRING
print("Hello World");

# PRINT LIST
assign arr = [1, 2, 3];
print(arr);

assign p = arr[1];
print(p);

# PRINT Identifier
assign a = 5;
print(a);

```

```python
#OUTPUT:
Hello World
[1, 2, 3]
2
5
```



