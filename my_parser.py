from my_lexer import *
from dataclasses import dataclass
# from fractions import Fraction
from sim import eval, AST, InvalidProgram, BinOp, ComparisonOp, IfElse, Let, Value


class EndOfLineErrror(Exception):
    pass

@dataclass
class Parser:
    lexer: Lexer

    def from_lexer(lexer):
        return Parser(lexer)

    def parse_if(self):
        t = StringLiteral("Chirag")
        self.lexer.match(Keyword("if"))
        c = self.parse_expr() # parse the condition
        if_branch = self.parse_expr()
        self.lexer.match(Keyword("else"))
        else_branch = self.parse_expr()
        print(c, if_branch, else_branch)
        return IfElse(c, if_branch, else_branch)

    # def parse_while(self):
    #     self.lexer.match(Keyword("while"))
    #     c = self.parse_expr()
    #     self.lexer.match(Keyword("do"))
    #     b = self.parse_expr()
    #     self.lexer.match(Keyword("done"))
    #     return While(c, b)


    def parse_atom(self):
        print("parse_atom")
        match self.lexer.peek_current_token():
            case Identifier(name):
                self.lexer.advance()
                return Identifier(name)
            case NumLiteral(value):
                self.lexer.advance()
                print("parse_atom", value)
                return NumLiteral(value)
            case FloatLiteral(value):
                self.lexer.advance()
                return FloatLiteral(value)
            case BoolLiteral(value):
                self.lexer.advance()
                return BoolLiteral(value)
            case Bracket("(") | Bracket("[") | Bracket("{"):
                print(self.lexer.peek_current_token())
                self.lexer.advance() # consume the opening bracket
                ans = self.parse_expr() # calculating the expression inside the brackets
                self.lexer.advance() # consume the closing bracket
                print(ans)
                return ans
                
            
    def parse_mult(self):
        print("parse_mult")
        left = self.parse_atom()
        try: 
            while True:
                match self.lexer.peek_current_token():
                    case Operator(op) if op in "* / // %".split():
                        self.lexer.advance()
                        m = self.parse_atom()
                        left = BinOp(op, left, m)
                        # print("parse_mult", left)
                    case _:
                        # print("break")
                        break
        except:
            raise EndOfLineErrror(f"; expected")
            pass
        return left

    def parse_add(self):
        print("parse_add")
        left = self.parse_mult()
        try: 
            while True:
                match self.lexer.peek_current_token():
                    case Operator(op) if op in "+-":
                        self.lexer.advance()
                        # print("before parse_add")
                        m = self.parse_mult()
                        # print("after parse_add",m)
                        left = BinOp(op, left, m)
                    case _:
                        break
        except:
            raise EndOfLineErrror(f"; expected ")
            # raise EndOfLineErrror()
            pass
        return left

    def parse_cmp(self):
        print("parse_cmp")
        left = self.parse_add()
        try:
            match self.lexer.peek_current_token():
                case Operator(op) if op in "< > >= <= == !=".split():
                    self.lexer.advance()
                    right = self.parse_add()
                    return ComparisonOp(op, left, right)
        except: 
            raise EndOfLineErrror(f"; expected ")
            # raise EndOfLineErrror()
            pass
        return left

    def parse_simple(self):
        return self.parse_cmp()

    def parse_expr(self):
        match self.lexer.peek_current_token():
            case Keyword("if"):
                print("if")
                return self.parse_if()
            case Keyword("while"):
                # print("while")
                return self.parse_while()
            case _:
                print("parse_simple")
                return self.parse_simple()


        # t = next(self.lexer)
        # print(t)
        # if isinstance(t, Num):
        #     return t.n
        # else:
        #     raise Exception("Expected number")
if __name__ == '__main__':
    # p = Parser()
    a = "2 + 3 * 5 ;"
    b = "1 + (9 -(8 - 9)) * 3;"
    b = "{1 + 9 + 3} (1 + 3);"
    b = "if 10>5 { if 1 > 9  1+{5+6 * 2} * 3  else {6} } else { 0 }"
    ins = Instrution()
    ins.form_instrutctions_of(b)
    ins.print_instrutions()
    # for i in ins.instruction_lists:
    # print(eval(Parser.from_lexer(Lexer.from_stream(Stream.from_string(a))).parse_expr()))
    print(eval(Parser.from_lexer(Lexer.from_stream(Stream.from_string(b))).parse_expr()))

        # if 3 > 2 then 1 else 0 end
 