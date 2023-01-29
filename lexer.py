from fractions import Fraction
from dataclasses import dataclass
from typing import Optional, NewType


@dataclass
class NumLiteral:
    _number: int


@dataclass
class floatLiteral:
    _float: float


@dataclass
class Bool:
    _bool: bool


@dataclass
class Keyword:
    _keyword: str

# variable names are identifiers


@dataclass
class Identifier:
    _variable: str


@dataclass
class Operator:
    _operator: str


@ dataclass
class StringLiteral:
    _string: str


Token = NumLiteral | floatLiteral | Bool | Keyword | Identifier | Operator | StringLiteral


class EndOfStream(Exception):
    pass


@dataclass
class Stream:
    source: str
    pos: int

    # set the source to the string s and the position to 0 to start
    def from_string(s):
        return Stream(s, 0)

    # return the next character in the stream and advance the position
    def next_char(self):
        if self.pos >= len(self.source):
            raise EndOfStream(f"End of stream reached")
        self.pos = self.pos + 1
        return self.source[self.pos - 1]

    # decrement the position by 1 to go back one character
    def unget(self):
        assert self.pos > 0
        self.pos = self.pos - 1

# Define the token types.
class EndOfTokens(Exception):
    pass


keywords = "if then else end while for do done let".split()
symbolic_operators = "+ - * / % // ** < > <= >= == !=  << >> =".split()
word_operators = "and or not is in".split()
whitespace = " \t\n"


def word_to_token(word):
    if word in keywords:
        return Keyword(word)
    if word in word_operators:
        return Operator(word)
    if word == "True":
        return Bool(True)
    if word == "False":
        return Bool(False)
    return Identifier(word)


class TokenError(Exception):
    pass


@dataclass
class Lexer:
    stream: Stream
    save: Token = None

    def from_stream(s):
        return Lexer(s)

    def next_token(self) -> Token:
        try:
            match self.stream.next_char():

                # reading the operators
                case c if c in symbolic_operators:
                    while True:
                        s = self.stream.next_char()
                        if s in symbolic_operators:
                            c = c+s
                        else:
                            self.stream.unget()
                            if c in symbolic_operators:
                                return Operator(c)
                            else:
                                # =! is not a valid operator
                                raise TokenError(f"{c} is an Invalid operator")

                # reading the string literal
                case c if c == '"':
                    st = ''
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c == '"':
                                return StringLiteral(st)
                            else:
                                st = st + c
                        except EndOfStream:
                            raise TokenError("Unterminated string literal")
                case c if c == "'":
                    st = ''
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c == "'":
                                return StringLiteral(st)
                            else:
                                st = st + c
                        except EndOfStream:
                            raise TokenError("Unterminated string literal")

                # reading the numbers
                case c if c.isdigit():
                    n = int(c)
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c.isdigit():
                                n = n*10 + int(c)
                            else:
                                self.stream.unget()
                                return NumLiteral(n)
                        except EndOfStream:
                            return NumLiteral(n)

                # reading the identifiers
                case c if c.isalpha() or c == "_":
                    s = c
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c.isalpha() or c == "_" or c.isdigit():
                                s = s + c
                            else:
                                self.stream.unget()
                                return word_to_token(s)
                        except EndOfStream:
                            return word_to_token(s)

                # readig the white space
                case c if c in whitespace:
                    return self.next_token()
        except EndOfStream:
            raise EndOfTokens(f"End of tokens reached")

    def peek_token(self) -> Token:
        if self.save is not None:
            return self.save
        self.save = self.next_token()
        return self.save

    def advance(self):
        assert self.save is not None
        self.save = None

    def match(self, expected):
        if self.peek_token() == expected:
            return self.advance()
        raise TokenError()

    # __iter__ and __next__ are used to make the Lexer iterable
    # __iter__ returns the object itself
    # __next__ returns the next token
    # __next__ raises StopIteration when there are no more tokens

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.next_token()
        except EndOfTokens:
            raise StopIteration


file = open("program.txt", "r")
program= file.read()
for i in Lexer.from_stream(Stream.from_string(program)):
    print(i)