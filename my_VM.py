from dataclasses import dataclass
from typing import List
from declaration import *

l = []

@dataclass
class Label:
    target: int

@dataclass
class CallFrame:
    caller: Label
    callee: Label

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
    @dataclass
    class MAKE_FUNC:
        name: Identifier
        args: List[Identifier]
        body: Sequence

    @dataclass
    class CALL_FUNC:
        name:Identifier
        args:List['AST']

    @dataclass
    class GET_FUNC:
        name:Identifier
    @dataclass
    class PUSH_ARGS:
        args: List['AST']

    @dataclass
    class LOAD_ARGS:
        pass

    @dataclass
    class RETURN:
        pass



    @dataclass
    class CREATE_FRAME:
        caller: Label
    @dataclass
    class DESTROY_FRAME:
        pass

    @dataclass
    class STORE_LABEL:
        name: str
        label: Label

    @dataclass
    class LOAD_LABEL:
        name: str

    @dataclass
    class JMP_TO_FUNC:
        name: str

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

        | I.MAKE_FUNC
        | I.CALL_FUNC
        | I.GET_FUNC
        | I.PUSH_ARGS
        | I.LOAD_ARGS
        | I.RETURN
        | I.CREATE_FRAME
        | I.DESTROY_FRAME
        | I.STORE_LABEL
        | I.LOAD_LABEL
        | I.JMP_TO_FUNC
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

            case I.MAKE_FUNC(Identifier(name), args, body):
                print(f"{i:=4} {'MAKE_FUNC':<15} {name} ")
            case I.GET_FUNC(Identifier(name)):
                print(f"{i:=4} {'GET_FUNC':<15} {name} ")
            case I.RETURN():
                print(f"{i:=4} {'RETURN VALUE':<15} ")
            case I.PUSH_ARGS(args):
                print(f"{i:=4} {'PUSH_ARGS':<15} {args} ")
            case I.LOAD_ARGS():
                print(f"{i:=4} {'LOAD_ARGS':<15}  ")

            case I.CREATE_FRAME():
                print(f"{i:=4} {'CREATE_FRAME':<15}  ")
            case I.DESTROY_FRAME():
                print(f"{i:=4} {'DESTROY_FRAME':<15}  ")
            case I.LOAD_LABEL(name):
                print(f"{i:=4} {'LOAD_LABEL':<15} {name} ")
            case I.STORE_LABEL(name,label):
                print(f"{i:=4} {'STORE_LABEL':<15}  ")
            case I.JMP_TO_FUNC(name):
                print(f"{i:=4} {'JMP_TO_FUNC':<15} {name} ")




class VM:
    bytecode: ByteCode
    ip: int
    data: List[Value]
    program_env: Environment()
    call_frame: List[CallFrame]
    label_dict: dict
    def load(self, bytecode):
        self.bytecode = bytecode
        self.program_env = Environment()
        self.restart()
        self.call_frame = []
        self.label_dict={}

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
                case I.MUL():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left * right)
                    self.ip += 1
                case I.DIV():
                    right = self.data.pop()
                    left = self.data.pop()
                    if right == 0:
                        raise ZeroDivisionError()
                    self.data.append(left / right)
                    self.ip += 1
                case I.MOD():
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
                case I.MAKE_FUNC(name, args, body):
                    self.program_env.add(name, Function(name, args, body))
                    self.ip += 1

                case I.CALL_FUNC(function,args):
                    self.ip += 1
                case I.GET_FUNC(Identifier(name)):
                    func = self.program_env.get(name)
                    self.data.append(func)
                    self.ip += 1

                case I.PUSH_ARGS(args):
                    self.data.append('ARGS_BEGIN')
                    self.ip += 1

                case I.LOAD_ARGS():
                    # handle error of invalid no of args
                    eval_args=[]
                    while(self.data[-1]!='ARGS_BEGIN'):
                        eval_args.append(self.data.pop())
                    args_begin=self.data.pop()

                    func=self.data.pop()
                    func_args=func.args
                    eval_args.reverse()
                    if(len(eval_args)!=len(func_args)):
                        raise InvalidProgram("Invalid no of arguments")
                    for i in range(len(eval_args)):
                        self.program_env.add(func_args[i],eval_args[i])

                    self.data.append(func)

                    self.ip += 1

                # case I.EXEC_BODY():
                #
                #     program_env_copy=Environment()
                #     program_env_copy.envs=self.program_env.envs.copy()
                #
                #     func=self.data.pop()
                #
                #     body=func.body
                #     rtr_value=None
                #     try:
                #         codegen(body)
                #         rtr_value=None
                #         print("successful")
                #     except Exception as e:
                #         val=e.args[0]
                #         print(e)
                #         print("type of val is", type(val))
                #         rtr_value=val
                #     print("return value is ", rtr_value)
                #     self.data.append(rtr_value)
                #     self.program_env=program_env_copy
                #     self.ip += 1

                case I.RETURN():

                    rtr_value=self.data.pop()
                    self.data.append(rtr_value)
                    self.ip = self.call_frame[-1].caller.target




                case I.CREATE_FRAME(caller):

                    callee=self.data.pop()
                    self.call_frame.append(CallFrame(caller,callee))
                    self.ip += 1
                case I.DESTROY_FRAME():
                    self.call_frame.pop()
                    self.ip += 1
                case I.STORE_LABEL(name, label):
                    self.label_dict[name] = label
                    self.ip += 1

                case I.LOAD_LABEL(name):
                    self.data.append(self.label_dict[name])

                    self.ip += 1

                case I.JMP_TO_FUNC(name):
                    self.ip = self.label_dict[name].target




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
        "*": I.MUL(),
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
                
                code.emit(I.ENTER_SCOPE())
                codegen_(elif_.if_body)
                code.emit(I.JMP(label2))
                
                code.emit(I.EXIT_SCOPE())
                code.emit_label(label1)
                
                labels.append(label2)

            code.emit(I.ENTER_SCOPE())
            codegen_(else_body)
            code.emit(I.EXIT_SCOPE())
            for label in labels:
                code.emit_label(label)
                
        case While(condition, body):
            label1 = code.label()
            label2 = code.label()
            code.emit_label(label1)
            code.emit(I.ENTER_SCOPE())
            codegen_(condition)
            
            code.emit(I.JMP_IF_FALSE(label2))
            
            
            codegen_(body)
            
            
            code.emit(I.JMP(label1))
            code.emit_label(label2)
            code.emit(I.EXIT_SCOPE())
            
        case For(exp1, condition, exp2, body):
            label1 = code.label()
            label2 = code.label()
            # label3 = code.label()
            codegen_(exp1)
            code.emit_label(label1)
            codegen_(condition)
            code.emit(I.JMP_IF_FALSE(label2))
            # Enter scope
            code.emit(I.ENTER_SCOPE())
            
            codegen_(body)
            # Exit scope
            codegen_(exp2)
            
            code.emit(I.JMP(label1))
            
            code.emit_label(label2)
            code.emit(I.EXIT_SCOPE())

        case Function(Identifier(name), args, body):
            code.emit(I.MAKE_FUNC(Identifier(name), args, body))
            func_label = code.label()
            func_start = code.label()
            code.emit(I.STORE_LABEL(name, func_start))
            code.emit(I.JMP(func_label))
            code.emit_label(func_start)

            codegen_(body)
            code.emit_label(func_label)



        case FunctionCall(Identifier(name), args):
            # enter scope
            code.emit(I.GET_FUNC(Identifier(name)))
            code.emit(I.ENTER_SCOPE())
            func_call_end= code.label()
            code.emit(I.LOAD_LABEL(name))
            code.emit(I.CREATE_FRAME(func_call_end))
            code.emit(I.PUSH_ARGS(args))
            code.emit(I.LOAD_ARGS())
            code.emit(I.JMP_TO_FUNC(name))
            code.emit(I.EXIT_SCOPE())
            code.emit_label(func_call_end)


        case Return(val):

            codegen_(val)
            code.emit(I.RETURN())


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
            BinOp(NumLiteral(4), '%', NumLiteral(2))
        ]
    )
    code = codegen(program)
    print_bytecode(code)

# test_codegen()

def test_vm():



    body = Sequence([Return(StringLiteral("hello"))])
    func = Function(Identifier("test"), [], body)

    func_call = FunctionCall(Identifier("test"), [])
    program2=Sequence(
        [
            func,
            Assign((Identifier("a"),), (func_call,)),
        ]
    )
    code = codegen(program2)
    print_bytecode(code)
    vm = VM()
    vm.load(code)
    vm.execute()



    # body = Sequence([Return(NumLiteral(5)), Print(StringLiteral("Hello World"))])
    # func = Function(Identifier("test"), [], body)
    #
    # func_call = FunctionCall(Identifier("test"), [])
    #
    # program3=Sequence(
    #     [
    #         func,
    #         Assign((Identifier("a"),), (func_call,)),
    #     ]
    # )
    # code = codegen(program3)
    # print_bytecode(code)
    # vm = VM()
    # vm.load(code)
    # vm.execute()

    # program4=Sequence(
    #     [
    #         Function(Identifier("hello"), [], Sequence([ Return(StringLiteral("Hello")) ])),
    # ])
    # code = codegen(program4)
    # print_bytecode(code)
    # vm = VM()
    # vm.load(code)
    # vm.execute()


    # c = ComparisonOp(Identifier('i'), '<', NumLiteral(2))
    #
    # if_branch = Sequence([Return(NumLiteral(1))])
    # elif_list = []
    #
    # f_call = FunctionCall(Identifier("test"), [BinOp(Identifier('i'), '-', NumLiteral(1))])
    # fact = BinOp(Identifier('i'), '*', f_call)
    # else_branch = Sequence([Return(fact)])
    # body = IfElse(c, if_branch, elif_list, else_branch)
    # func = Function(Identifier("test"), [Identifier('i')], Sequence([body]))
    #
    # func_call = FunctionCall(Identifier("test"), [NumLiteral(4)])
    # program5=Sequence(
    #     [
    #         func,
    #         Assign((Identifier("a"),), (func_call,)),
    #     ]
    # )
    # code = codegen(program5)
    # print_bytecode(code)
    # vm = VM()
    # vm.load(code)
    # vm.execute()




# test_vm()
