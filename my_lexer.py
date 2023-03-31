from dataclasses import dataclass
from declaration import *


class EndOfStream(Exception):
    pass


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
        self.column_num = 1
        # self.code.append("")
    
    def unget_line(self):
        """Decrement the line number and reset the column number
        """
        self.line_num = self.line_num - 1
        self.column_num = 1
    
    def next_column(self):
        """Increment the column number
        """
        self.column_num = self.column_num + 1
    
    def unget_column(self):
        """Decrement the column number
        """
        self.column_num = self.column_num - 1
    
    # def add_to_code(self, c):
    #     """Add the character to the code list

    #     Args:
    #         c (str): character to be added
    #     """
    #     self.code[-1] += c
     
    
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
            self.column_num = 0
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


keywords = """
    int string float const assign slice
    if elif else break continue
    for while break continue
    def
    print let 
    slice in 
    """.split()
    
symbolic_operators = """
    + - * / % // ** ~
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


def word_to_token(word, line_num, column_num):
    """Convert a word to a tokens. Tokens are keywords, word operators, bool literals, identifiers"""
    if word in keywords:
        return Token(Keyword(word), line_num, column_num)
        return Keyword(word)
    if word in word_operators:
        return Token(Operator(word), line_num, column_num)
        return Operator(word)
    if word == "True":
        return Token(BoolLiteral(True), line_num, column_num)
        return BoolLiteral(True)
    if word == "False":
        return Token(BoolLiteral(False), line_num, column_num)
        return BoolLiteral(False)
    return Token(Identifier(word), line_num, column_num)
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
                    return Token(EndOfLine(c), self.stream.line_num, self.stream.column_num)
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
                    

                # reading the operators
                # special case !=
                case c if c == "!":
                    start_column = self.stream.column_num
                    s = self.stream.next_char()
                    if c + s in symbolic_operators:
                        return Token(Operator(c + s), self.stream.line_num, start_column)
                    print(f"In Line {self.stream.line_num}\n{self.stream.code[self.stream.line_num]}\n{' ' * (start_column - 1)}^\n{c + s} is an Invalid operator")
                    raise TokenError(f"In Line {self.stream.line_num}\n{self.stream.code[self.stream.line_num]}\n{' ' * (start_column - 1)}^\n{c + s} is an Invalid operator")

                case c if c in symbolic_operators:
                    start = self.stream.pos - 1
                    start_column = self.stream.column_num
                    while True:
                        s = self.stream.next_char()
                        # +- for unary operator ++--6
                        if s in symbolic_operators or s in "+-":
                            c = c + s
                        else:
                            self.stream.unget()
                            if c in symbolic_operators:
                                return Token(Operator(c), self.stream.line_num, start_column)
                            else:
                                for i in c:
                                    if i not in "+-":
                                        # =! is not a valid operator
                                        raise TokenError(f"In Line {self.stream.line_num}\n{self.stream.code[self.stream.line_num ]}\n{' ' * (start_column - 1)}^\n{c} is an Invalid operator")
                                        # raise TokenError(f"{c} is an Invalid operator")
                                # here getting unary operator
                                self.stream.pos = start + 1
                                # return Operator(c[0])
                                return Token(Operator(c[0]), self.stream.line_num, start_column)

                # reading the string literal, "" or ''
                case c if c == '"' or c == "'":
                    start_column = self.stream.column_num
                    current_quote = c
                    st = ''
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c == current_quote:
                                return Token(StringLiteral(st), self.stream.line_num, start_column)
                                # return StringLiteral(st)
                            else:
                                st = st + c
                        except EndOfStream:
                            raise TokenError(f'In Line {self.stream.line_num}\n{self.stream.code[self.stream.line_num]}\n{" " * (self.stream.column_num)}^\n{st}: Unterminated string literal')
                            # raise TokenError(f"{st}: Unterminated string literal")

                # handling .25
                case c if c == ".":
                    start_column = self.stream.column_num
                    n = str(0)
                    n = n + c
                    while True:
                        c = self.stream.next_char()
                        if c.isdigit():
                            n += c
                        elif c == ".":
                            raise TokenError(f"In line {self.stream.line_num}\n{self.stream.code[self.stream.line_num]}\n{' ' * (self.stream.column_num - 1)}^\n{n + c} Invalid number")
                            # raise TokenError(f"{n + c} Invalid number")
                        else:
                            self.stream.unget()
                            return Token(FloatLiteral(float(n)), self.stream.line_num, start_column)
                            # return FloatLiteral(float(n))
                    pass

                # reading the numbers
                case c if c.isdigit():
                    start_column = self.stream.column_num
                    n = int(c)
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c.isdigit():
                                n = n * 10 + int(c)
                            elif c == ".":
                                n = str(n)
                                n = n + c
                                while True:
                                    c = self.stream.next_char()
                                    if c.isdigit():
                                        n += c
                                    elif c == ".":
                                        raise TokenError(f"In line {self.stream.line_num}\n{self.stream.code[self.stream.line_num]}\n{' ' * (self.stream.column_num - 1)}^\n{n + c} Invalid number")
                                        raise TokenError(
                                            f"{n + c} Invalid number")
                                    else:
                                        self.stream.unget()
                                        return Token(FloatLiteral(float(n)), self.stream.line_num, start_column)
                                        return FloatLiteral(float(n))
                            else:
                                self.stream.unget()
                                return Token(NumLiteral(n), self.stream.line_num, start_column)
                                return NumLiteral(n)
                        except EndOfStream:
                            return Token(NumLiteral(n), self.stream.line_num, start_column)
                            return NumLiteral(n)

                # bracket and bracket matching
                case c if c in opening_brackets:
                    bracket_track_list.append(c)
                    return Token(Bracket(c), self.stream.line_num, self.stream.column_num)
                    return Bracket(c)
                case c if c in closing_brackets:
                    if len(bracket_track_list) == 0 or bracket_map[c] != bracket_track_list.pop():
                        print(Bracket(c))
                        raise TokenError(f"In Line {self.stream.line_num}\n{self.stream.code[self.stream.line_num]}\n{' ' * (self.stream.column_num - 1)}^\n{c} Unmatched closing bracket")
                        raise TokenError(f"{c} Unmatched closing bracket")
                    return Bracket(c)

                # reading the identifiers
                # _, a are valid identifiers        
                case c if c.isalpha() or c == "_":
                    start_column = self.stream.column_num
                    s = c
                    while True:
                        try:
                            c = self.stream.next_char()
                            # a1, a_ is valid identifier
                            if c.isalpha() or c == "_" or c.isdigit():
                                s = s + c
                            else:
                                self.stream.unget()
                                return word_to_token(s, self.stream.line_num, start_column)
                        except EndOfStream:
                            return word_to_token(s, self.stream.line_num, start_column)

                # reading the white space
                case c if c in whitespace:
                    return self.next_token()
        except EndOfStream:
            # you can put the end of the file
            return Token(EndOfFile("EOF"), self.stream.line_num, self.stream.column_num)
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
            None: if the current token is the expected token it will consume it and return None
        """

        if self.peek_current_token() == expected:
            return self.advance()

        raise TokenError(f"Expected {expected} but got {self.peek_current_token()} ")

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
        if isinstance(nxt_t, Token) and isinstance(nxt_t.token, EndOfFile):
            if len(bracket_track_list) != 0:
                raise TokenError(
                    f"{' '.join(bracket_track_list)} : Unmatched opening bracket")
            raise StopIteration

        return nxt_t

if __name__ == "__main__":
    
    # testing on playground
    file = open("program.txt", "r")
    program = file.read()
    lexer_object = Lexer.from_stream(Stream.from_string(program))
    print(lexer_object)
    for token in lexer_object:
        print(token)