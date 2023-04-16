# Lists

Lists can be declared in the way we declared lists in python language. The syntax is in the form of `[]` brackets. The list can be declared in a similar way as we declare a variable. So basically, we are assigning a identifier to a list when `assign` is called.

### Syntax

#### List declaration

```python
# INPUT
assign arr = [1, 2, 3, 11, 18];
print(arr);
```
```python
# OUTPUT
[1, 2, 3, 11, 18]
```

```python
# INPUT
assign arr = ["Hi", 2, "hello", 11, 18];
print(arr);
```
```python
# OUTPUT
["Hi", 2, "hello", 11, 18]
```

Here we have made the list declaration in such a way that it can be reassigned as well. Example is shown below:-
```python
# INPUT
assign arr = [1, 3, 5, 11, 29];
print(arr);

arr = [2, 4, 6, 12, 30];
print(arr);
```

```python
# OUTPUT
[1, 3, 5, 11, 29]
[2, 4, 6, 12, 30]
```
#### Multi-dimensional list declaration

```python
# INPUT
assign arr = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
print(arr);
```
```python
# OUTPUT
[[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```


### Operations

#### Indexing


```python   
# INPUT
assign arr = [1, 2, 3, 11, 18];
print(arr[0]);
```
```python
# OUTPUT
1
```
#### Length of the list


```python
# INPUT
assign arr = [1, 2, 3, 11, 18];
print(arr.LEN);
```
```python
5
```

#### Head of the list


```python
# INPUT
assign arr = [1, 2, 3, 11, 18];
print(arr.HEAD);
```
```python
1
```

#### Tail of the list


```python
# INPUT
assign arr = [1, 2, 3, 11, 18];
print(arr.TAIL);
```
```python
18
```

#### Append to the list


```python
# INPUT
assign arr = [1, 2, 3, 11, 18];
arr.APPEND(20);
print(arr);
arr.APPEND([21, 22, 23]);
print(arr);

# You could also do this
arr = arr.APPEND(20);
```
```python
[1, 2, 3, 11, 18, 20]
[1, 2, 3, 11, 18, 20, [21, 22, 23]]
[1, 2, 3, 11, 18, 20, [21, 22, 23], 20]


```

#### Pop from the list  


```python
# INPUT
assign arr = [1, 2, 3, 11, 18];
arr.POP;
print(arr);
```
```python
[1, 2, 3, 11]
```

#### Change one element of the list


```python
# INPUT
assign arr = [1, 2, 3, 11, 18];
arr[3] = 20;
print(arr);
```
```python
[1, 2, 3, 20, 18]
```

#### Concatenate two lists


```python
# INPUT
assign arr1 = [1, 2, 3, 11, 18];
assign arr2 = [4, 5, 6, 12, 19];
arr3 = arr1 + arr2;
print(arr3);
```
```python
[1, 2, 3, 11, 18, 4, 5, 6, 12, 19]
```