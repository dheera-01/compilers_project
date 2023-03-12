# Indexer

The indexer can be used to index the lists and strings. The syntax is the identifier followed by the index in square brackets. The syntax for indexing is as follows:


#### INDEX ELEMENT OF A LIST:-
```python
# INPUT
assign arr = [1, 2, 3, 11, 18];
print(arr);

assign p = arr[3];
print(p);
```
```python
# OUTPUT
[1, 2, 3, 11, 18]
11
```

#### INDEX ELEMENT OF A STRING:-
```python
# INPUT
assign str = "hello";
assign q = str[1];
print(q);
```

```python
# OUTPUT
e
```

#### ACCESSING ELEMENT OUT OF RANGE:-
```python
# INPUT
assign arr = [1, 2, 3, 11, 18];
print(arr);

assign p = arr[10];
print(p);
```

```python
# OUTPUT
[1, 2, 3, 11, 18]
Index out of range
```

#### ACCESSING ELEMENT OF A NON-ITERABLE:-
```python
# INPUT
assign a = 5;
assign p = a[1];
print(p);
```

```python
# OUTPUT
The Indentifier a is not iterable
```