# Print

### Basic Syntax:-

```python
#INPUT:
print("Hello World");

assign arr = [1, 2, 3];
print(arr);
```
```python
#OUTPUT:
Hello World
[1, 2, 3]
```

### Class structure for print:-

The print class takes value which will be of type AST. The class structure is shown below:-

```python
@dataclass
class Print:
    val: 'AST'

    def __repr__(self) -> str:
        return f"Print({self.val})"
```

### How is the print class evaluated?

We will be evaluating the value of the AST and then printing it using eval_literals function.

Here is the eval function declared in eval_for_parser.py:-

```python
        case Print(value):
            # The print function will print the evaluated value of val and return the AST val
            val = eval(value, program_env)
            if isinstance(val, NumLiteral) or isinstance(val, StringLiteral)  or isinstance(val, Identifier) or isinstance(val, BoolLiteral) or isinstance(val, FloatLiteral) or isinstance(val, list):
              
                ans = eval_literals(val)
                print(ans)
                display_output.append(str(ans))
                return None
            else:
                raise InvalidProgram(f"SyntaxError: invalid syntax for print")
```

The eval function will evaluate the value of the AST and then print it. If the value is not of type NumLiteral, StringLiteral, Identifier, BoolLiteral, FloatLiteral or list, then it will raise an error.

### Parser of print

We have created a parser in such a way that it will detect the Keyword print followed by Bracket '(' and then parse the expression inside it. Then we will match the Bracket ')' and End of line operator that is ';'. We will return the parsed experssion here to the print case in eval function. Below is the code snippet:-

```python
    def parse_print(self):
        """parse the print expression
        Returns:
            Print: return AST of the print expression
        """
        self.lexer.match(Keyword("print"))
        self.lexer.match(Bracket("("))
        print_statement = self.parse_simple()
        self.lexer.match(Bracket(")"))
        self.lexer.match(EndOfLine(';'))
        return Print(print_statement)
```

### Changes in lexer:-

We have only added a `print` keyword in Keywords of lexer.py so that the lexer can tokenize the print keyword as well.
