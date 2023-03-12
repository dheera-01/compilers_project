# Assign and Const

*Note: By default all variables are mutable variables. If we want to declare immutable variables, then `const` explicitly should be specified.*
## Assign
Following example illustrates the usage of `assign` keyword for declaring and updating variables.
#### Example 1
```text
assign a = 4;
print(a);
```
Output:
```text
4
```

#### Example 2
```text
assign a = 4;
assign a = 6;
print(a);
```
Output:
```text
6
```

## Const
`const` keyword is used in-front of `assign` for declaring immutable variables. Following example illustrates:
#### Example 1
```text
const assign a = 5;
print(a);
```
Output:
```text
5
```

#### Example 1
```text
const assign a = 5;
assign a = 6;
```
Output:
The above program throws the following error because we are mutating a immutable variable.
```python
.
.
InvalidProgram(f"Variable a is immutable")
.
.
```