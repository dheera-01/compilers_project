from lexer import *
from dataclasses import dataclass
# from fractions import Fraction
from eval_for_parser import *
import sys
from declaration import *


class EndOfLineErrror(Exception):
    pass


@dataclass
class Parser:
    lexer: Lexer
    mySequence = Sequence([])

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
            IfElse AST: return AST of if else statement
        """
        self.lexer.match(Keyword("if"))

        c = self.parse_expr()  # parse the condition

        if_branch = self.parse_expr()
        self.lexer.match(Keyword("else"))
        else_branch = self.parse_expr()

        return IfElse(c, if_branch, else_branch)

    # def parse_while(self):
    #     """parse while statement

    #     Returns:
    #         While AST: return AST of while statement
    #     """
    #     self.lexer.match(Keyword("while"))
    #     # Parse the condition
    #     c_ast = self.parse_expr()
    #     body_ast = self.parse_expr()
    #     return While(c_ast, body_ast)

    def parse_while(self):
        """parse while statement

        Returns:
            while AST: return AST of while loop
        """
        self.lexer.match(Keyword("while"))
        # print(self.lexer.peek_current_token())
        cond = self.parse_expr()  # parse the condition
        # print("cond", cond)
        while_body = self.parse_block()
        return While(cond, while_body)

    def parse_for(self):
        """parse for statement

        Returns:
            for AST: return AST of for loop
        """
        self.lexer.match(Keyword("for"))
        self.lexer.match(Bracket("("))
        initial = self.parse_assign()
        self.lexer.match(EndOfLine(";"))
        cond = self.parse_expr()
        self.lexer.match(EndOfLine(";"))
        termination = self.parse_expr()
        self.lexer.match(Bracket(")"))
        for_body = self.parse_block()
        # print(self.lexer.peek_current_token())
        return For(initial, cond, termination, for_body)

    def parse_atom(self):
        """parse the atomic expression"""
        match self.lexer.peek_current_token():

            case Identifier(name):
                self.lexer.advance()

                return Identifier(name)
            case StringLiteral(value):
                self.lexer.advance()
                return StringLiteral(value)
            case NumLiteral(value):
                self.lexer.advance()
                return NumLiteral(value)
            case FloatLiteral(value):
                self.lexer.advance()
                return FloatLiteral(value)
            case BoolLiteral(value):
                self.lexer.advance()
                return BoolLiteral(value)
            case Bracket("(") | Bracket("[") | Bracket("{"):
                self.lexer.advance()  # consume the opening bracket
                ans = self.parse_expr()  # calculating the expression inside the brackets
                self.lexer.advance()  # consume the closing bracket
                return ans

    def parse_exponent(self):
        """parse the exponent operator, this is right associative

        Returns:
            AST: return AST of the exponent operation
        """

        temp = []
        left = self.parse_atom()
        temp.append(left)
        while True:
            match self.lexer.peek_current_token():
                case Operator(op) if op == "**":
                    self.lexer.advance()
                    m = self.parse_atom()
                    temp.append(m)
                case _:
                    break

        # making the exponent right associative
        left = temp.pop()
        while len(temp) > 0:
            left = BinOp(temp.pop(), "**", left)
        return left

    def parse_uniary(self):
        """parse the uniary operator, this is left associative

        Returns:
            AST: return AST of the uniory operation
        """

        # uniary operator is left associative
        left = self.parse_exponent()
        if left == None:
            while True:
                match self.lexer.peek_current_token():
                    case Operator(op) if op in "-+":
                        self.lexer.advance()
                        left = UnaryOp(op, self.parse_exponent())
                    case _:
                        break
        return left

    def parse_mult(self):
        """parse the *, /, //, % operator

        Raises:
            EndOfLineErrror: _description_

        Returns:
            AST: return AST of the *, /, //, % operation
        """

        left = self.parse_uniary()

        while True:
            match self.lexer.peek_current_token():

                case Operator(op) if op in "* / // %".split():
                    self.lexer.advance()
                    m = self.parse_uniary()
                    left = BinOp(left, op, m)

                case _:
                    break

        return left

    def parse_add(self):
        """parse the addition and subtraction operatior

        Raises:
            EndOfLineErrror: _description_

        Returns:
            AST: return AST of the addition and subtraction operation
        """
        left = self.parse_mult()

        while True:
            match self.lexer.peek_current_token():

                case Operator(op) if op in "+-":
                    self.lexer.advance()
                    # print("before parse_add")
                    m = self.parse_mult()
                    # print("after parse_add",m)
                    left = BinOp(left, op, m)

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
        string_literal = self.parse_expr()
        self.lexer.match(Operator(":"))
        start = self.parse_expr()
        self.lexer.match(Operator(":"))
        end = self.parse_expr()
        self.lexer.match(Operator(":"))
        step = self.parse_expr()
        self.lexer.match(Bracket(")"))
        return Slice(string_literal, start, end, step)

    def parse_cmp(self):
        """parse the comparison operator

        Raises:
            EndOfLineErrror: _description_

        Returns:
            AST: return AST of the comparison operator
        """

        left = self.parse_add()
        match self.lexer.peek_current_token():

            case Operator(op) if op in "< > >= <= == !=".split():
                self.lexer.advance()
                right = self.parse_add()

                return ComparisonOp(left, op, right)

        return left

    def parse_simple(self):
        """parse the simple expression (witoout if else, while)

        Returns:
            AST: return AST of the simple expression
        """

        return self.parse_cmp()

    def parse_assign(self):
        """
        parse the assign expression
        """
        self.lexer.advance()
        left_part = self.parse_atom()
        self.lexer.match(Operator("="))
        right_part = self.parse_expr()
        return Assign(left_part, right_part)

    def parse_const(self):
        self.lexer.advance()
        self.lexer.match(Keyword("assign"))
        identifier = self.parse_atom()
        identifier.is_mutable = False
        self.lexer.match(Operator("="))
        right_part = self.parse_expr()
        return Assign(identifier, right_part)

    def parse_print(self):
        """parse the print expression

        Returns:
            Print AST: return AST of the print expression
        """
        self.lexer.match(Keyword("print"))
        return Print(self.parse_expr())

    def parse_expr(self):
        """parse the expression

        Returns:
            AST: return AST of the expression
        """
        match self.lexer.peek_current_token():

            case c if isinstance(c, EndOfLine):
                self.lexer.advance()
                return EndOfLine(";")
            case c if isinstance(c, EndOfFile):
                # print("End of file")
                # print("Sequence\n",self.mySequence)
                # exit the program successfully
                # return Sequence(self.self.mySequence)
                return EndOfFile("EOF")
                sys.exit(0)
            case Keyword("if"):
                print(self.lexer.peek_current_token())
                return self.parse_if()
            case Keyword("while"):
                return self.parse_while()
            case Keyword("for"):
                return self.parse_for()
            case Keyword("assign"):
                return self.parse_assign()
            case Keyword("print"):
                return self.parse_print()
            case Keyword("slice"):
                return self.parse_slice()
            case Keyword("const"):
                return self.parse_const()
            case _:
                return self.parse_simple()

    # statements with {} is considered blocks
    def parse_block(self) -> Sequence:
        """parse the block

        Returns:
            AST: return AST of the block
        """
        self.lexer.match(Bracket("{"))
        block_sequence = Sequence([])
        block_sequence.statements.append(EndOfLine(";"))
        while True:
            # print("peek token", self.lexer.peek_current_token())
            if self.lexer.peek_current_token() == Bracket("}"):
                if (block_sequence.statements[-1] != EndOfLine(";")):
                    # print("error")
                    raise InvalidProgram(f"Syntax Error: Expecter {EndOfLine(';')} but found {Bracket('}')}")
                block_sequence.statements.pop()
                break
            t = self.parse_expr()
            # print("t",t)
            if t == EndOfLine(";"):
                if (block_sequence.statements[-1] == EndOfLine(";")):
                    raise InvalidProgram(f"Syntax Error: Expecter AST but found {EndOfLine(';')}")
                block_sequence.statements.append(t)
            else:
                if (block_sequence.statements[-1] != EndOfLine(";")):
                    raise InvalidProgram(f"Syntax Error: Expecter {EndOfLine(';')} but found {t}")
                block_sequence.statements.pop()
                block_sequence.statements.append(t)
        self.lexer.match(Bracket("}"))
        # print("block_sequence",block_sequence)
        return block_sequence

    def parse_program(self) -> Sequence:
        """parse the program

        Returns:
            AST: return AST of the program
        """
        self.mySequence.statements.append(EndOfLine(";"))
        while True:
            t = self.parse_expr()
            if (t == EndOfFile("EOF")):
                if (self.mySequence.statements[-1] != EndOfLine(";")):
                    raise InvalidProgram(f"Syntax Error: Expecter {EndOfLine(';')} but found {t}")
                self.mySequence.statements.pop()
                break
            if t == EndOfLine(";"):
                if (self.mySequence.statements[-1] == EndOfLine(";")):
                    raise InvalidProgram(f"Syntax Error: Expecter AST but found {EndOfLine(';')}")
                self.mySequence.statements.append(t)
            else:
                if (self.mySequence.statements[-1] != EndOfLine(";")):
                    raise InvalidProgram(f"Syntax Error: Expecter {EndOfLine(';')} but found {t}")
                self.mySequence.statements.pop()
                self.mySequence.statements.append(t)
        return self.mySequence


if __name__ == '__main__':

    file = open("tests_parser/const.txt", "r")

    program = file.read()
    obj_parser = Parser.from_lexer(
        Lexer.from_stream(Stream.from_string(program)))

    a = obj_parser.parse_program()
    print(a)
    program_env = Enviroment()
    print(program_env)
    ans = eval(a, program_env)
    for i in ans:
        print(i)