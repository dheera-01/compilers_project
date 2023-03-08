# Strings

## Declaring strings
Strings in our language can be declared in double quotation marks. For example, "Hello World!" is a string. Example for declaring a variable containing string `assign a = "Hello World!"`.

## Operations performed on strings
Strings in our language support following operations.

### Concatenation
Strings can be concatenated with another strings or numbers. Following examples illustrate the usage of concatenation.
#### Example 1
```text
assign a = "Hello";
assign b = " World!";
assign c = a + b;
print(c);
```
output:
```text
Hello World!
```

#### Example 2
```text
assign a = "Hello";
assign b = 3;
assign c = a + b;
print(c);
```
output:
```text
Hello3
```

### Replication
Same string can be replicated a number of time using * operator on strings. Following example illustrates the usage.
#### Example 1
```text
assign a = "Hello";
assign b = 4;
assign c = a*b;
print(c);
```
output:
```text
HelloHelloHelloHello
```

### Slicing
Strings can be sliced by passing the start, end and step arguments. Start represents the index of the first letter to start slicing with(follows 0 based indexing). End represents the index of last letter which is not included and correspondingly step represents the number of letter to skip - 1. Following example illustrates the syntax for using slice on some string.
#### Example 1
```text
assign a = "Hello World!";
assign b = slice(a:0:5:1);
print(b);
```
output:
```text
Hello
```