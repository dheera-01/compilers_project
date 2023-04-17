# User defined datatype (struct)

## Syntax

### Declaration

```
struct <name>
{
    <field1> <type1>;
    <field2> <type2>;
    ...
}
```

### Instantiation

```
assign <identifier> = <name>{value1,value2,...};
```
or
```
<identifier>.<field1> = <value1>;
```

## Usage:


### Example 1:
```python
struct Student {name, roll, std};
assign s = Student{};
s.std = "13";
assign t = Student{"chirag", 20110047, "12"};
t.std = "10";
print(s);
print(t);
print(s[name]);
print(t[roll]);
```

### Output:

```python
Struct Student begin
['name', None], ['roll', None], ['std', '13'],
end
Struct Student begin
['name', 'chirag'], ['roll', 20110047], ['std', '10'],
end
None
20110047
```

### Example 2:
```python

