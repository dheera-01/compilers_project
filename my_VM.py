from dataclasses import dataclass
from typing import List
from declaration import *

l = []

@dataclass
class Label:
    target: int

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

    @dataclass
    class LOAD_FAST:
        what: str

    @dataclass
    class STORE_FAST:
        what: str
        is_mutable: bool

    @dataclass
    class STORE_FAST_UPDATE:
        what: str

    @dataclass
    class PRINT:
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
    class ENTER_SCOPE:
        pass
    
    @dataclass
    class EXIT_SCOPE:
        pass
        

    @dataclass
    class MAKE_LIST:
        pass

    @dataclass
    class LIST_OP:
        op: str # LEN, APPEND, HEAD, POP, UPDATE, TAIL

    @dataclass
    class INDEX:
        pass

Instruction = (
        I.PUSH
        | I.ADD

        | I.SUB
        | I.MUL
        | I.DIV

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
        | I.POW
        | I.FLOORDIV


        | I.LOAD_FAST
        | I.STORE_FAST
        | I.STORE_FAST_UPDATE

        | I.PRINT
        | I.MAKE_LIST
        | I.LIST_OP
        | I.INDEX
)


@dataclass
class ByteCode:
    insns: List[Instruction]
    flag: int
    trackList: List

    def __init__(self):
        self.insns = []
        self.flag = 0
        self.trackList = []

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

            case I.LOAD_FAST(name):
                print(f"{i:=4} {'LOAD_FAST':<15} {name}")
            case I.STORE_FAST(name , is_mutable):
                print(f"{i:=4} {'STORE_FAST':<15} {name} {is_mutable}")
            case I.STORE_FAST_UPDATE(name):
                print(f"{i:=4} {'STORE_FAST_UPDATE':<15} {name}")
            case I.PRINT():
                print(f"{i:=4} {'PRINT':<15}")
            case I.HALT():
                print(f"{i:=4} {'HALT':<15}")
                
            case I.GT():
                print(f"{i:=4} {'GT':<15}")
            case I.LT():
                print(f"{i:=4} {'LT':<15}")
                
            case I.JMP(Label(offset)) | I.JMP_IF_TRUE(Label(offset)) | I.JMP_IF_FALSE(Label(offset)):
                print(f"{i:=4} {insn.__class__.__name__:<15} {offset}")
                
            case I.ENTER_SCOPE():
                print(f"{i:=4} {'ENTER_SCOPE':<15}")
                
            case I.EXIT_SCOPE():
                print(f"{i:=4} {'EXIT_SCOPE':<15}")

            case I.MAKE_LIST():
                print(f"{i:=4} {'MAKE_LIST':<15}")
            case I.LIST_OP(op):
                print(f"{i:=4} {'LIST_OP':<15} {op}")
            case I.INDEX():
                print(f"{i:=4} {'INDEX':<15}")


class VM:
    bytecode: ByteCode
    ip: int
    data: List[Value]
    program_env: Environment()

    def load(self, bytecode):
        self.bytecode = bytecode
        self.program_env = Environment()
        self.restart()

    def restart(self):
        self.ip = 0
        self.data = []

    def execute(self) -> Value:
        while True:
            # print(self.data)
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

                case I.SUB():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left - right)
                    self.ip += 1
                case I.GE():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left >= right)
                    self.ip += 1
                case I.GT():
                    a = self.data.pop()
                    b = self.data.pop()
                    self.data.append(a < b)
                    self.ip += 1
                case I.LT():
                    a = self.data.pop()
                    b = self.data.pop()
                    self.data.append(a > b)
                    self.ip += 1
                case I.FLOORDIV():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left // right)
                    self.ip += 1
                case I.POW():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left ** right)
                    self.ip += 1
                case I.LE():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left <= right)
                    self.ip += 1
                case I.E():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left == right)
                    self.ip += 1
                case I.NE():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left != right)
                    self.ip += 1
                case I.MUL:
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left * right)
                    self.ip += 1
                case I.DIV:
                    right = self.data.pop()
                    left = self.data.pop()
                    if right == 0:
                        raise ZeroDivisionError()
                    self.data.append(left / right)
                    self.ip += 1
                case I.MOD:
                    right = self.data.pop()
                    left = self.data.pop()
                    if right == 0:
                        raise ZeroDivisionError()
                    self.data.append(left % right)
                    self.ip += 1

                case I.STORE_FAST(name, is_mutable):
                    top = self.data.pop()
                    ident = Identifier(name, is_mutable=is_mutable)
                    self.program_env.add(ident, top)
                    self.ip += 1
                case I.LOAD_FAST(name):
                    value = self.program_env.get(name)
                    self.data.append(value)
                    self.ip += 1
                case I.STORE_FAST_UPDATE(name):
                    top = self.data.pop()
                    ident = Identifier(name)
                    self.program_env.update(ident, top)
                    self.ip += 1
                case I.PRINT():
                    print(self.data.pop())
                    self.ip += 1
                case I.ENTER_SCOPE():
                    # Enter scope
                    self.program_env.enter_scope()
                    self.ip += 1
                
                case I.EXIT_SCOPE():
                    # Exit scope
                    self.program_env.exit_scope()
                    self.ip += 1
                

                case I.MAKE_LIST():
                    lst = []
                    while True:
                        val = self.data.pop()
                        if val == 'LIST_BEGIN':
                            break
                        lst.append(val)
                    lst.reverse()
                    self.data.append(lst)
                    self.ip += 1

                case I.LIST_OP(op):
                    lst = self.data.pop()
                    # LEN, APPEND, HEAD, POP, UPDATE, TAIL
                    if op == 'LEN':
                        self.data.append(len(lst))
                    elif op == 'APPEND':
                        lst.append(self.data.pop())
                        self.data.append(lst)
                    elif op == 'HEAD':
                        self.data.append(lst[0])
                    elif op == 'POP':
                        self.data.append(lst.pop())
                        self.data.append(lst)
                    elif op == 'UPDATE':
                        value = self.data.pop()
                        index = self.data.pop()
                        lst[index] = value
                        self.data.append(lst)
                    elif op == 'TAIL':
                        self.data.append(lst[-1])
                    self.ip += 1

                case I.INDEX():
                    obj = self.data.pop()
                    index = self.data.pop()
                    self.data.append(obj[index])
                    self.ip += 1

                # Jump cases    
                case I.JMP(label):
                    self.ip = label.target
                    # self.ip += 1
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
                    return



def codegen(program: AST) -> ByteCode:
    code = ByteCode()
    do_codegen(program, code)
    code.emit(I.HALT())
    return code


def do_codegen(program: AST, code: ByteCode) -> None:
    def codegen_(program):
        do_codegen(program, code)

    simple_ops = {
        "+": I.ADD(),
        "-": I.SUB(),
        "/": I.DIV(),
        "**": I.POW(),
        "//": I.FLOORDIV(),
        '%': I.MOD(), 
        '>': I.GT(),
        '<': I.LT(),
        '<=': I.LE(),
        '>=': I.GE(),
        
        # ">=": I.GE(),
        # "<=": I.LE(),
        "==": I.E(),
        "!=": I.NE(),
        # ">": I.GT(),
        # "<": I.LT(),
    }
    
    match program:
        
        case Sequence(statements):
            for statement in statements:
                codegen_(statement)
        case NumLiteral(value) | StringLiteral(value):
            code.emit(I.PUSH(value))

        case BinOp(left, op, right) if op in simple_ops:
            codegen_(left)
            codegen_(right)
            code.emit(simple_ops[op])
        case ComparisonOp(left, op, right) if op in simple_ops:
            codegen_(left)
            codegen_(right)
            code.emit(simple_ops[op])
        case Assign(identifier, right):
            
            for i, ident in enumerate(identifier):
                codegen_(right[i])
                code.emit(I.STORE_FAST(ident.name, ident.is_mutable))
        case Identifier(name):
            code.emit(I.LOAD_FAST(name))
        case Update(identifier, op, right):
            codegen_(right)
            if op._operator == "=":
                code.emit(I.STORE_FAST_UPDATE(identifier.name))
            else:
                codegen_(identifier)
                code.emit(simple_ops[op._operator[: len(op._operator) - 1]])
                code.emit(I.STORE_FAST_UPDATE(identifier.name))
        case Print(value):
            codegen_(value)
            code.emit(I.PRINT())

        case ListLiteral(value):
            code.emit(I.PUSH('LIST_BEGIN'))
            for element in value:
                codegen_(element)
            code.emit(I.MAKE_LIST())

        case ListOperations(identifier, val, item, indVal):
            if val == "LEN":
                codegen_(identifier)
                code.emit(I.LIST_OP('LEN'))
            elif val == "HEAD":
                codegen_(identifier)
                code.emit(I.LIST_OP('HEAD'))
            elif val == "TAIL":
                codegen_(identifier)
                code.emit(I.LIST_OP('TAIL'))
            elif val == "APPEND":
                codegen_(item)
                codegen_(identifier)
                code.emit(I.LIST_OP('APPEND'))
            elif val == "POP":
                codegen_(identifier)
                code.emit(I.LIST_OP('POP'))
                code.emit(I.STORE_FAST_UPDATE(identifier.name))
            elif val == "ChangeOneElement":
                codegen_(indVal)
                codegen_(item)
                codegen_(identifier)
                code.emit(I.LIST_OP('UPDATE'))

        case Indexer(identifier, indexVal):
            codegen_(indexVal)
            codegen_(identifier)
            code.emit(I.INDEX())

            
        # case IfElse(condition, if_body, elif_body, else_body):
        #     label1 = code.label()
        #     label2 = code.label()
        #     # label3 = code.label()
        #     codegen_(condition)
        #     code.emit(I.JMP_IF_FALSE(label1))
        #
        #     codegen_(if_body)
        #
        #     if(code.flag > 0):
        #         label = code.trackList.pop()
        #         code.emit(I.JMP(label))
        #         code.trackList.append(label)
        #
        #     else:
        #         code.trackList.append(label2)
        #         code.emit(I.JMP(label2))
        #
        #     code.emit_label(label1)
        #     if(len(elif_body) != 0):
        #         code.flag += 1
        #
        #
        #     for elif_ in elif_body:
        #         codegen_(elif_)
        #
        #     if(len(elif_body) != 0):
        #         code.flag -= 1
        #
        #     codegen_(else_body)
        #     if code.flag == 0:
        #         code.emit_label((label2))

        case IfElse(condition, if_body, elif_body, else_body):
            elif_list = []

            new_if = IfElse(condition, if_body, [], None)
            elif_list.append(new_if)

            labels = []
            for elif_ in elif_body:
                elif_list.append(elif_)

            for elif_ in elif_list:
                label1 = code.label()
                label2 = code.label()
                codegen_(elif_.condition)
                code.emit(I.JMP_IF_FALSE(label1))
                codegen_(elif_.if_body)
                code.emit(I.JMP(label2))
                code.emit_label(label1)
                labels.append(label2)

            codegen_(else_body)
            for label in labels:
                code.emit_label(label)
                
        case While(condition, body):
            label1 = code.label()
            label2 = code.label()
            code.emit_label(label1)
            codegen_(condition)
            code.emit(I.JMP_IF_FALSE(label2))
            code.emit(I.ENTER_SCOPE())
            codegen_(body)
            code.emit(I.EXIT_SCOPE())
            code.emit(I.JMP(label1))
            code.emit_label(label2)
            
        case For(exp1, condition, exp2, body):
            label1 = code.label()
            label2 = code.label()
            label3 = code.label()
            codegen_(exp1)
            code.emit_label(label1)
            codegen_(condition)
            code.emit(I.JMP_IF_FALSE(label2))
            # Enter scope
            code.emit(I.ENTER_SCOPE())
            codegen_(body)
            # Exit scope
            code.emit(I.EXIT_SCOPE())
            
            codegen_(exp2)
            code.emit(I.JMP(label1))
            code.emit_label(label2)
            


            
            

# Program for while nested loop

    # program = Sequence(
    #     [
    #         Assign((Identifier("i"), Identifier("j")), (NumLiteral(0), NumLiteral(0))),
    #         While(ComparisonOp(Identifier("i"), '<',  NumLiteral(10)), 
    #               Sequence([Print(Identifier("i")), 
    #                         While(ComparisonOp(Identifier("j"), '<',  NumLiteral(3)), Sequence([Print(StringLiteral("Hi")), Update(Identifier("j"), Operator("="), BinOp(Identifier("j"), "+", NumLiteral(1)))])),
    #                         Update(Identifier("i"), Operator("="), BinOp(Identifier("i"), "+", NumLiteral(1)))]
    #                        ))
    #     ]
    # )
    
# Program for while single loop

    # program = Sequence(
    #     [
    #         Assign((Identifier("i"), Identifier("j")), (NumLiteral(0), NumLiteral(0))),
    #         While(ComparisonOp(Identifier("i"), '<',  NumLiteral(10)), 
    #               Sequence([Print(Identifier("i")), Update(Identifier("i"), Operator("="), BinOp(Identifier("i"), "+", NumLiteral(1)))]))
    #     ]
    # )    

# Program for Single For loop

    # program = Sequence(
    #     [
    #         For(Assign((Identifier("i"),) , (NumLiteral(0), )), 
    #             ComparisonOp(Identifier("i"), '<',  NumLiteral(10)), 
    #             Update(Identifier("i"), Operator("="), BinOp(Identifier("i"), "+", NumLiteral(1))), 
    #             Sequence([Print(Identifier("i"))])
    #             )
    #     ]
    # )
    
# Program for Nested For loop

    # program = Sequence(
    #     [
    #         For(Assign((Identifier("i", is_mutable=True), ) , (NumLiteral(0), )), 
    #             ComparisonOp(Identifier("i"), '<',  NumLiteral(5)), 
    #             Update(Identifier("i"), Operator("="), BinOp(Identifier("i"), "+", NumLiteral(1))), 
    #             Sequence([Print(Identifier("i")), 
    #                       For(Assign((Identifier("j", is_mutable=True),) , (NumLiteral(0), )),
    #                             ComparisonOp(Identifier("j", is_mutable= True), '<',  NumLiteral(3)),
    #                             Update(Identifier("j", is_mutable=True), Operator("="), BinOp(Identifier("j", is_mutable=True), "+", NumLiteral(1))),
    #                             Sequence([Print(StringLiteral("Hi"))])
    #                           )
    #                       ])
    #             )
    #     ]
    # )

# Program for if-else

    # program = Sequence(
    #     [
    #         # Assign((Identifier("a", is_mutable=False)), (NumLiteral(10),)),
    #         IfElse(ComparisonOp(NumLiteral(1), '<',  NumLiteral(2)),
    #                Sequence([Print(StringLiteral("Hello"))]), 
    #               [IfElse(ComparisonOp(NumLiteral(6), '<', NumLiteral(4)), Sequence([Print(StringLiteral("Equal"))]), [], None), IfElse(ComparisonOp(NumLiteral(9), '>', NumLiteral(5)), Sequence([Print(StringLiteral("NotEqual"))]), [], None)],
    #                Sequence([Print(StringLiteral("World"))]))
    #     ]
    # )

# Program for assign, update, const

    # program = Sequence(
    #      [
    #          Assign((Identifier("i"), Identifier("j")), (NumLiteral(0), NumLiteral(0))),
    #          While(ComparisonOp(Identifier("i"), '<',  NumLiteral(10)), 
    #                Sequence([Print(Identifier("i")), 
    #                          While(ComparisonOp(Identifier("j"), '<=',  NumLiteral(3)), Sequence([Print(StringLiteral("Hi")), Update(Identifier("j"), Operator("="), BinOp(Identifier("j"), "+", NumLiteral(1)))])),
    #                          Update(Identifier("i"), Operator("="), BinOp(Identifier("i"), "+", NumLiteral(1)))]
    #                         ))
    #      ]
    #  )

# Program for listLiteral

# program = Sequence(
#          [
#              Assign((Identifier("arr"),),(ListLiteral([ListLiteral([NumLiteral(1), NumLiteral(4)]), NumLiteral(2), NumLiteral(3)]),))
#              ,Print(Identifier("arr"))
#              ,Assign((Identifier("i"),),(NumLiteral(0),))
#              ,Print(Indexer(Identifier("arr"), Identifier("i")))
#              ,Print(ListOperations(Identifier("arr"), "LEN", None, None))
#              ,Print(ListOperations(Identifier("arr"), "HEAD", None, None))
#                 ,Print(ListOperations(Identifier("arr"), "TAIL", None, None))
#                 ,Print(ListOperations(Identifier("arr"), "APPEND", NumLiteral(5), None))
#                 ,Print(ListOperations(Identifier("arr"), "POP", None, None))
#                 ,Print(ListOperations(Identifier("arr"), "ChangeOneElement", NumLiteral(5), NumLiteral(1)))
#          ]
#      )
      

      
def test_codegen():

    # Make case for FOR loop
    program = Sequence(
        [
            Assign((Identifier("i"),), (NumLiteral(0),)),
            While(ComparisonOp(Identifier("i"), '<',  NumLiteral(10)), 
                  Sequence([Assign((Identifier("j"),), (NumLiteral(0),)),
                            Print(Identifier("i")), 
                            While(ComparisonOp(Identifier("j"), '<',  NumLiteral(3)), Sequence([Print(StringLiteral("Hi")), Update(Identifier("j"), Operator("="), BinOp(Identifier("j"), "+", NumLiteral(1)))])),
                            Update(Identifier("i"), Operator("="), BinOp(Identifier("i"), "+", NumLiteral(1)))]
                           ))
        ]
    )
    code = codegen(program)
    print_bytecode(code)

# test_codegen()

def test_vm():
    program = Sequence(
        [
            Assign((Identifier("i"),), (NumLiteral(0),)),
            While(ComparisonOp(Identifier("i"), '<',  NumLiteral(10)), 
                  Sequence([Assign((Identifier("j"),), (NumLiteral(0),)),
                            Print(Identifier("i")), 
                            While(ComparisonOp(Identifier("j"), '<',  NumLiteral(3)), Sequence([Print(StringLiteral("Hi")), Update(Identifier("j"), Operator("="), BinOp(Identifier("j"), "+", NumLiteral(1)))])),
                            Update(Identifier("i"), Operator("="), BinOp(Identifier("i"), "+", NumLiteral(1)))]
                           ))
        ]
    )
        

    code = codegen(program)
    print_bytecode(code)
    vm = VM()
    vm.load(code)
    vm.execute()

test_vm()
