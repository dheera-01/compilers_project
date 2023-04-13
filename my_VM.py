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
    class ADD:
        pass

    @dataclass
    class HALT:
        pass


Instruction = (
      I.PUSH
      | I.ADD
      | I.HALT)

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
    }

    match program:
        case NumLiteral(value):
            code.emit(I.PUSH(value))
        case BinOp(left, op, right) if op in simple_ops:
            codegen_(left)
            codegen_(right)
            code.emit(simple_ops[op])

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