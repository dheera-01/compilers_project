from typing import List
from dataclasses import dataclass
from declaration import AST
from my_parser import *
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
bytecode = ByteCode()
# emit some instructions and labels into the bytecode object...
vm = VirtualMachine() ###VirtualMachine class comes later in the code
vm.load_bytecode(bytecode.to_bytecode())
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
        
        "**":I.POW(),
        "//":I.FLOORDIV()

    }
    match program:
        case NumLiteral(what) | BoolLiteral(what) | StringLiteral(what):
            code.emit(I.PUSH(what))
        # case UnitLiteral():
        #     code.emit(I.PUSH(None))
        case BinOp(op, left, right) if op in simple_ops:
            codegen_(left)
            codegen_(right)
            code.emit(simple_ops[op])
class Frame:
    def __init__(self, retaddr=0, dynamicLink=None, locals=None):
        self.retaddr = retaddr
        self.dynamicLink = dynamicLink
        self.locals = locals or {}

    def __repr__(self):
        return f"<Frame retaddr={self.retaddr} locals={self.locals}>"
class I:    
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



class VirtualMachine:
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
###Other instructions like PUSHFN I haven't added as they are related to functions            

    
    









        

  

           







