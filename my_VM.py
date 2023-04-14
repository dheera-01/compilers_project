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

@dataclass
class Label:
    target: int

class I:
    """The instructions for our stack VM."""
    @dataclass
    class PUSH:
        what: Value
    
    @dataclass
    class ADD:
        pass

    @dataclass
    class HALT:
        pass
    @dataclass
    class UMINUS:
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
    class LT:
        pass

    @dataclass
    # Greater than
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
    class POP:
        pass


Instruction = (
        I.PUSH
        | I.ADD
        | I.HALT
        | I.JMP
        | I.JMP_IF_FALSE
        | I.JMP_IF_TRUE
        | I.POP
        | I.LT
        | I.GT
      )

@dataclass
class ByteCode:
    insns: List[Instruction]

    def __init__(self):
        self.insns = []

    def emit(self, instruction):
        self.insns.append(instruction)
        
    def label(self):
        return Label(-1)

    def emit_label(self, label):
        label.target = len(self.insns)

def print_bytecode(code: ByteCode):
    for i, insn in enumerate(code.insns):
        match insn:
            case I.PUSH(value):
                print(f"{i:=4} {'PUSH':<15} {value}")
            case I.ADD():
                print(f"{i:=4} {'ADD':<15}")
            case I.GT():
                print(f"{i:=4} {'GT':<15}")
            case I.LT():
                print(f"{i:=4} {'LT':<15}")
            case I.JMP(Label(offset)) | I.JMP_IF_TRUE(Label(offset)) | I.JMP_IF_FALSE(Label(offset)):
                print(f"{i:=4} {insn.__class__.__name__:<15} {offset}")

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
                case I.GT():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(right < left)
                    self.ip += 1
                case I.LT():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(right > left)
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
                case I.POP():
                    self.data.pop()
                    self.ip += 1
                case I.HALT():
                    return self.data.pop()



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
    }

    match program:
        case NumLiteral(value):
            code.emit(I.PUSH(value))
        case BinOp(left, op, right) if op in simple_ops:
            codegen_(left)
            codegen_(right)
            code.emit(simple_ops[op])
            
        case ComparisonOp(left, op, right) if op in simple_ops:
            codegen_(left)
            codegen_(right)
            code.emit(simple_ops[op])
            
        case IfElse(condition, if_body, elif_body, else_body):
            E = code.label()
            F = code.label()
            # G = code.label()
            # codegen_(condition)
            # code.emit(I.JMP_IF_FALSE(F))
            # codegen_(if_body)
            # code.emit(I.JMP(G))
            # code.emit_label(F)
            # codegen_(elif_body)
            # code.emit(I.JMP(G))
            # code.emit_label(G)


            codegen_(condition)
            code.emit(I.JMP_IF_FALSE(F))
            codegen_(if_body)
            code.emit(I.JMP(E))
            code.emit_label(F)
            codegen_(else_body)
            code.emit_label(E)
            
            # codegen_(condition)
            # label = code.label()
            # code.emit(I.JMP_IF_FALSE(label))
            # codegen_(if_body)
            # code.emit_label(label)

def test_codegen():
    program = BinOp(NumLiteral(1), '+',NumLiteral(2))
    code = codegen(program)
    print_bytecode(code)

def test_vm():
    program = BinOp(NumLiteral(1), '+',NumLiteral(2))
    code = codegen(program)
    vm = VM()
    vm.load(code)
    assert vm.execute() == 3
    
# Test if else
# def test_codegen():
#     program = IfElse(2<3, print("Hello"), None, print("World"))
#     code = codegen(program)
#     print_bytecode(code)

# def test_vm():
#     program = IfElse(2<3, print("Hello"), None, print("World"))
#     code = codegen(program)
#     vm = VM()
#     vm.load(code)
#     assert vm.execute() == "Hello"

# Test comparison operations    
# def test_codegen():
#     condition = ComparisonOp(NumLiteral(1), '<', NumLiteral(2))
#     program = IfElse(condition, print("45"), None, print("33"))
#     code = codegen(program)
#     print_bytecode(code)
    
# def test_vm():
#     condition = ComparisonOp(NumLiteral(1), '<', NumLiteral(2))
#     program = IfElse(condition, print("45"), None, print("33"))
#     code = codegen(program)
#     vm = VM()
#     vm.load(code)   
#     assert vm.execute() == True
    
test_vm()
test_codegen()
