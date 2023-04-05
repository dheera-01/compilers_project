from typing import List
from dataclasses import dataclass
from declaration import AST
from my_parser import *
class I:    
Instruction = (
      I.PUSH
    | I.ADD
    | I.SUB
    | I.MUL
    | I.DIV
    | I.QUOT
    | I.REM
    | I.NOT
    | I.UMINUS
    | I.UPLUS
    | I.JMP
    | I.JMP_IF_FALSE
    | I.JMP_IF_TRUE
    | I.DUP
    | I.POP
    | I.HALT
    | I.EQ
    | I.NEQ
    | I.LT
    | I.GT
    | I.LE
    | I.GE
    | I.LOAD
    | I.STORE
    | I.POW
    | I.FLOORDIV
)


@dataclass
class ByteCode:
    insns: List[Instruction]

    def __init__(self):
        self.insns = []

    def label(self):
        return Label(-1)

    def emit(self, instruction):
        self.insns.append(instruction)

    def emit_label(self, label):
        label.target = len(self.insns)

def print_bytecode(code: ByteCode):
    for i, insn in enumerate(code.insns):
        match insn:
            case I.JMP(Label(offset)) | I.JMP_IF_TRUE(Label(offset)) | I.JMP_IF_FALSE(Label(offset)):
                print(f"{i:=4} {insn.__class__.__name__:<15} {offset}")
            case I.LOAD(localID) | I.STORE(localID):
                print(f"{i:=4} {insn.__class__.__name__:<15} {localID}")
            case I.PUSH(value):
                print(f"{i:=4} {'PUSH':<15} {value}")
            case _:
                print(f"{i:=4} {insn.__class__.__name__:<15}")

class Frame:
    locals: List[Value]

    def __init__(self):
        MAX_LOCALS = 32
        self.locals = [None] * MAX_LOCALS

class VM:
    bytecode: ByteCode
    ip: int
    data: List[Value]
    currentFrame: Frame        
@dataclass
class Label:
    target: int

class I:
    """The instructions for our stack VM."""
    @dataclass
    class PUSH:
        what: Value

    @dataclass
    class UMINUS:
        pass
    @dataclass
    class UPLUS:
        pass
  
        pass
    @dataclass
    class ADD:
        pass

    @dataclass
    class SUB:
        pass

    @dataclass
    class MUL:
        pass

    @dataclass
    class DIV:
        pass

    @dataclass
    class QUOT:
        pass

    @dataclass
    class REM:
        pass

    @dataclass
    class EXP:
        pass

    @dataclass
    class EQ:
        pass

    @dataclass
    class NEQ:
        pass

    @dataclass
    class LT:
        pass

    @dataclass
    class GT:
        pass

    @dataclass
    class LE:
        pass

    @dataclass
    class GE:
        pass

    @dataclass
    class JMP:
        label: Label

    @dataclass
    class JMP_IF_FALSE:
        label: Label

    @dataclass
    class JMP_IF_TRUE:
        label: Label

    @dataclass
    class NOT:
        pass

    @dataclass
    class DUP:
        pass

    @dataclass
    class POP:
        pass

    @dataclass
    class LOAD:
        localID: int

    @dataclass
    class STORE:
        localID: int

    @dataclass
    class HALT:
        pass
    @dataclass
    class POW:
        pass
    @dataclass
    class FLOORDIV:
        pass
    class VM:
    bytecode: ByteCode
    ip: int
    data: List[Value]
    currentFrame: Frame

    def load(self, bytecode):
        self.bytecode = bytecode
        self.restart()

    def restart(self):
        self.ip = 0
        self.data = []
        self.currentFrame = Frame()

    def execute(self) -> Value:
        while True:
            assert self.ip < len(self.bytecode.insns)
            match self.bytecode.insns[self.ip]:
                case I.POW():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left**right)
                    self.ip += 1
                case I.FLOORDIV:
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left//right)
                    self.ip += 1
                case I.UPLUS():
                    op = self.data.pop()
                    self.data.append(+op)
                    self.ip += 1    
                case I.PUSH(val):
                    self.data.append(val)
                    self.ip += 1
                case I.PUSHFN(Label(offset)):
                    self.data.append(CompiledFunction(offset))
                    self.ip += 1
                case I.CALL():
                    self.currentFrame = Frame (
                        retaddr=self.ip + 1,
                        dynamicLink=self.currentFrame
                    )
                    cf = self.data.pop()
                    self.ip = cf.entry
                case I.RETURN():
                    self.ip = self.currentFrame.retaddr
                    self.currentFrame = self.currentFrame.dynamicLink
                case I.UMINUS():
                    op = self.data.pop()
                    self.data.append(-op)
                    self.ip += 1
                case I.ADD():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left+right)
                    self.ip += 1
                case I.SUB():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left-right)
                    self.ip += 1
                case I.MUL():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left*right)
                    self.ip += 1
                case I.DIV():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left/right)
                    self.ip += 1
                case I.EXP():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left**right)
                    self.ip += 1
                case I.QUOT():
                    right = self.data.pop()
                    left = self.data.pop()
                    if left.denominator != 1 or right.denominator != 1:
                        raise RunTimeError()
                    left, right = int(left), int(right)
                    self.data.append(Fraction(left // right, 1))
                    self.ip += 1
                case I.REM():
                    right = self.data.pop()
                    left = self.data.pop()
                    if left.denominator != 1 or right.denominator != 1:
                        raise RunTimeError()
                    left, right = int(left), int(right)
                    self.data.append(Fraction(left % right, 1))
                    self.ip += 1
                case I.EQ():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left==right)
                    self.ip += 1
                case I.NEQ():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left!=right)
                    self.ip += 1
                case I.LT():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left<right)
                    self.ip += 1
                case I.GT():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left>right)
                    self.ip += 1
                case I.LE():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left<=right)
                    self.ip += 1
                case I.GE():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left>=right)
                    self.ip += 1
                case I.JMP(label):
                    self.ip = label.target
                case I.JMP_IF_FALSE(label):
                    op = self.data.pop()
                    if not op:
                        self.ip = label.target
                    else:
                        self.ip += 1
                case I.JMP_IF_TRUE(label):
                    op = self.data.pop()
                    if op:
                        self.ip = label.target
                    else:
                        self.ip += 1
                case I.NOT():
                    op = self.data.pop()
                    self.data.append(not op)
                    self.ip += 1
                case I.DUP():
                    op = self.data.pop()
                    self.data.append(op)
                    self.data.append(op)
                    self.ip += 1
                case I.POP():
                    self.data.pop()
                    self.ip += 1
                case I.LOAD(localID):
                    self.data.append(self.currentFrame.locals[localID])
                    self.ip += 1
                case I.STORE(localID):
                    v = self.data.pop()
                    self.currentFrame.locals[localID] = v
                    self.ip += 1
                case I.HALT():
                    return self.data.pop()

def codegen(program: AST) -> ByteCode:
    code = ByteCode()
    do_codegen(program, code)
    code.emit(I.HALT())
    return code

def do_codegen (
        program: AST,
        code: ByteCode
) -> None:
    def codegen_(program):
        do_codegen(program, code)

    simple_ops = {
        "+": I.ADD(),
        "-": I.SUB(),
        "*": I.MUL(),
        "/": I.DIV(),
        "quot": I.QUOT(),
        "rem": I.REM(),
        "<": I.LT(),
        ">": I.GT(),
        "≤": I.LE(),
        "≥": I.GE(),
        "=": I.EQ(),
        "≠": I.NEQ(),
        "not": I.NOT(),
        "**":I.POW(),
        "//":I.FLOORDIV()

    }

    match program:
        case NumLiteral(what) | BoolLiteral(what) | StrLiteral(what):
            code.emit(I.PUSH(what))
        case UnitLiteral():
            code.emit(I.PUSH(None))
        case BinOp(op, left, right) if op in simple_ops:
            codegen_(left)
            codegen_(right)
            code.emit(simple_ops[op])
        case BinOp("and", left, right):
            E = code.label()
            codegen_(left)
            code.emit(I.DUP())
            code.emit(I.JMP_IF_FALSE(E))
            code.emit(I.POP())
            codegen_(right)
            code.emit_label(E)
        case BinOp("or", left, right):
            E = code.label()
            codegen_(left)
            code.emit(I.DUP())
            code.emit(I.JMP_IF_TRUE(E))
            code.emit(I.POP())
            codegen_(right)
            code.emit_label(E)
        case UnOp("-", operand):
            codegen_(operand)
            code.emit(I.UMINUS())
        case UnOp("+", operand):
            codegen_(operand)
            code.emit(I.UPLUS())    
        case Seq(things):
            if not things: raise BUG()
            last, rest = things[-1], things[:-1]
            for thing in rest:
                codegen_(thing)
                code.emit(I.POP())
            codegen_(last)
        case IfElse(cond, iftrue, iffalse):
            E = code.label()
            F = code.label()
            codegen_(cond)
            code.emit(I.JMP_IF_FALSE(F))
            codegen_(iftrue)
            code.emit(I.JMP(E))
            code.emit_label(F)
            codegen_(iffalse)
            code.emit_label(E)
        case While(cond, body):
            B = code.label()
            E = code.label()
            code.emit_label(B)
            codegen_(cond)
            code.emit(I.JMP_IF_FALSE(E))
            codegen_(body)
            code.emit(I.POP())
            code.emit(I.JMP(B))
            code.emit_label(E)
            code.emit(I.PUSH(None))
        case (Variable() as v) | UnOp("!", Variable() as v):
            code.emit(I.LOAD(v.localID))
        case Put(Variable() as v, e):
            codegen_(e)
            code.emit(I.STORE(v.localID))
            code.emit(I.PUSH(None))
        case Let(Variable() as v, e1, e2) | LetMut(Variable() as v, e1, e2):
            codegen_(e1)
            code.emit(I.STORE(v.localID))
            codegen_(e2)
        case LetFun(fv, _, _, body, expr):
            EXPRBEGIN = code.label()
            FBEGIN = code.label()
            code.emit(I.JMP(EXPRBEGIN))
            code.emit_label(FBEGIN)
            codegen_(body)
            code.emit(I.RETURN())
            code.emit_label(EXPRBEGIN)
            code.emit(I.PUSHFN(FBEGIN))
            code.emit(I.STORE(fv.localID))
            codegen_(expr)
        case FunCall(fn, _):
            code.emit(I.LOAD(fn.localID))
            code.emit(I.CALL())
        case TypeAssertion(expr, _):
            codegen_(expr)

def parse_string(s):
    return Parser.from_lexer(Lexer.from_stream(Stream.from_string(s))).parse_expr()

def parse_file(f):
    return Parser.from_lexer(Lexer.from_stream(Stream.from_file(f))).parse_expr()

def compile(program):
    return codegen(typecheck(resolve(program)))
def test_resolve():
    print(resolve(parse_string("let fun f(x : num) : num = let a = 1 in x + a end in f(0) end")))
def test_typecheck():
    e1 = NumLiteral(2)
    te1 = typecheck(e1)
    assert te1.type == FractionType()
    e2 = NumLiteral(3)
    e3 = BinOp("+", e1, e2)
    te3 = typecheck(e3)
    assert te3.type == FractionType()

def typecheck (
        program: AST,
        environment: EnvironmentType[Variable, SimType] = None
):
    if environment is None:
        environment = EnvironmentType()

    def typecheck_(p: AST):
        return typecheck(p, environment)
 def resolve (
        program: AST,
        rstate: ResolveState = None
) -> AST:
    if rstate is None:
        rstate = ResolveState()

    def resolve_(program):
        return resolve(program, rstate)           
 