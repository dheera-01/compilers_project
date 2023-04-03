from my_lexer import *
from dataclasses import dataclass
import sys
from declaration import *
from eval_for_parser import *


@dataclass
class Parser:
    lexer: Lexer
    mySequence = Sequence([])

    def __init__(self, _lexer):
        self.lexer = _lexer
        self.mySequence = Sequence([])

    def from_lexer(_lexer):
        """give a tokens (lexer output ) to the parser

        Args:
            Lexer: lexer output

        Returns:
            Parser: parser object
        """
        return Parser(_lexer)

    def parse_if(self):
        """parse if else statement

        Returns:
            IfElse: return AST of if else statement
        """
        self.lexer.match(Keyword("if"))
        c = self.parse_simple()  # parse the condition which is a simple expression
        if_branch = self.parse_block()
        

        # single if statement
        if self.lexer.peek_current_token().token != Keyword("else") and self.lexer.peek_current_token().token != Keyword("elif"):
            return IfElse(c, if_branch, [], None)

        elif_list = []
        while self.lexer.peek_current_token().token == Keyword("elif"):
            self.lexer.advance()
            elif_condition = self.parse_simple()
            elif_body = self.parse_block()
            elif_list.append(IfElse(elif_condition, elif_body, [], None))

        # if and elif are allowed without else
        if self.lexer.peek_current_token().token != Keyword("else"):
            return IfElse(c, if_branch, elif_list, None)

        self.lexer.match(Keyword("else"))
        else_branch = self.parse_block()
        return IfElse(c, if_branch, elif_list, else_branch)

    def parse_while(self):
        """parse while statement

        Returns:
            while AST: return AST of while loop
        """
        self.lexer.match(Keyword("while"))
        # print(self.lexer.peek_current_token())
        cond = self.parse_simple()  # parse the condition
        # print("cond", cond)
        while_body = self.parse_block()
        return While(cond, while_body)

    def parse_for(self):
        """parse for statement

        Returns:
            For: return AST of for loop
        """
        self.lexer.match(Keyword("for"))
        self.lexer.match(Bracket("("))
        initial = self.parse_expr()
        cond = self.parse_simple()
        self.lexer.match(EndOfLine(";"))
        termination = self.parse_expr()
        self.lexer.match(Bracket(")"))
        for_body = self.parse_block()
        # print(self.lexer.peek_current_token())
        return For(initial, cond, termination, for_body)

    def parse_atom(self):
        """parse the atomic expression"""
        match self.lexer.peek_current_token().token:
            case Identifier(name):
                ct = self.lexer.peek_current_token()
                self.lexer.advance()
                match self.lexer.peek_current_token().token:
                    case Bracket("["):
                        self.lexer.advance()
                        right_part = self.parse_atom()
                        self.lexer.match(Bracket("]"))
                        return Indexer(ct, right_part)
                    case _:
                        # self.lexer.advance()
                        return ct

            case Bracket("(") | Bracket("[") | Bracket("{"):
                self.lexer.advance()  # consume the opening bracket
                ans = self.parse_simple()  # calculating the expression inside the brackets
                self.lexer.advance()  # consume the closing bracket
                return ans

            # case _ :
            #     ct = self.lexer.peek_current_token()
            #     self.lexer.advance()
            #     return ct
            case StringLiteral(value):
                ct = self.lexer.peek_current_token()
                self.lexer.advance()
                return ct
                return StringLiteral(value)
            case NumLiteral(value):
                ct = self.lexer.peek_current_token()
                # print(self.lexer.peek_current_token())
                self.lexer.advance()
                # print(self.lexer.peek_current_token())
                return Token(NumLiteral(value), ct.line, ct.column)
            case FloatLiteral(value):
                ct = self.lexer.peek_current_token()
                self.lexer.advance()
                return Token(FloatLiteral(value), ct.line, ct.column)
            case BoolLiteral(value):
                ct = self.lexer.peek_current_token()
                self.lexer.advance()
                return Token(BoolLiteral(value), ct.line, ct.column)
            case Keyword("slice"):
                ct = self.lexer.peek_current_token()
                return self.parse_slice()
            case Keyword("let"):
                ct = self.lexer.peek_current_token()
                return self.parse_let()

    def parse_exponent(self):
        """parse the exponent operator, this is right associative

        Returns:
            AST: return AST of the exponent operation
        """

        temp = []
        left = self.parse_atom()
        temp.append(left)
        while True:
            # print(f"exponent current token {self.lexer.peek_current_token()}")
            match self.lexer.peek_current_token().token:
                case Operator(op) if op == "**":
                    ct = self.lexer.peek_current_token()
                    temp.append(ct)
                    self.lexer.advance()
                    m = self.parse_atom()
                    temp.append(m)
                case _:
                    break

        # making the exponent right associative
        left = temp.pop()
        while len(temp) > 0:
            op1 = temp.pop()
            exponent_op: Token = temp.pop()
            if exponent_op.token == "**":
                left = BinOp(op1, exponent_op, left)
                # raise Exception(f"In line {exponent_op.line}\n{self.lexer.stream.code[exponent_op.line]}\n{' '*(exponent_op.column-1)}^\nExpected **")
        return left

    def parse_unary(self):
        """parse the unary operator, this is left associative

        Returns:
            AST: return AST of the unary operation
        """

        # unary operator is left associative
        left = self.parse_exponent()
        if left == None:
            while True:
                # print(f"current token {self.lexer.peek_current_token()}")
                match self.lexer.peek_current_token().token:
                    case Operator(op) if op in "-+":
                        ct = self.lexer.peek_current_token()
                        self.lexer.advance()
                        exp = self.parse_exponent()
                        if (exp != None):
                            return UnaryOp(ct, exp)
                        else:
                            return UnaryOp(ct, self.parse_unary())
                    case _:
                        break
        return left

    def parse_mult(self):
        """parse the *, /, //, % operator

        Returns:
            AST: return AST of the *, /, //, % operation
        """

        left = self.parse_unary()

        while True:
            match self.lexer.peek_current_token().token:
                case Operator(op) if op in "* / // %".split():
                    ct = self.lexer.peek_current_token()  # current Token
                    self.lexer.advance()
                    m = self.parse_unary()
                    left = BinOp(left, ct, m)

                case _:
                    break

        return left

    def parse_add(self):
        """parse the addition and subtraction operator

        Returns:
            AST: return AST of the addition and subtraction operation
        """
        left = self.parse_mult()

        while True:
            match self.lexer.peek_current_token().token:

                case Operator(op) if op in "+-~":
                    ct = self.lexer.peek_current_token()
                    self.lexer.advance()
                    # print("before parse_add")
                    m = self.parse_mult()
                    # print("after parse_add",m)
                    left = BinOp(left, ct, m)

                case _:
                    break

        return left

    def parse_slice(self):
        """parse the slice operation

        Returns:
            AST: return AST of the slice operation
        """
        self.lexer.match(Keyword("slice"))
        self.lexer.match(Bracket("("))
        string_literal = self.parse_simple()
        self.lexer.match(Operator(":"))
        start = self.parse_simple()
        self.lexer.match(Operator(":"))
        end = self.parse_simple()
        self.lexer.match(Operator(":"))
        step = self.parse_simple()
        self.lexer.match(Bracket(")"))
        return Slice(string_literal, start, end, step)

    def parse_cmp(self):
        """parse the comparison operator

        Returns:
            AST: return AST of the comparison operator
        """

        left = self.parse_add()
        match self.lexer.peek_current_token().token:
            case Operator(op) if op in "< > >= <= == !=".split():
                current_token = self.lexer.peek_current_token()
                self.lexer.advance()
                right = self.parse_add()
                return ComparisonOp(left, current_token, right)

        return left

    def parse_and(self):
        """parse the and Operator

        Returns:
            AST: return the AST of the and operator
        """

        left = self.parse_cmp()
        while True:
            match self.lexer.peek_current_token().token:
                case Operator(op) if op == "and":
                    current_token = self.lexer.peek_current_token()
                    self.lexer.advance()
                    right = self.parse_cmp()
                    left = ComparisonOp(left, current_token, right)
                case _:
                    break
        return left
        pass

    def parse_or(self):
        """parse the or operator

        Returns:
            AST: return AST of the or operator
        """

        left = self.parse_and()
        while True:
            match self.lexer.peek_current_token():
                case c if isinstance(c.token, Operator) and c.token._operator == "or":
                    self.lexer.advance()
                    right = self.parse_and()
                    left = ComparisonOp(left, c, right)
                case _:
                    break
        return left

        pass

    def parse_simple(self):
        """parse the simple expression (without if else, while, for, assign, const and update, or something returning none) 

        Returns:
            AST: return AST of the simple expression
        """

        return self.parse_or()

    def parse_assign(self):
        self.lexer.match(Keyword("assign"))
        assignments_l = []
        assignments_r = []
        while True:
            # self.lexer.advance()
            left_part = self.parse_atom()
            assignments_l.append(left_part)
            self.lexer.match(Operator("="))

            # 2 cases: 1. assign to a variable 2. assign to a list
            match self.lexer.peek_current_token().token:
                case Bracket("["):
                    # Till you dont encounter a closing bracket, keep parsing the expression and store the literals
                    # in a list and skip the operator ","
                    self.lexer.advance()
                    right_part = []
                    while True:
                        match self.lexer.peek_current_token().token:
                            case Bracket("]"):
                                self.lexer.advance()
                                break
                            case Operator(","):
                                self.lexer.advance()
                            case _:
                                right_part.append(self.parse_simple())
                    assignments_r.append(right_part)
                case _:
                    right_part = self.parse_simple()
                    assignments_r.append(right_part)

            match self.lexer.peek_current_token().token:
                case Operator(op) if op in ",":
                    self.lexer.match(Operator(","))
                    continue
                case _:
                    break

        self.lexer.match(EndOfLine(";"))
        return Assign(tuple(assignments_l), tuple(assignments_r))

    def parse_const(self):
        """paster the immutable assign expression

        Returns:
            Assign: return AST of the immutable assign expression
        """
        self.lexer.match(Keyword("const"))
        self.lexer.match(Keyword("assign"))
        assignments_l = []
        assignments_r = []
        while True:
            # self.lexer.advance()
            left_part = self.parse_atom()
            left_part.is_mutable = False
            assignments_l.append(left_part)
            self.lexer.match(Operator("="))

            # 2 cases: 1. assign to a variable 2. assign to a list
            match self.lexer.peek_current_token().token:
                case Bracket("["):
                    # Till you dont encounter a closing bracket, keep parsing the expression and store the literals
                    # in a list and skip the operator ","
                    self.lexer.advance()
                    right_part = []
                    while True:
                        match self.lexer.peek_current_token().token:
                            case Bracket("]"):
                                self.lexer.advance()
                                break
                            case Operator(","):
                                self.lexer.advance()
                            case _:
                                right_part.append(self.parse_simple())
                    assignments_r.append(right_part)
                case _:
                    right_part = self.parse_simple()
                    assignments_r.append(right_part)

            match self.lexer.peek_current_token().token:
                case Operator(op) if op in ",":
                    self.lexer.match(Operator(","))
                    continue
                case _:
                    break

        self.lexer.match(EndOfLine(";"))
        return Assign(tuple(assignments_l), tuple(assignments_r))

    def parse_update(self):
        """parse the update expression

        Returns:
            Update: return AST of the update expression
        """
        left_part = self.parse_atom()

        assignment_operator_list = "= -= += *= /= %= //= **=".split()
        ct = self.lexer.peek_current_token()
        op = self.lexer.peek_current_token().token
        if not isinstance(ct.token, Operator):
            raise InvalidProgram(
                f"In line {ct.line}\n{self.lexer.stream.code[ct.line]}\n{' '*(ct.column-1)}^\nSyntax Error: Expected an assignment operator but got {ct.token}")
            # raise InvalidProgram(f"Syntax Error: Expected an assignment operator but got {op}")
        if ct.token._operator not in assignment_operator_list:
            raise InvalidProgram(
                f"In line {ct.line}\n{self.lexer.stream.code[ct.line]}\n{' '*(ct.column-1)}^\nSyntax Error: {ct.token} not a valid assignment operator")
            # raise InvalidProgram(f"Syntax Error: {op} not a valid assignment operator")
        self.lexer.advance()  # consuming the assignment operator

        match self.lexer.peek_current_token().token:
            case Bracket("["):
                # Till you dont encounter a closing bracket, keep parsing the expression and store the literals
                # in a list and skip the operator ","
                self.lexer.advance()
                right_part = []
                while True:
                    match self.lexer.peek_current_token().token:
                        case Bracket("]"):
                            self.lexer.advance()
                            break
                        case Operator(","):
                            self.lexer.advance()
                        case _:
                            right_part.append(self.parse_simple())
                self.lexer.match(EndOfLine(";"))
                return Update(left_part, op, right_part)
            case _:
                right_part = self.parse_simple()
                self.lexer.match(EndOfLine(";"))
                return Update(left_part, op, right_part)

    def parse_print(self):
        """parse the print expression

        Returns:
            Print: return AST of the print expression
        """
        # print("Parsing print")
        self.lexer.match(Keyword("print"))
        self.lexer.match(Bracket("("))
        print_statement = self.parse_simple()
        self.lexer.match(Bracket(")"))
        self.lexer.match(EndOfLine(';'))
        return Print(print_statement)

    def parse_let(self):
        """parse the let expression
        Returns:
            returns the value of expression after in keyword
        """

        self.lexer.match(Keyword("let"))
        left_part = self.parse_atom()
        self.lexer.match(Operator("="))
        right_part = self.parse_simple()
        self.lexer.match(Bracket("("))
        body = self.parse_simple()
        self.lexer.match(Bracket(")"))
        return Let(left_part, right_part, body)

    def parse_expr(self):
        """parse the expression

        Returns:
            AST: return AST of the expression
        """
        # current_token = self.lexer.peek_current_token()
        # print(f"parser_expr: {current_token}")
        match self.lexer.peek_current_token():
            case c if isinstance(c.token, EndOfLine):
                self.lexer.advance()
                return Token(EndOfLine(";"), c.line, c.column)
            case c if isinstance(c.token, EndOfFile):
                return Token(EndOfFile("EOF"), c.line, c.column)
                return EndOfFile("EOF")
                sys.exit(0)
            case c if c.token == Keyword("elif"):
                # case Keyword("elif"):
                raise InvalidProgram(
                    f"In Line {c.line}\n{self.lexer.stream.code[c.line]}\n{' ' * c.column - 1}^\nSyntax Error: elif can only be used after if")
                raise InvalidProgram(
                    f"Syntax Error: elif can only be used after if")
            case c if c.token == Keyword("if"):
                return self.parse_if()
            case c if c.token == Keyword("while"):
                return self.parse_while()
            case c if c.token == Keyword("for"):
                return self.parse_for()
            case c if c.token == Keyword("assign"):
                return self.parse_assign()
            case c if c.token == Keyword("const"):
                return self.parse_const()
            # update statements
            case c if isinstance(c.token, Identifier):
                return self.parse_update()
            case c if c.token == Keyword("print"):
                return self.parse_print()
            case _:
                return self.parse_simple()

    # statements with {} is considered blocks
    def parse_block(self) -> Sequence:
        """parse the block. block starts with Brackets('{')

        Returns:
            Sequence: return AST of the block
        """
        self.lexer.match(Bracket("{"))
        block_sequence = Sequence([])
        while True:
            t = self.parse_expr()
            # } will not be parsed as it is not a valid expression
            if t == None and self.lexer.peek_current_token().token == Bracket("}"):
                break
            block_sequence.statements.append(t)
        self.lexer.match(Bracket("}"))
        return block_sequence

    def parse_program(self) -> Sequence:
        """parse the program

        Returns:
            Sequence: return AST of the program
        """
        # print(f"parse program function: {self}")
        while True:
            t = self.parse_expr()
            # print(f"Parse_program: {t}")
            if isinstance(t, Token) and t.token == EndOfFile("EOF"):
                break
            self.mySequence.statements.append(t)
        return self.mySequence

    def __repr__(self) -> str:
        return f"Parser:\nLexer: {self.lexer}\nSequence: {self.mySequence}"


# def parse_code_file(file_location:str):
#     '''
#     to parse and evaluate given file present file_Location
#     '''

#     file = open(file_location, "r")

#     program = file.read()
#     obj_parser = Parser.from_lexer(
#         Lexer.from_stream(Stream.from_string(program)))

#     a = obj_parser.parse_program()
#     print(a)
#     program_env = Environment()
#     print(program_env)
#     ans = eval(a, program_env)

if __name__ == '__main__':

    file = open("program.txt", "r")

    program = file.read()
    object_lexer = Lexer.from_stream(Stream.from_string(program))
    for i in object_lexer:
        print(i)

    obj_parser = Parser.from_lexer(
        Lexer.from_stream(Stream.from_string(program)))
    print(f"object parser {obj_parser}")
    a = obj_parser.parse_program()
    # eval(a)
    print(f"Parsed program: {a}")
