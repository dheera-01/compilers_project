from typing import List
from dataclasses import dataclass
from declaration import AST

from typing import Optional,TypeVar,MutableMapping
from dataclasses import dataclass
from my_parser import *
from my_lexer import *
class BUG(Exception):
        pass
class ResolveError(Exception):
    pass
T = TypeVar('T')
U = TypeVar('U')
Env = MutableMapping[U, T]

class EnvironmentType(MutableMapping[U, T]):
    def __init__(self):
        self.envs = [{}]

    def begin_scope(self):
        self.envs.append({})

    def end_scope(self):
        self.envs.pop()

    def __getitem__(self, k):
        for env in reversed(self.envs):
            if k in env:
                return env[k]

    def __setitem__(self, k, v):
        self.envs[-1][k] = v

    def __delitem__(self, k):
        for env in reversed(self.envs):
            if k in env:
                del env[k]

    def __iter__(self):
        return iter(dict.fromkeys(self))

    def __len__(self):
        return len(dict.fromkeys(self))
arithmetic_ops = [ "+", "-", "*", "/", "//", "%","**" ]
comp_ops        = [ "<", ">", "<=", ">=" ]
eq_ops         = [ "=", "!=" ]
lo_ops         = [ "and", "or" ] 
SimType=NumLiteral|StringLiteral


@dataclass
class Variable:
    name: str
    id: int = None
    fdepth: int = None
    localID: int = None
    type: Optional[SimType] = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"{self.name}::{self.id}::{self.localID}"   

def cmptype(t:SimType):
    return t in [NumLiteral(), StringLiteral()]


class ResolveState:
    env: EnvironmentType[str, Variable]
    stk: List[List[int]]
    lastID: int

    def __init__(self):
        self.env = EnvironmentType()
        self.stk = [[0, -1]]
        self.lastID = -1

    def begin_fun(self):
        self.stk.append([0, -1])

    def end_fun(self):
        self.stk.pop()

    def handle_new(self, v):
        v.fdepth = len(self.stk) - 1
        v.id = self.lastID = self.lastID + 1
        v.localID = self.stk[-1][1] = self.stk[-1][1] + 1
        self.env[v.name] = v

    def begin_scope(self):
        self.env.begin_scope()

    def end_scope(self):
        self.env.end_scope()

def resolve (
        program: AST,
        rstate: ResolveState = None
) -> AST:
    if rstate is None:
        rstate = ResolveState()

    def resolve_(program):
        return resolve(program, rstate)

    match program:
        case NumLiteral() | BoolLiteral() | StringLiteral():
            return program
        case UnaryOp(op, e):
            re = resolve_(e)
            return UnaryOp(op, re)
        case BinOp(op, left, right):
            rleft = resolve_(left)
            rright = resolve_(right)
            return BinOp(op, rleft, rright)
        case Variable(name):
            if name not in rstate.env:
                raise ResolveError()
            declared = rstate.env[name]
            return declared
     
        case Sequence(things):
            rthings = []
            for e in things:
                rthings.append(resolve_(e))
            return Sequence(rthings)
  
           # return TypeAssertion(rexpr, type)
        case _:
             raise BUG()

 

@dataclass
class Label:
    target: int

class I:
 ##The instructions for stack VM.
    @dataclass
    class PUSH:
        what: Value

    @dataclass
    class UMINUS:
        pass
    @dataclass
    class UPLUS:
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
    class REM:
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
Instruction = (
      I.PUSH
    | I.ADD
    | I.SUB
    | I.MUL
    | I.DIV
    
    | I.REM
    
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

    def label(self):  #To mark position in bytecode
        return Label(-1)

    def emit(self, instruction):#to add an instruction to the bytecode sequence.
        self.insns.append(instruction)

    def emit_label(self, label):# to mark the current position in the bytecode with a given Label object.
        label.target = len(self.insns)

    def to_bytecode(self) -> bytes:# to convert the sequence of instructions into bytes that can be executed by our virtual machine
        bytecode = b''
        for instr in self.insns:
            bytecode += instr.to_bytes()
        return bytecode
    
   
def print_bytecode(code: ByteCode):
    i = 0
    while i < len(code.insns):
        insn = code.insns[i]
        if isinstance(insn, (I.JMP, I.JMP_IF_TRUE, I.JMP_IF_FALSE)):
            offset = insn.arg
            print(f"{i:=4} {insn.__class__.__name__:<15} {offset}")
            i += 1
        elif isinstance(insn, (I.LOAD, I.STORE)):
            localID = insn.arg
            print(f"{i:=4} {insn.__class__.__name__:<15} {localID}")
            i += 1
        elif isinstance(insn, I.PUSH):
            value = insn.arg
            print(f"{i:=4} {'PUSH':<15} {value}")
            i += 1        

class VirtualMachine:
    insns: List[Instruction]
    def __init__(self):
        self.bytecode = None
        self.ip = 0
        self.data = []
        self.currentFrame = None

    def load(self, bytecode):
        self.bytecode = bytecode
        self.restart()

    def restart(self):
        self.ip = 0
        self.data = []
        self.currentFrame = Frame()
    # def load_bytecode(self, byte_code):
    #  for instruction in byte_code.insns:
    #     self.code.emit(instruction)

    def execute(self) -> Value:
        while True:
            assert self.ip < len(self.bytecode.insns)
            insn = self.bytecode.insns[self.ip]

            if isinstance(insn, I.POW):
                right = self.data.pop()
                left = self.data.pop()
                self.data.append(left**right)
                self.ip += 1

            elif isinstance(insn, I.FLOORDIV):
                right = self.data.pop()
                left = self.data.pop()
                if  right== 0:
                    raise ZeroDivisionError()
                self.data.append(left//right)
                self.ip += 1

            elif isinstance(insn, I.UPLUS):
                op = self.data.pop()
                self.data.append(+op)
                self.ip += 1

            elif isinstance(insn, I.PUSH):
                self.data.append(insn.val)
                self.ip += 1
            elif isinstance(insn, I.UMINUS):
                op = self.data.pop()
                self.data.append(-op)
                self.ip += 1

            elif isinstance(insn, I.ADD):
                right = self.data.pop()
                left = self.data.pop()
                self.data.append(left+right)
                self.ip += 1

            elif isinstance(insn, I.SUB):
                right = self.data.pop()
                left = self.data.pop()
                self.data.append(left-right)
                self.ip += 1

            elif isinstance(insn, I.MUL):
                right = self.data.pop()
                left = self.data.pop()
                self.data.append(left*right)
                self.ip += 1

            elif isinstance(insn, I.DIV):
                right = self.data.pop()
                left = self.data.pop()
                if  right== 0:
                    raise ZeroDivisionError()
                self.data.append(left/right)
                self.ip += 1

          

        

            elif isinstance(insn, I.REM):
                right = self.data.pop()
                left = self.data.pop()
                if  right==0:
                    raise ZeroDivisionError()
                left, right = int(left), int(right)
                self.data.append(left % right, 1)
                self.ip += 1

            elif isinstance(insn, I.EQ):
               right = self.data.pop()
               left = self.data.pop()
               self.data.append(left == right)
               self.ip += 1
            elif isinstance(insn, I.NEQ):
               right = self.data.pop()
               left = self.data.pop()
               self.data.append(left != right)
               self.ip += 1
            elif isinstance(insn, I.LT):
               right = self.data.pop()
               left = self.data.pop()
               self.data.append(left < right)
               self.ip += 1
            elif isinstance(insn, I.GT):
               right = self.data.pop()
               left = self.data.pop()
               self.data.append(left > right)
               self.ip += 1
            elif isinstance(insn, I.LE):
              right = self.data.pop()
              left = self.data.pop()
              self.data.append(left <= right)
              self.ip += 1
            elif isinstance(insn, I.GE):
              right = self.data.pop()
              left = self.data.pop()
              self.data.append(left >= right)
              self.ip += 1
            elif isinstance(insn, I.JMP):
              self.ip = insn.label.target
            elif isinstance(insn, I.JMP_IF_FALSE):
              op = self.data.pop()
              if not op:
               self.ip = insn.label.target
            # else:
            #   self.ip += 1
            elif isinstance(insn, I.JMP_IF_TRUE):
              op = self.data.pop()
              if op:
               self.ip = insn.label.target
              else:
                        self.ip += 1 
            # else:
            #   self.ip += 1
         
            elif isinstance(insn, I.DUP):
                op = self.data.pop()
                self.data.append(op)
                self.data.append(op)
                self.ip += 1
            elif isinstance(insn, I.POP):
                self.data.pop()
                self.ip += 1
            elif isinstance(insn, I.LOAD):
                self.data.append(self.currentFrame.locals[insn.localID])
                self.ip += 1
            elif isinstance(insn, I.STORE):
                 v = self.data.pop()
                 self.currentFrame.locals[insn.localID] = v
                 self.ip += 1
            elif isinstance(insn, I.HALT):
                 return self.data.pop()
   
  
class Frame:
    def __init__(self, retaddr=0, dynamicLink=None, locals=None):
        self.retaddr = retaddr
        self.dynamicLink = dynamicLink
        self.locals = locals or {}

    def __repr__(self):
        return f"<Frame retaddr={self.retaddr} locals={self.locals}>"   


def codegen_(program: AST) -> ByteCode:
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
       
        "rem": I.REM(),
        "<": I.LT(),
        ">": I.GT(),
        "<=": I.LE(),
        ">=": I.GE(),
        "=": I.EQ(),
        "!=": I.NEQ(),
        
        "**":I.POW(),
        "//":I.FLOORDIV()

    
    }





    match program:
        case Sequence(things):
            if not things: raise BUG()
            last, rest = things[-1], things[:-1]
            for thing in rest:
                codegen_(thing)
                code.emit(I.POP())
            codegen_(last)
            # print(f"ans: {ans}")
            # ans = []
            # for statement in statements:
            #     # print(f"statement: {statement}")
            #     ans.append(eval(statement, environment))
            # # print(f"ans: {ans}")
            # return ans

        case NumLiteral(what):
            # print(program)
            code.emit(I.PUSH(what))

        case FloatLiteral(what):
             code.emit(I.PUSH(what))


        case StringLiteral(what):
             code.emit(I.PUSH(what))


        case BoolLiteral(what):
             code.emit(I.PUSH(what))

        
        case BinOp(op, left, right) if op in simple_ops:
            codegen_(left)
            codegen_(right)
            code.emit(simple_ops[op])
        # unary operation
        case UnaryOp("-", x):
            codegen_(x)
            code.emit(I.UMINUS())

        case UnaryOp("+", x):
            codegen_(x)
            code.emit(I.UPLUS())

        # binary operation
        

def parse_string(s):
    return Parser.from_lexer(Lexer.from_stream(Stream.from_string(s))).parse_expr()  

def compile(program):
    return codegen_((resolve(program)))
def test_codegen():
    programs = {
        "5*2",
        "8/2"

    }   
    v = VirtualMachine()
    for p, e in programs.items():
        v.load(compile(parse_string(p)))
        assert e == v.execute()

def print_codegen():
    print_bytecode(compile(parse_string("5*2")))    
print_codegen() 






        


       

        








