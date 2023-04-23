# Binary Operations

### Addition (`+`):
- Supports addition of numbers (`NumLiteral`), floating-point numbers (`FloatLiteral`), and string literals (`StringLiteral`).
- If both operands are strings, it concatenates them.
- If one operand is a string and the other is a number or float, it converts the number or float to a string and concatenates them.
- Any other combination of operands results in a TypeError.

### Subtraction (`-`):
- Supports subtraction of numbers (`NumLiteral`) and floating-point numbers (`FloatLiteral`).
- Any other combination of operands results in a TypeError.

### Multiplication (`*`):
- Supports multiplication of numbers (`NumLiteral`), floating-point numbers (`FloatLiteral`), and string literals (`StringLiteral`).
- If one operand is a string and the other is a number, it repeats the string by the number of times specified by the number operand.
- Any other combination of operands results in a TypeError.

### Division (`/`):
- Supports division of numbers (`NumLiteral`) and floating-point numbers (`FloatLiteral`).
- Raises a ZeroDivisionError if the divisor is zero.
- Any other combination of operands results in a TypeError.

### Floor Division (`//`):
- Supports floor division of numbers (`NumLiteral`) and floating-point numbers (`FloatLiteral`).
- Raises a ZeroDivisionError if the divisor is zero.
- Any other combination of operands results in a TypeError.

### Modulo (`%`):
- Supports modulo operation on numbers (`NumLiteral`) and floating-point numbers (`FloatLiteral`).
- Raises a ZeroDivisionError if the divisor is zero.
- Any other combination of operands results in a TypeError.

### Exponentiation (`**`):
- Supports exponentiation of numbers (`NumLiteral`) and floating-point numbers (`FloatLiteral`).
- Any other combination of operands results in a TypeError.

### Concatenation (`~`):
- Supports concatenation of numbers (`NumLiteral`), floating-point numbers (`FloatLiteral`), and string literals (`StringLiteral`).
- If both operands are numbers, it concatenates their string representation.
- If both operands are strings, it concatenates them.
- If one operand is a string and the other is a number or float, it converts the number or float to a string and concatenates them.
- Any other combination of operands results in a TypeError.