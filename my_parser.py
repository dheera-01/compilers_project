from my_lexer import *
from dataclasses import dataclass
# from fractions import Fraction
from sim import *
import sys


class EndOfLineErrror(Exception):
    pass


@dataclass
class Parser:
    lexer: Lexer

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
    
    def parse_while(self):
        """parse while statement

        Returns:
            While AST: return AST of while statement
        """
        self.lexer.match(Keyword("while"))
        # Parse the condition
        c_ast = self.parse_expr()
        body_ast = self.parse_expr()
        return While(c_ast, body_ast)
    
    def parse_for(self):
        """parse for statement

        Returns:
            For AST: return AST of for statement
        """
        self.lexer.match(Keyword("for"))
    
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
            left = BinOp( temp.pop(), "**",left)
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
                    left = BinOp( left, op,m)

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
                    left = BinOp(left,op,  m)

                case _:
                    break

        return left

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

                return ComparisonOp(left,op,  right)

        return left

    def parse_simple(self):
        """parse the simple expression (witoout if else, while)

        Returns:
            AST: return AST of the simple expression 
        """

        return self.parse_cmp()

    def parse_assignment(self):
        """parse the assignment expression
        """

        pass
    
    def parse_assign(self):
        """
        parse the assign expression
        """
        self.lexer.advance()
        left_part = self.parse_atom()
        self.lexer.match(Operator("="))
        right_part = self.parse_expr()
        return Assign(left_part, right_part)
    
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
                return self.parse_expr()
            case c if isinstance(c, EndOfFile):
                print("End of file")
                # exit the program successfully
                sys.exit(0)
            case c if isinstance(c, Identifier):
                return self.parse_assignment()
            case Keyword("if"):
                return self.parse_if()
            case Keyword("while"):
                return self.parse_while()
            case Keyword("for"):
                return self.parse_for()
            case Keyword("assign"):
                return self.parse_assign()
            case Keyword("print"):
                return self.parse_print()
            case _:
                return self.parse_simple()


        # t = next(self.lexer)
        # print(t)
        # if isinstance(t, Num):
        #     return t.n
        # else:
        #     raise Exception("Expected number")
if __name__ == '__main__':

    file = open("programParse.txt", "r")
    program = file.read()
    obj_parser = Parser.from_lexer(
        Lexer.from_stream(Stream.from_string(program)))

    while True:
        print(eval(obj_parser.parse_expr()))
    # print(obj_parser.lexer.peek_current_token())
    # print(eval(obj_parser.parse_expr()))
    # print(eval(obj_parser.parse_expr()))

    # print(eval(Parser.from_lexer(Lexer.from_stream(Stream.from_string(a))).parse_expr()))
