# Weekly Report - 3 April 23

## @chirag-25

### Work Done
- completed the addition of concatenation operator (`~`)
- added the explicit error functionality


#### Concatenation Operator
Concatenation operator is used to concatenate two datatype. it will return String Literal irrespective of the datatype of the operands. It will not throw an error if the operands are not of the same datatype. Currently working only of `NumLiteral`, `StringLiteral` and `StringLiteral`.

#### Implementation
addition, subtraction and concatenation operator are parsed in the same function `parse_add` in `parser.py`. They have same preference and left to right associativity. So, I have added the concatenation operator in the same function.

```python
def parse_add(self):
    """parse the addition and subtraction operator

    Returns:
        AST: return AST of the addition and subtraction operation
    """
    left = self.parse_mult()

    while True:
        match self.lexer.peek_current_token():

            case Operator(op) if op in "+-~":
                self.lexer.advance()
                # print("before parse_add")
                m = self.parse_mult()
                # print("after parse_add",m)
                left = BinOp(left, op, m)

            case _:
                break

        return left
```

#### Eval
```python
case BinOp(left, "+", right):
    eval_left = eval(left, program_env)
    eval_right = eval(right, program_env)

    try:
        if isinstance(eval_left, FloatLiteral) or isinstance(eval_right, FloatLiteral):
            res = eval_literals(eval_left) + eval_literals(eval_right)
            return FloatLiteral(res)
        elif isinstance(eval_left, NumLiteral) and isinstance(eval_right, NumLiteral):
            res = eval_literals(eval_left) + eval_literals(eval_right)
            return NumLiteral(res)
        else: 
            raise InvalidProgram(
                f"+ not supported between instances of {eval_left} and {eval_right}")
            
    except Exception as e:
        raise InvalidProgram(
            f"+ not supported between instances of {eval_left} and {eval_right}")

# concatenation operation
case BinOp(left, "~", right):
    eval_left = eval(left, program_env)
    eval_right = eval(right, program_env)
    try:
        concat_similar_addition = ["StringLiteral", "NumLiteral", "FloatLiteral"]
        if eval_left.__class__.__name__  in concat_similar_addition and eval_right.__class__.__name__ in concat_similar_addition:
            res = str(eval_literals(eval_left)) + str(eval_literals(eval_right))
            return StringLiteral(res)
        
        raise InvalidProgram(
            f"~ not supported between instances of {eval_left} and {eval_right}")
    
    except Exception as e:
        raise InvalidProgram(
            f"~ not supported between instances of {eval_left} and {eval_right}")
```
Addition was changed to support addition of `NumLiteral` and `FloatLiteral` only. Concatenation operator is added to support concatenation of `NumLiteral`, `StringLiteral` and `FloatLiteral`.


#### Example
```python
print(1+1.4);
print("Hello"~"World"~1~1.5); # "HelloWorld"
```
Output:
```text
2.4
HelloWorld11.5
```

#### Special Use
can be used to convert the the Literal to String Literal.

```python
assign a = 1;
a = 1 ~ "";
print(a);
print(a  + 1);
```

Output, Give error:
```text
1
InvalidProgram: + not supported between instances of StringLiteral("1") and NumLiteral(1)
```

#### Error Handling

created new class called `Token` that will store `tokens` along with the `line_number` and `column_number`. This will be used to give the error message with the line number and column number.

```python
# comments are not tokens they are removed by the lexer
tokens = NumLiteral | FloatLiteral | BoolLiteral | Keyword | Identifier | Operator | StringLiteral | Bracket | EndOfLine | EndOfFile

@dataclass
class Token:
    token: tokens
    line: int # line number
    column: int # column number

    def __repr__(self) -> str:
        return f"{self.token} [{self.line}:{self.column}]"
        # return f"{self.token}"
```

`Stream` class was updated, it now represents a stream of characters from a source string, along with information about the current position within the stream, the current line number, and the current column number. The class provides methods for manipulating the position within the stream, reading and unreading characters, and updating the line and column numbers as characters are read.

##### Attributes:

`source`: a string representing the source of the stream
`pos`: an integer representing the current position within the stream
`code`: a list of strings representing the lines of code in the stream. we be used to display the line of code with the error.
`line_num`: an integer representing the current line number within the stream
`column_num`: an integer representing the current column number within the stream

##### Methods:

`from_string(s: str) -> Stream`: a class method that creates a new `Stream` object from the string `s`. The `pos` attribute is initialized to 0.

`new_line() -> None`: increments the `line_num` attribute by 1 (line number starts with 0) and resets the `column_num` attribute to 0.

`unget_line() -> None`: decrements the `line_num` attribute by 1 and resets the `column_num` attribute to 0.

`next_column() -> None`: increments the `column_num` attribute by 1.

`unget_column() -> None`: decrements the column_num attribute by 1.

`next_char() -> str`: returns the current character in the stream and advances the `pos` attribute by 1 to go to the next character. If the current character is a newline character, the `line_num` attribute is incremented by 1 and the column_num attribute is reset to 0 (calling `next_line()`). Otherwise, the `column_num` attribute is incremented by 1. If the end of the stream is reached, an EndOfStream exception is raised.

`unget() -> None`: decrements the `pos` attribute by 1 to go back one character.



```python
@dataclass
class Stream:
    source: str
    pos: int
    code: List[str]
    line_num: int = 1
    column_num: int = 0

    def from_string(s):
        """Set the source to the string s and the position to 0 to start

        Args:
            s (str): string to be set as source

        Returns:
            Stream: Stream object
        """
        code = [""] + s.splitlines() 
        return Stream(s, 0, code)
    def new_line(self):
        """Increment the line number and reset the column number
        """
        self.line_num = self.line_num + 1
        self.column_num = 0
        # self.code.append("")
    
    def unget_line(self):
        """Decrement the line number and reset the column number
        """
        self.line_num = self.line_num - 1
        self.column_num = 0
    
    def next_column(self):
        """Increment the column number
        """
        self.column_num = self.column_num + 1
    
    def unget_column(self):
        """Decrement the column number
        """
        assert self.column_num > 0
        self.column_num = self.column_num - 1

    def next_char(self):
        """Return the current char in the stream and advance the position by 1 to go to the next char. It will also increment the column number and line number if the current char is a new line
        column number is reset to 0 if the current char is a new line, else column number point the returned char

        Raises:
            EndOfStream: if the end of the stream is reached

        Returns:
            str: current character
        """
        if self.pos >= len(self.source):
            raise EndOfStream(f"End of stream reached")
        self.pos = self.pos + 1
        next_character = self.source[self.pos - 1]
        if next_character == "\n":
            self.new_line()
            return next_character
        # self.add_to_code(next_character)
        self. next_column()
        return next_character

    def unget(self):
        """Decrement the position by 1 to go back one character. it will also decrement the column number.
        """
        assert self.pos > 0
        self.pos = self.pos - 1
        # self.code[-1] = self.code[-1][:-1]
        self.unget_column()
```

##### Error mesage
```python 
raise TokenError(f"In Line {self.stream.line_num}\n{self.stream.code[self.stream.line_num]}\n{' ' * (start_column - 1)}^\n{c + s} is an Invalid operator")
```

##### Usage

In Lexer
```python
print(1+2);
print(3+4+5+55+5);
print(5+6+2+"hello");

```

output:
```text
declaration.InvalidProgram: In line 3
print(5+6+2+"hello");
           ^
+ not supported between instances of NumLiteral(13) and StringLiteral("hello")
```
image.pn


## Dheeraj Yadav(@dheera-01)
Implemented static type checking in separate file. Also wrote some basic pytest cases for different cases.

## Rahul Rai(@RahulRai02)
Debugged code for iteration over lists

The majority of the time spent on this task was devoted to debugging the code for iterating over the lists. The original implementation was causing unexpected errors when iterating over lists, but after careful inspection, the issue was identified and resolved. This commit on branch "Issue_37" includes the corrected code for iterating over lists.

The testcase is currently written in program.txt

## @Sandeep-Desai
The following work done this week:

Previously, the function could have only one return statement, solved that issue and now we can write multiple return statements in a function.
Implemented parser for function declaration and function call.
Previously, the if return statement is some other constructs such as if, while, for, etc. then the return statement was not working. Solved that issue by raising return value as exception and catching it in the main function.
Wrote some test cases for the above mentioned issues.
Now the following example works:
Simple Hello world print function;
Functions to add two numbers and return the sum
Function with if and else statements
Function with while loop
Factorial function implemented using recursion
The following work is planned for next week:

Solve some issues related some complex recursive functions such as fibonacci series.
Current implementation of function may have some unknown scoping related issues which needed to be addressed.

## Sankskriti Sarkar(@Sanskriti-56)
Reviewed code for unary boolifying operator and fixed errors in it.
