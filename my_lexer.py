from dataclasses import dataclass
from declaration import *

# comments are not tokens they are removed by the lexer
Token = NumLiteral | FloatLiteral | BoolLiteral | Keyword | Identifier | Operator | StringLiteral | Bracket | EndOfLine | EndOfFile


class EndOfStream(Exception):
    pass



@dataclass
class Stream:
    source: str
    pos: int
    # source_code: list = None
    current_line_number: int = 1
    current_column_number: int = 0

    def from_string(s):
        """Set the source to the string s and the position to 0 to start

        Args:
            s (str): string to be set as source

        Returns:
            Stream: Stream object
        """
        source_code.clear()
        source_code.append("Start")
        for i in s.splitlines():
            source_code.append(i)
        # print(f"source code: {source_code}")
        return Stream(s, 0)

    def next_char(self):
        """Return the current char in the stream and advance the position by 1 to go to the next char
        column number is incremented by 1 so now it is pointing to the next char

        Raises:
            EndOfStream: if the end of the stream is reached

        Returns:
            str: current character
        """
        if self.pos >= len(self.source):
            raise EndOfStream(f"End of stream reached")
        self.pos = self.pos + 1

        if self.source[self.pos - 1] == "\n":
            self.current_line_number += 1
            self.current_column_number = 0
            # self.source_code.append("")
            return self.source[self.pos - 1]

        self.current_column_number += 1
        # self.source_code[-1] += self.source[self.pos - 1]
        return self.source[self.pos - 1]

    def unget(self):
        """Decrement the position by 1 to go back one character
        """

        assert self.pos > 0
        self.pos = self.pos - 1
        if self.source[self.pos] == "\n":
            self.current_line_number -= 1
            self.current_column_number = len(
                source_code[self.current_line_number - 1])
            # self.source_code.pop()
        else:
            self.current_column_number -= 1
            # self.source_code[-1] = self.source_code[-1][:-1]


keywords = """
    int string float const assign slice
    if elif else break continue
    for while break continue
    def
    print let
    slice in LEN TAIL HEAD APPEND POP
    struct
    func
    return
    """.split()

symbolic_operators = """
    + - * / % // **
    > < <= >= == !=
    >> <<
    -= += *= /= %= //= **=
    : =
    ,
    """.split()

word_operators = "and or not is in".split()
opening_brackets = "( [ { ".split()
closing_brackets = ") ] }".split()
whitespace = " \t\n"


# def word_to_token(word):
#     """Convert a word to a tokens. Tokens are keywords, word operators, bool literals, identifiers"""
#     if word in keywords:
#         return Keyword(word)
#     if word in word_operators:
#         return Operator(word)
#     if word == "True":
#         return BoolLiteral(True)
#     if word == "False":
#         return BoolLiteral(False)
#     return Identifier(word)
def word_to_token(word, line, col):
    """Convert a word to a tokens. Tokens are keywords, word operators, bool literals, identifiers"""
    if word in keywords:
        return Keyword(word, line, col)
    if word in word_operators:
        return Operator(word, line, col)
    if word == "True":
        return BoolLiteral(True, line, col)
    if word == "False":
        return BoolLiteral(False, line, col)
    return Identifier(word, line_number= line, column_number= col)


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

    def get_line_number(self):
        return self.stream.current_line_number

    def get_column_number(self):
        return self.stream.current_column_number

    def get_code(self):
        return source_code[self.get_line_number()]

    def next_token(self) -> Token:
        """Return the next token in the stream

        Returns:
            Token: next token
        """
        try:
            match self.stream.next_char():
                # reading the end of line
                case c if c == ";":
                    return EndOfLine(c, self.get_line_number(), self.get_column_number())
                    pass
                # reading the comments:
                case c if c == "#":
                    cmt = ""
                    while True:
                        c = self.stream.next_char()
                        if c == "\n":  # one line comment ends
                            comments.append(cmt)
                            # lexer removes the comments and moves on
                            return self.next_token()
                        cmt = cmt + c
                    pass

                # reading the operators
                # special case !=
                case c if c == "!":
                    s = self.stream.next_char()
                    if c + s in symbolic_operators:
                        # return Operator(c + s)
                        # -1 as != is 2 chars so pointer should be at !
                        return Operator(c + s, self.get_line_number(), self.get_column_number() - 1)
                    # raise TokenError(f"{c + s} is an Invalid operator")
                    raise TokenError(
                        f"Token Error: In line {self.get_line_number}\n{self.get_code()}\n{' ' * self.get_column_number()}^\n{c + s} is an Invalid operator")

                case c if c in symbolic_operators:
                    start = self.stream.pos - 1
                    start_column = self.get_column_number()
                    while True:
                        s = self.stream.next_char()
                        # +- for unary operator ++--6
                        if s in symbolic_operators or s in "+-":
                            c = c + s
                        else:
                            self.stream.unget()
                            if c in symbolic_operators:
                                return Operator(c, self.get_line_number(), start_column)
                            else:
                                for i in c:
                                    if i not in "+-":
                                        # =! is not a valid operator
                                        # raise TokenError(f"{c} is an Invalid operator")
                                        raise TokenError(
                                            f"Token Error: In line {self.get_line_number()}\n{self.get_code()}\n{' ' * self.get_column_number()}^\n{c} is an Invalid operator")
                                # here getting unary operator
                                self.stream.pos = start + 1
                                # return Operator(c[0])
                                self.stream.current_column_number = start_column
                                return Operator(c[0], self.get_line_number(), start_column)

                # reading the string literal, "" or ''
                case c if c == '"' or c == "'":
                    start_column = self.get_column_number()
                    current_quote = c
                    st = ''
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c == current_quote:
                                # return StringLiteral(st)
                                return StringLiteral(st, self.get_line_number(), start_column)
                            else:
                                st=st + c
                        except EndOfStream:
                            # raise TokenError(f"{st}: Unterminated string literal")
                            raise TokenError(f"Token Error: In line {self.get_line_number()}\n{self.get_code()}\n{' ' * self.get_column_number()}^\n{st}: Unterminated string literal")

                case c if c == ".":
                    start_column = self.get_column_number()
                    # temp_str=""
                    # unget_count=0
                    # list_operations=["LEN", "TAIL", "HEAD", "APPEND", "POP"]
                    # list_operations_flag=False
                    # while True:
                    #     unget_count += 1
                    #     char=self.stream.next_char()
                    #     temp_str += c
                    #     if temp_str in list_operations:
                    #         list_operations_flag=True
                    #         break

                    #     if char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    #         break

                    #     if unget_count > 6:
                    #         break

                    # for i in range(unget_count):
                    #     self.stream.unget()

                    # if list_operations_flag:
                    #     return Operator(".", self.get_line_number(), start_column)

                    char=self.stream.next_char()
                    if char.isdigit():
                        try: 
                            self.stream.unget()
                            n=str(0)
                            n=n + c
                            while True:
                                c=self.stream.next_char()
                                if c.isdigit():
                                    n += c
                                elif c == ".":
                                    # raise TokenError(f"{n + c} Invalid number")
                                    raise TokenError(f"Token Error: In line {self.get_line_number()}\n{self.get_code()}\n{' ' * (self.get_column_number()-1)}^\n{n + c} Invalid number")
                                else:
                                    self.stream.unget()
                                    # return FloatLiteral(float(n)
                                    return FloatLiteral(float(n), self.get_line_number(), start_column)
                        except EndOfStream:
                            return FloatLiteral(float(n), self.get_line_number(), start_column)
                    else:
                        self.stream.unget()
                        return Operator(".", self.get_line_number(), start_column)

                # reading the numbers
                case c if c.isdigit():
                    start_column = self.get_column_number()
                    n=int(c)
                    while True:
                        try:
                            c=self.stream.next_char()
                            if c.isdigit():
                                n=n * 10 + int(c)
                            elif c == ".":

                                n=str(n)
                                n=n + c
                                while True:
                                    c=self.stream.next_char()
                                    if c.isdigit():
                                        n += c
                                    elif c == ".":
                                        # raise TokenError(f"{n + c} Invalid number")
                                        raise TokenError(f"Token Error: In line {self.get_line_number()}\n{self.get_code()}\n{' ' * (self.get_column_number()-1)}^\n{n + c} Invalid number")
                                    else:
                                        self.stream.unget()
                                        # return FloatLiteral(float(n))
                                        return FloatLiteral(float(n), self.get_line_number(), start_column)
                            else:
                                self.stream.unget()
                                # return NumLiteral(n)
                                return NumLiteral(n, self.get_line_number(), start_column)
                        except EndOfStream:
                            # return NumLiteral(n)
                            return NumLiteral(n, self.get_line_number(), start_column)

                # bracket and bracket matching
                case c if c in opening_brackets:
                    bracket_track_list.append(c)
                    # return Bracket(c)
                    return Bracket(c, self.get_line_number(), self.get_column_number())
                case c if c in closing_brackets:
                    temp=c
                    if len(bracket_track_list) == 0 or bracket_map[c] != bracket_track_list.pop():
                        # print(Bracket(c))
                        # raise TokenError(f"{c} Unmatched closing bracket")
                        raise TokenError(f"Token Error: In line {self.get_line_number()}\n{self.get_code()}\n{' ' * self.get_column_number()}^\n{c} Unmatched closing bracket")
                    # return Bracket(c)
                    return Bracket(c, self.get_line_number(), self.get_column_number())

                # reading the identifiers
                # _, a are valid identifiers


                case c if c.isalpha() or c == "_":
                    start_column = self.get_column_number()
                    s=c
                    while True:
                        try:
                            c=self.stream.next_char()
                            # a1, a_ is valid identifier
                            if c.isalpha() or c == "_" or c.isdigit():
                                s=s + c
                            else:
                                self.stream.unget()
                                return word_to_token(s, self.get_line_number(), start_column )
                        except EndOfStream: 
                            return word_to_token(s, self.get_line_number(), start_column )

                # reading the white space
                case c if c in whitespace:
                    return self.next_token()
        except EndOfStream:
            # you can put the end of the file
            return EndOfFile("EOF", self.get_line_number(), self.get_column_number())

    # see the current token without consuming it
    def peek_current_token(self) -> Token:
        """Return the current token without consuming it

        Returns:
            Token: current token
        """
        if self.save is not None:
            return self.save
        self.save=self.next_token()
        return self.save

    # consume the current token
    def advance(self):
        """Consume the current token"""
        assert self.save is not None
        self.save=None

    # match the current token against the expected token and consume it
    def match(self, expected):
        """Match the current token against the expected token and consume it if they match

        Args:
            expected (Token): expected token

        Raises:
            TokenError: if the current token is not the expected token

        Returns:
            None: if the current token is the expected token it will consume it and return None
        """

        pt = self.peek_current_token()
        if self.peek_current_token() == expected:
            return self.advance()

        # raise TokenError(
        #     f"Expected {expected} but got {self.peek_current_token()} ")
        expected.line_number=pt.line_number
        expected.column_number=pt.column_number
        raise TokenError(f"Token Error: In line {pt.line_number}\n{source_code[pt.line_number]}\n{' ' * (pt.column_number-1)}^\nExpected {expected} but got {self.peek_current_token()}")

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
        nxt_t=self.next_token()
        if isinstance(nxt_t, EndOfFile):
            if len(bracket_track_list) != 0:
                raise TokenError(
                    f"{' '.join(bracket_track_list)} : Unmatched opening bracket")
            raise StopIteration

        return nxt_t

if __name__ == "__main__":

    # testing on playground
    file=open("program.txt", "r")
    program=file.read()

    # print(Lexer.from_stream(Stream.from_string(program)))



    # # program = """4 .LEN;"""
    lexer_object=Lexer.from_stream(Stream.from_string(program))
    print(lexer_object)
    for token in lexer_object:
        print(token)
