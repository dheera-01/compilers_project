from dataclasses import dataclass
from typing import List
from declaration import *


# @dataclass
# class NumLiteral:
#     """A number literal."""
#     value: int
#
#     def __str__(self):
#         return f"{self.value}"
#
# @dataclass
# class BinOp:
#     """A binary operation."""
#     op: str
#     left: 'AST'
#     right: 'AST'
#
#     def __str__(self):
#         return f"({self.left} {self.op} {self.right})"
#
#
#
# Value = NumLiteral
#
# AST = (
#       NumLiteral
#     | BinOp
# )

class I:
    """The instructions for our stack VM."""
    @dataclass
    class PUSH:
        what: Value
    @dataclass
    class POP:
        what: Value
    @dataclass
    class ADD:
        pass

    @dataclass
    class HALT:
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
    class FLOORDIV:
        pass
    @dataclass
    class GT:
        pass
    @dataclass
    class LT:
        pass
    @dataclass
    class NE:
        pass
    @dataclass
    class E:
        pass
    @dataclass
    class POW:
        pass
    @dataclass
    class GE:
        pass
    @dataclass
    class LE:
        pass
    @dataclass
    class UPLUS:
        pass
    @dataclass
    class UMINUS:
        pass
    @dataclass
    class MOD:
        pass
Instruction = (
         I.PUSH
        |I.ADD
      
        |I.SUB
        |I.MUL
        |I.DIV
    
    #   |I.REM
    
        | I.UMINUS
        | I.UPLUS
      
        | I.POP
        | I.HALT
        | I.E
        | I.NE
        | I.LT
        | I.GT
        | I.LE
        | I.GE
        | I.MOD
    #   | I.LOAD
    #   | I.STORE
        | I.POW
        | I.FLOORDIV
)    

@dataclass
class ByteCode:
    insns: List[Instruction]

    def __init__(self):
        self.insns = []

    def emit(self, instruction):
        self.insns.append(instruction)

def print_bytecode(code: ByteCode):
    for i, insn in enumerate(code.insns):
        match insn:
            case I.PUSH(value):
                print(f"{i:=4} {'PUSH':<15} {value}")
            case I.ADD():
                print(f"{i:=4} {'ADD':<15}")
            case I.SUB():
                 print(f"{i:=4} {'SUB':<15}")
            case I.MUL():
                 print(f"{i:=4} {'MUL':<15}") 
            case I.DIV():
                 print(f"{i:=4} {'DIV':<15}") 
            case I.FLOORDIV():
                 print(f"{i:=4} {'FLOORDIV':<15}")  
            case I.GE():
                 print(f"{i:=4} {'GE':<15}")  
            case I.NE():
                 print(f"{i:=4} {'NE':<15}")                     
            case I.E():
                 print(f"{i:=4} {'E':<15}") 
            case I.LE():
                 print(f"{i:=4} {'LE':<15}")
            case I.POW():
                 print(f"{i:=4} {'POW':<15}")      
            case I.POP(value):
                 print(f"{i:=4} {'POP':<15} {value}")     
            case I.MOD():
                 print(f"{i:=4} {'MOD':<15}")                  
class VM:
    bytecode: ByteCode
    ip: int
    data: List[Value]

    def load(self, bytecode):
        self.bytecode = bytecode
        self.restart()

    def restart(self):
        self.ip = 0
        self.data = []

    def execute(self) -> Value:
        while True:
            assert self.ip < len(self.bytecode.insns)
            match self.bytecode.insns[self.ip]:
                case I.PUSH(val):
                    self.data.append(val)
                    self.ip += 1
                case I.ADD():
                    a = self.data.pop()
                    b = self.data.pop()
                    self.data.append(a + b)
                    self.ip += 1
                case I.HALT():
                    return self.data.pop()
                
                case I.SUB():
                 right = self.data.pop()
                 left = self.data.pop()
                 self.data.append(left-right)
                 self.ip += 1
                case I.GE():
                 right = self.data.pop()
                 left = self.data.pop()
                 self.data.append(left>=right)
                 self.ip += 1
                case I.FLOORDIV():
                 right = self.data.pop()
                 left = self.data.pop()
                 self.data.append(left//right)
                 self.ip += 1
                case I.POW():
                 right = self.data.pop()
                 left = self.data.pop()
                 self.data.append(left**right)
                 self.ip += 1
                case I.LE():
                 right = self.data.pop()
                 left = self.data.pop()
                 self.data.append(left<=right)
                 self.ip += 1
                case I.E():
                 right = self.data.pop()
                 left = self.data.pop()
                 self.data.append(left==right)
                 self.ip += 1
                case I.NE():
                 right = self.data.pop()
                 left = self.data.pop()
                 self.data.append(left!=right)
                 self.ip += 1
                case  I.MUL:
                 right = self.data.pop()
                 left = self.data.pop()
                 self.data.append(left*right)
                 self.ip += 1

                case I.DIV:
                 right = self.data.pop()
                 left = self.data.pop()
                 if  right== 0:
                    raise ZeroDivisionError()
                 self.data.append(left/right)
                 self.ip += 1
                case I.MOD:
                 right = self.data.pop()
                 left = self.data.pop()
                 if  right== 0:
                    raise ZeroDivisionError()
                 self.data.append(left%right)
                 self.ip += 1

def codegen(program: AST) -> ByteCode:
    code = ByteCode()
    do_codegen(program, code)
    code.emit(I.HALT())
    return code

def do_codegen (program: AST, code: ByteCode) -> None:

    def codegen_(program):
     do_codegen(program, code)

    simple_ops = {
        "+": I.ADD(),
        "-": I.SUB(),
        "/": I.DIV(),
        "**": I.POW(),
        "//": I.FLOORDIV(),
        '%': I.MOD()
        # ">=": I.GE(),
        # "<=": I.LE(),
        # "==": I.E(),
        # "!=": I.NE(),
        # ">": I.GT(),
        # "<": I.LT(),
    }

    match program:
        case NumLiteral(value):
            code.emit(I.PUSH(value))
        case BinOp(left, op, right) if op in simple_ops:
            codegen_(left)
            codegen_(right)
            code.emit(simple_ops[op])
        case ComparisonOp(left, op, right)if op in simple_ops:
            codegen_(left)
            codegen_(right)
            code.emit(simple_ops[op]) 

def test_codegen():
    program = BinOp(NumLiteral(10), '%',NumLiteral(2))
    code = codegen(program)
    print_bytecode(code)
test_codegen()    
def test_vm():
    program = BinOp(NumLiteral(10), '%',NumLiteral(2))
    code = codegen(program)
    vm = VM()
    vm.load(code)
    assert vm.execute() == 0