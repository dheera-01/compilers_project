# Parser

## Operator Precedence and Associativity

| Operator                         | Description                                      | Associativity |
| -------------------------------- | ------------------------------------------------ | ------------- |
| `()`,`{}`,`[]`                   | Parentheses                                      | Left-to-right |
| `**`                             | Exponentiation                                   | Right-to-left |
| `+x`, `-x`                       | Positive, Negative                               | Right-to-left |
| `*`, `/`, `//`, `%`              | Multiplication, Division, Floor Division, Modulo | Left-to-right |
| `+`, `-`, `~`                    | Addition, Subtraction, Concatenation             | Left-to-right |
| `<`, `<=`, `>`, `>=`, `!=`, `==` | Comparisons, Identity, Membership                | Left-to-right |
| `and`                            | Boolean AND                                      | Left-to-right |
| `or`                             | Boolean OR                                       | Left-to-right |

## Grammar

```bnf
atom:
    "(" simple_expr ")"
    | "[" simple_expr  "]"
    | "{" simple_expr   "}"
    | NumLiteral
    | StringLiteral
    | Identifier
    | BoolLiteral
    | FloatLiteral
    | slice
    | let_expr

exponent:
    atom
    | atom "**" atom

unary:
    exponent
    | "+" exponent
    | "-" exponent
    | "~" exponent

mult:
    unary
    | unary "*" unary
    | unary "/" unary
    | unary "//" unary 
    | unary "%" unary  

add:
    mult
    | mult "+" mult
    | mult "-" mult

cmp:
    add
    | add "<" add
    | add "<=" add
    | add ">" add
    | add ">=" add
    | add "!=" add
    | add "==" add

and_expr:
    cmp
    | cmp "and" cmp

or_expr:
    and_expr
    | and_expr "or" and_expr

simple_expr:
    or_expr

expr = simple_expr
    | const_assign_expr
    | assign_expr
    | update_expr
    | print_expr
    | while_expr
    | if_else_expr
    | for_expr

program:
    expr
    | expr program

block_expr:
    "{" program "}"


arg_assign:
    '='
    | '+='
    | '-='
    | '*='
    | '/='
    | '%='
    | '**='
    | '//='
    | '~='

EndOfLine:
    ';'

EndOfFile:
    "EOF"
```

## Syntax Tree

#### For loop

```bnf
for_expr:
    "for" "(" expr simple_expr EndOfLine simple_expr EndofLine expr ")" block_expr
```

Sample codes
```python
for(assign i = 0; i < 10; i = i + 1) 
{
    print(i);
}
```
```python
for(i = 0; i < 10; i = i + 1) 
{
    print(i);
}
```


#### While loop

```bnf
while_expr:
    "while" simple_expr block_expr
```

Sample code
```python
while(i < 10) 
{
    print(i);
    i = i + 1;
}
```

#### If else

```bnf
if_else_expr:
    "if" simple_expr block_expr
    | "if" simple_expr block_expr "else" block_expr
    | "if" simple_expr block_expr  elif_expr

elif_expr:
    "elif" simple_expr block_expr
    | "elif" simple_expr block_expr elif_expr
```


Sample code
```python
if(i < 10) 
{
    print(i);
}
```
```python
if(i < 10) 
{
    print(i);
}
else
{
    print("i is not less than 10");
}
```
```python
if(i < 10) 
{
    print(i);
}
elif(i < 20)
{
    print("i is not less than 10");
}
elif(i < 30)
{
    print("i is not less than 20");
}
else
{
    print("i is not less than 20");
}
```
```python
if(i < 10) 
{
    print(i);
}
elif(i < 20)
{
    print("i is not less than 10");
}
elif(i < 30)
{
    print("i is not less than 20");
}
```

#### Print

```bnf
print_expr:
    "print" simple_expr EndOfLine
```
Sample Code
```python
print("Hello World");
print(4+5+6);
print(True);
```

#### Assign

```bnf
assign_expr:
    "assign" Identifier "=" simple_expr EndOfLine |
    assign_parallel_expr EndOfLine

assign_parallel_expr:
    Identifier "=" simple_expr |
    Identifier "=" simple_expr "," assign_parallel_expr

```
Sample code
```python
assign i = 10;
assign i = 10, j = 20;
```

#### Const Assign

```bnf
const_assign_expr:
    "const" assign_expr
```
Sample code
```python
const assign i = 10;
```

#### Update

```bnf
update_expr:
    Identifier arg_assign simple_expr EndOfLine
```
Sample code
```python
i += 10;
i = i + 10;
```


#### Slice

```bnf
slice:
    "slice" "(" simple_expr ":" simple_expr ":" simple_expr ":" simple_expr ")"
```

Sample code
```python
slice("HelloWorld!":10:2:3);
```

#### Let
```bnf
let_expr:
    "let" Identifier "=" simple_expr "(" simple_expr ")"
```

Sample code
```python
let i = 5 (i + 5);
```
