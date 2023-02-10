from fractions import Fraction
from dataclasses import dataclass
from typing import Optional, NewType


@dataclass
class NumLiteral:
    _number: int

    def __repr__(self) -> str:
        return f"NumLiteral({self._number})"


@dataclass
class FloatLiteral:
    _float: float

    def __repr__(self) -> str:
        return f"FloatLiteral({self._float})"


@dataclass
class BoolLiteral:
    _bool: bool

    def __repr__(self) -> str:
        return f"BoolLiteral({self._bool})"


@dataclass
class Keyword:
    _keyword: str

    def __repr__(self) -> str:
        return f"Keyword({self._keyword})"

# variable names are identifiers


@dataclass
class Identifier:
    _variable: str

    def __repr__(self) -> str:
        return f"Identifier({self._variable})"


@dataclass
class Operator:
    _operator: str

    def __repr__(self) -> str:
        return f"Operator({self._operator})"


@ dataclass
class StringLiteral:
    _string: str

    def __repr__(self) -> str:
        return f"StringLiteral({self._string})"


@dataclass
class Bracket:
    _bracket: str

    def __repr__(self) -> str:
        return f"Bracket({self._bracket})"


@dataclass
class Comments:
    _comment: str

    def __repr__(self) -> str:
        return f"Comments({self._comment})"


@dataclass
class EndOfLine:
    _eol: str

    def __repr__(self) -> str:
        return f"EndOfLine({self._eol})"


@dataclass
class EndOfFile:
    _eof: str

    def __repr__(self) -> str:
        return f"EndOfFile({self._eof})"

# comments are not tokens they are removed by the lexer
Token = NumLiteral | FloatLiteral | BoolLiteral | Keyword | Identifier | Operator | StringLiteral | Bracket | EndOfLine | EndOfFile


class EndOfStream(Exception):
    pass


@dataclass
class Stream:
    source: str
    pos: int

    def from_string(s):
        """Set the source to the string s and the position to 0 to start

        Args:
            s (str): string to be set as source

        Returns:
            Stream: Stream object
        """
        return Stream(s, 0)

    def next_char(self):
        """Retrun the current char in the stream and advance the position by 1 to go to the next char

        Raises:
            EndOfStream: if the end of the stream is reached

        Returns:
            str: current character
        """
        if self.pos >= len(self.source):
            raise EndOfStream(f"End of stream reached")
        self.pos = self.pos + 1
        return self.source[self.pos - 1]

    def unget(self):
        """Decrement the position by 1 to go back one character
        """
        assert self.pos > 0
        self.pos = self.pos - 1


keywords = "if then else end while for do done let int string float def".split()
symbolic_operators = "+ - * / % // ** < > <= >= == !=  << >> = += -= *= /= %= //= **=".split()
word_operators = "and or not is in".split()
opening_brackets = "( [ { ".split()
closing_brackets = ") ] }".split()
whitespace = " \t\n"


def word_to_token(word):
    """Convert a word to a tokens. Tokens are keywords, word operators, bool literals, identifiers"""
    if word in keywords:
        return Keyword(word)
    if word in word_operators:
        return Operator(word)
    if word == "True":
        return BoolLiteral(True)
    if word == "False":
        return BoolLiteral(False)
    return Identifier(word)



class TokenError(Exception):
    # print("Token Error:", Exception)
    pass


# bracket matching list
bracket_track_list = []
bracket_map = {')': '(', '}': '{', ']': '['}
comments = []


@dataclass
class Lexer:
    stream: Stream
    save: Token = None

    def from_stream(s):
        """Set the stream to the string s

        Args:
            s (Stream): stream to be set as source 

        Returns:
            Lexer: Lexer object
        """
        return Lexer(s)

    def next_token(self) -> Token:
        """Return the next token in the stream

        Returns:
            Token: next token
        """
        try:
            match self.stream.next_char():
                # reading the end of line
                case c if c == ";":
                    return EndOfLine(c)
                    pass
                # reading the commenrts:
                case c if c == "#":
                    cmt = ""
                    while True:
                        c = self.stream.next_char()
                        if c == "\n": # one line comment ends
                            comments.append(cmt)
                            # lexer removest the comments and moves on
                            return self.next_token()
                        cmt = cmt + c
                    pass

                # reading the operators
                # special case !=
                case c if c == "!":
                    s = self.stream.next_char()
                    if c+s in symbolic_operators:
                        return Operator(c+s)
                    raise TokenError(f"{c+s} is an Invalid operator")

                case c if c in symbolic_operators:
                    start = self.stream.pos - 1
                    while True:
                        s = self.stream.next_char()
                        # +- for uniary operator ++--6
                        if s in symbolic_operators or s in "+-":
                            c = c+s
                        else:
                            self.stream.unget()
                            if c in symbolic_operators:
                                return Operator(c)
                            else:
                                for i in c:
                                    if i not in "+-":
                                        # =! is not a valid operator
                                        raise TokenError(f"{c} is an Invalid operator")
                                # here getting uniary operator
                                self.stream.pos = start+1
                                return Operator(c[0])
                                      

                # reading the string literal, "" or ''
                case c if c == '"' or c == "'":
                    current_quote = c
                    st = ''
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c == current_quote:
                                return StringLiteral(st)
                            else:
                                st = st + c
                        except EndOfStream:
                            raise TokenError(f"{st}: Unterminated string literal")

                case c if c == ".":
                    n = str(0)
                    n = n + c
                    while True:
                        c = self.stream.next_char()
                        if c.isdigit():
                            n += c
                        elif c == ".":
                            raise TokenError(f"{n+c} Invalid number")
                        else:
                            self.stream.unget()
                            return FloatLiteral(float(n))
                    pass

                # reading the numbers
                case c if c.isdigit():
                    n = int(c)
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c.isdigit():
                                n = n*10 + int(c)
                            elif c == ".":
                                n = str(n)
                                n = n + c
                                while True:
                                    c = self.stream.next_char()
                                    if c.isdigit():
                                        n += c
                                    elif c == ".":
                                        raise TokenError(
                                            f"{n+c} Invalid number")
                                    else:
                                        self.stream.unget()
                                        return FloatLiteral(float(n))
                            else:
                                self.stream.unget()
                                return NumLiteral(n)
                        except EndOfStream:
                            return NumLiteral(n)

                # bracket and bracket matching
                case c if c in opening_brackets:
                    bracket_track_list.append(c)
                    return Bracket(c)
                case c if c in closing_brackets:
                    temp = c
                    if len(bracket_track_list) == 0 or bracket_map[c] != bracket_track_list.pop():
                        print(Bracket(c))
                        raise TokenError(f"{c} Unmatched closing bracket")
                    return Bracket(c)

                # reading the identifiers
                # _, a are valid identifiers
                case c if c.isalpha() or c == "_":
                    s = c
                    while True:
                        try:
                            c = self.stream.next_char()
                            # a1, a_ is valid identifier
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
            # you can put the end of the file
            return EndOfFile("EOF")

    # see the current token without consuming it
    def peek_current_token(self) -> Token:
        """Return the current token without consuming it

        Returns:
            Token: current token
        """
        if self.save is not None:
            return self.save
        self.save = self.next_token()
        return self.save

    # consume the current token
    def advance(self):
        """Consume the current token"""
        assert self.save is not None
        self.save = None

    # match the current token against the expected token and consume it
    def match(self, expected):
        """Match the current token against the expected token and consume it if they match

        Args:
            expected (Token): expected token

        Raises:
            TokenError: if the current token is not the expected token

        Returns:
            None: if the current token is the expected token it will cosume it and return None
        """
        
        if self.peek_current_token() == expected:
            return self.advance()

        raise TokenError(f"{self.peek_current_token()} is not {expected}")

    # __iter__ and __next__ are used to make the Lexer iterable
    # __iter__ returns the object itself
    # __next__ returns the next token
    # __next__ raises StopIteration when there are no more tokens

    def __iter__(self):
        """Return the object itself

        Returns:
            Object: the object itself
        """
        return self

    def __next__(self):
        """Return the next token

        Raises:
            TokenError: if there are unmatched opening brackets
            StopIteration: if there are no more tokens

        Returns:
            Token: the next token
        """
        nxt_t = self.next_token()
        if isinstance(nxt_t, EndOfFile):
            if len(bracket_track_list) != 0:
                raise TokenError(
                    f"{' '.join(bracket_track_list)} : Unmatched opening bracket")
            raise StopIteration
        
        return nxt_t
    


# @dataclass
# class Program:
#     # 2d list of statements which make up the program and made of list of tokens
#     prgram_instruction = []

#     def form_instrutctions_of(self, t):
#         self.instruction_lists.append(list([]))
#         for i in Lexer.from_stream(Stream.from_string(t)):
#             if isinstance(i, Comments):
#                 pass
#             elif isinstance(i, EndOfLine):
#                 self.instruction_lists[-1].append(i)
#                 self.instruction_lists.append(list([]))
#             else:
#                 self.instruction_lists[-1].append(i)
#         self.instruction_lists[-1].append(EndOfFile("EOF"))

#     def print_tokens(self):
#         print("Instruction:")
#         for i in range(len(self.instruction_lists)):
#             print(self.instruction_lists[i])
#             pass


if __name__ == "__main__":

    file = open("program.txt", "r")
    program = file.read()
    # print("Program:")
    # print(program) 
    program = "+-+--+6"
    for i in Lexer.from_stream(Stream.from_string(program)):
        print(i, end=" ")
    # ins = Instrution()
    # ins.form_instrutctions_of(program)
    # ins.print_instrutions()