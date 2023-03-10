# Parser

## Operator Precedence and Associativity 
| Operator | Description | Associativity |
| --- | --- | --- |
| `()`,`{}`,`[]`  | Parentheses | Left-to-right |
| `**` | Exponentiation | Right-to-left |
| `+x`, `-x` | Positive, Negative | Right-to-left |
| `*`, `/`, `//`, `%` | Multiplication, Division, Floor Division, Modulo | Left-to-right |
| `+`, `-` | Addition, Subtraction | Left-to-right |
| `<<`, `>>` | Bitwise Shifts | Left-to-right |
| `&` | Bitwise AND | Left-to-right |
| `^` | Bitwise XOR | Left-to-right |
| `|` | Bitwise OR | Left-to-right |
| `in`, `not in`, `is`, `is not`, `<`, `<=`, `>`, `>=`, `!=`, `==` | Comparisons, Identity, Membership | Left-to-right |
| `not x` | Boolean NOT | Right-to-left |
| `and` | Boolean AND | Left-to-right |
| `or` | Boolean OR | Left-to-right |
| `if-else` | Conditional Expression | Right-to-left |
| `lambda` | Lambda Expression | Left-to-right |
