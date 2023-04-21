from dataclasses import dataclass
from declaration import *
from my_debugger_parser import *
from my_lexer import *
import copy
import sys


def ReturnException(value: Value):
    return value


struct_instance = []

@dataclass
class Debugger:
    program_env: Environment = Environment()
    
    def user_command(self, line_number) -> None:
        print(f"PC-> {line_number}: {source_code[line_number]}")
        while True:
            command = input("(Karma Debugger) ").split()
            try: 
                cmd = command[0]
                if cmd == "n" or cmd == "next": # next
                    return None
                elif cmd == "q" or cmd == "quit": # quit
                    sys.exit()
                elif cmd == "p" or cmd == "print": # print the environment
                    if len(command) == 1:
                        print(f"{self.program_env}")
                    else:
                        print(f"{self.program_env.get(command[1])}")
                elif cmd == "c" or cmd == "current": # current line
                    print(f"PC-> {line_number}: {source_code[line_number]}")
                else:
                    print(f"Invalid command: {command[0]}")
            except Exception as e:
                print(f"Invalid command: {command}")
    
    
    def eval_literals(self, literal: Value) -> Value_literal:
        match literal:
            case NumLiteral(value):
                return value
            
            case FloatLiteral(value):
                return value

            case StringLiteral(value):
                return value

            case BoolLiteral(value):
                return value
            
            case ListLiteral(value):
                ans = []
                for x in value:
                    ans.append(eval_literals(x))
                return ans
            case Struct(name, fields) as s:
                ans = Struct(name, fields)
                ans.name = name
                ans.fields = []
                for i, filed in enumerate(fields):
                    temp = []
                    temp.append(s.fields[i][0].name)
                    temp.append(eval_literals(s.fields[i][1]))
                    ans.fields.append(temp)
                return ans


    def eval(self, program: AST) -> Value:
        
        match program:
            case Sequence(statements):
                for statement in statements:                        
                    self.user_command(statement.line_number)
                    if(isinstance(statement,Return)):
                        e=self.eval(statement)
                        return e
                    else:
                        self.eval(statement)
                return None

            case NumLiteral(value):
                # print(program)
                return program

            case FloatLiteral(value):
                return program

            case StringLiteral(value):
                return program

            case BoolLiteral(value):
                return program
            
            case ListLiteral(value):
                for i, x in enumerate(value):
                    value[i] = self.eval(x)
                return program
            
            case Identifier(name):
                return self.program_env.get(name)

            case Struct(name, fields):
                # print(f"\nInside eval struct: {program}")
                if name not in user_defined_data_types:
                    user_defined_data_types[name] = Struct(name, fields)
                    # print(f"user defined datatype: \n{user_defined_data_types}")
                    return None
                struct_object = copy.deepcopy(user_defined_data_types[name])
                for i in range(len(fields)):
                    struct_object.fields[i][1] = fields[i][1]
                return struct_object
            
            
            case Assign(identifier, right):
                for i, ident in enumerate(identifier):
                    value = self.eval(right[i])
                    if isinstance(value, Struct):
                        struct_instance.append(ident)     
                    self.program_env.add(ident, value)
                return None
            
            case Update(identifier, op, right):
                value = self.eval(right)
                if op._operator == "=":
                    self.program_env.update(identifier, value)
                else:# op is +=, -=, *=, /=, %=, **= (binop of first to second last char)
                    v = self.eval(BinOp(identifier, op._operator[: len(op._operator) -1], right))
                    self.program_env.update(identifier, v)
                return None 
            
            case Print(value):
                val = self.eval(value)
                if isinstance(val, NumLiteral) or isinstance(val, StringLiteral)  or isinstance(val, Identifier) or isinstance(val, BoolLiteral) or isinstance(val, FloatLiteral) or isinstance(val, ListLiteral) or isinstance(val, Struct) or  val is None:
                    ans = self.eval_literals(val)
                    print(f"{ans}")
                    display_output.append(str(ans))
                    return None
                else:
                    raise InvalidProgram(f"SyntaxError: invalid syntax for print")

            case While(cond, body):
                c = self.eval(cond)
                while (self.eval_literals(c) == True) :
                    self.program_env.enter_scope()
                    self.eval(body)
                    self.program_env.exit_scope()
                    c = self.eval(cond)
                return None
                

            case For(exp1, condition, exp2, body):
                self.program_env.enter_scope()
                self.eval(exp1)                
                cond=self.eval(condition)
                while(cond==BoolLiteral(True)):
                    self.program_env.enter_scope()
                    self.eval(body)
                    self.user_command(exp1.line_number)
                    self.eval(exp2)
                    cond=self.eval(condition)
                    self.program_env.exit_scope()

                self.program_env.exit_scope()
                return None
                

            case Slice(string_var, start, end, step):
                string_var = self.eval(string_var)
                start = self.eval(start)
                end = self.eval(end)
                step = self.eval(step)
                if isinstance(string_var, StringLiteral) and isinstance(start, NumLiteral) and isinstance(end, NumLiteral) and isinstance(step,NumLiteral):
                    string_var = self.eval_literals(string_var)
                    start = self.eval_literals(start)
                    end = self.eval_literals(end)
                    step = self.eval_literals(step)
                    res = string_var[start:end:step]
                    return StringLiteral(res)
                else:
                    raise InvalidProgram(
                        f"TypeError: slice indices must be NumLiteral")

            case IfElse(condition_ast, if_ast, elif_list ,else_ast):
                condition_res = self.eval(condition_ast)
                if self.eval_literals(condition_res) == True:
                    # print(f"Inside the if of IfElse")
                    self.program_env.enter_scope()
                    rtr_value=self.eval(if_ast)
                    self.program_env.exit_scope()
                    return rtr_value
                
                if len(elif_list) != 0:
                    for elif_ast in elif_list:
                        elif_condition = self.eval(elif_ast.condition)
                        self.user_command(elif_ast.line_number)
                        if self.eval_literals(elif_condition) == True:
                            self.program_env.enter_scope()
                            self.eval(elif_ast.if_body)
                            self.program_env.exit_scope()
                            return None
                
                if else_ast != None:
                    # print('Inside else of IfElse')
                    self.program_env.enter_scope()
                    rtr_value=self.eval(else_ast)
                    self.program_env.exit_scope()
                    return rtr_value
                
                return None

            # comparison operation
            case ComparisonOp(x, ">", const):
                try:
                    if self.eval_literals(self.eval(x)) > self.eval_literals(self.eval(const)):
                        return BoolLiteral(True)
                    return BoolLiteral(False)
                except Exception as e:
                    raise InvalidProgram(
                        f"TypeError: > not supported between instances of {x} and {const}")

            case ComparisonOp(x, "<", const):
                try:
                    if self.eval_literals(self.eval(x)) < self.eval_literals(self.eval(const)):
                        return BoolLiteral(True)
                    return BoolLiteral(False)
                except Exception as e:
                    raise InvalidProgram(
                        f"TypeError: < not supported between instances of {x} and {const}")

            case ComparisonOp(x, "==", const):
                try:
                    if self.eval_literals(self.eval(x)) == self.eval_literals(self.eval(const)):
                        return BoolLiteral(True)
                    return BoolLiteral(False)
                except Exception as e:
                    raise InvalidProgram(
                        f"TypeError: == not supported between instances of {x} and {const}")

            case ComparisonOp(x, "!=", const):
                try:
                    if self.eval_literals(self.eval(x)) != self.eval_literals(self.eval(const)):
                        return BoolLiteral(True)
                    return BoolLiteral(False)
                except Exception as e:
                    raise InvalidProgram(
                        f"TypeError: != not supported between instances of {x} and {const}")

            case ComparisonOp(x, "<=", const):
                try:
                    if self.eval_literals(self.eval(x)) <= self.eval_literals(self.eval(const)):
                        return BoolLiteral(True)
                    return BoolLiteral(False)
                except Exception as e:
                    raise InvalidProgram(
                        f"TypeError: <= not supported between instances of {x} and {const}")

            case ComparisonOp(x, ">=", const):
                try:
                    if self.eval_literals(self.eval(x)) >= self.eval_literals(self.eval(const)):
                        return BoolLiteral(True)
                    return BoolLiteral(False)
                except Exception as e:
                    raise InvalidProgram(
                        f"TypeError: >= not supported between instances of {x} and {const}")
            
            case ComparisonOp(cond1, "and", cond2):
                try:
                    if self.eval_literals(self.eval(cond1)) and self.eval_literals(self.eval(cond2)):
                        return BoolLiteral(True)
                    return BoolLiteral(False)
                except Exception as e:
                    raise InvalidProgram(
                        f"TypeError: and not supported between instances of {cond1} and {cond2}")
            
            case ComparisonOp(cond1, "or", cond2):
                try:
                    if self.eval_literals(self.eval(cond1)) or self.eval_literals(self.eval(cond2)):
                        return BoolLiteral(True)
                    return BoolLiteral(False)
                except Exception as e:
                    raise InvalidProgram(
                        f"TypeError: or not supported between instances of {cond1} and {cond2}")

            # unary operation
            case UnaryOp("-", x):
                try:
                    return self.eval(BinOp(NumLiteral(-1), "*", x))
                except Exception as e:
                    raise InvalidProgram(
                        f"TypeError: - not supported between instances of {x}")

            case UnaryOp("+", x):
                try:
                    return self.eval(BinOp(NumLiteral(1), "*", x))
                except Exception as e:
                    raise InvalidProgram(
                        f"TypeError: + not supported between instances of {x}")

            # binary operation
            case BinOp(left, "+", right):
                eval_left = self.eval(left)
                eval_right = self.eval(right)

                try:
                    if isinstance(eval_left, StringLiteral) or isinstance(eval_right, StringLiteral):
                        res = str(self.eval_literals(eval_left)) + str(self.eval_literals(eval_right))
                        return StringLiteral(res)
                    else:
                        res = self.eval_literals(eval_left) + self.eval_literals(eval_right)
                        if isinstance(eval_left, FloatLiteral) or isinstance(eval_right, FloatLiteral):
                            return FloatLiteral(res)
                        else:
                            return NumLiteral(res)
                except Exception as e:
                    # raise TypeError(f"+ not supported between instances of {type(eval_left).__name__} and {type(eval_right).__name__}")
                    raise InvalidProgram(
                        f"+ not supported between instances of {left} and {right}")

            case BinOp(left, "-", right):
                eval_left = self.eval(left)
                eval_right = self.eval(right)
                try:
                    res = self.eval_literals(eval_left) - self.eval_literals(eval_right)
                    if isinstance(eval_left, FloatLiteral) or isinstance(eval_right, FloatLiteral):
                        return FloatLiteral(res)
                    else:
                        return NumLiteral(res)
                except Exception as e:
                    raise InvalidProgram(f"TypeError: - not supported between instances of {left} and {right}")

            case BinOp(left, "*", right):
                eval_left = self.eval(left)
                eval_right = self.eval(right)
                try:
                    res = self.eval_literals(eval_left) * self.eval_literals(eval_right)
                    if isinstance(eval_left, StringLiteral) and isinstance(eval_right, NumLiteral):
                        return StringLiteral(res)
                    elif isinstance(eval_left, FloatLiteral) or isinstance(eval_right, FloatLiteral):
                        return FloatLiteral(res)
                    else:
                        return NumLiteral(res)
                except Exception as e:
                    raise InvalidProgram(f"TypeError: * not supported between instances of {left} and {right}")

            case BinOp(left, "/", right):
                eval_left = eval(left)
                eval_right = eval(right)
                try:
                    res = eval_literals(eval_left) / eval_literals(eval_right)
                    return FloatLiteral(res)
                except ZeroDivisionError as e:
                    raise InvalidProgram(f"ZeroDivisionError: division by zero")
                except Exception as e:
                    raise InvalidProgram(
                        f"TypeError: / not supported between instances of {left} and {right}")

            case BinOp(left, "//", right):
                eval_left = self.eval(left)
                eval_right = self.eval(right)
                try:
                    res = self.eval_literals(eval_left) // self.eval_literals(eval_right)
                    return NumLiteral(res)
                except ZeroDivisionError as e:
                    raise InvalidProgram(
                        f"ZeroDivisionError: floor division by zero")
                except Exception as e:
                    raise InvalidProgram(
                        f"TypeError: // not supported between instances of {left} and {right}")

            case BinOp(left, "%", right):
                eval_left = self.eval(left)
                eval_right = self.eval(right)
                try:
                    res = self.eval_literals(eval_left) % self.eval_literals(eval_right)
                    return NumLiteral(res)
                except ZeroDivisionError as e:
                    raise InvalidProgram(f"ZeroDivisionError: modulo by zero")
                except Exception as e:
                    raise InvalidProgram(
                        f"TypeError: % not supported between instances of {left} and {right}")

            case BinOp(left, "**", right):
                eval_left = self.eval(left)
                eval_right = self.eval(right)
                try:
                    res = self.eval_literals(eval_left) ** self.eval_literals(eval_right)
                    return NumLiteral(res)
                except Exception as e:
                    raise InvalidProgram(
                        f"TypeError: ** not supported between instances of {left} and {right}")

            case Indexer(identifier, indexVal):
                # print(f"identifier: {identifier}, indexVal: {indexVal}")
                # print(f'user defined dat {user_defined_data_types}')
                if identifier in struct_instance:
                    i = indexVal
                else:
                    i = eval_literals(eval(indexVal))
                # if not isinstance(indexVal, Identifier):
                #     i = eval_literals(eval(indexVal))
                # else:
                #     i = indexVal
                objectToBeIndexed = eval(self.program_env.get(identifier.name))
                
                if isinstance( objectToBeIndexed, Struct):
                    return objectToBeIndexed.get(i)

                if(len(objectToBeIndexed.value) <= i):
                    raise InvalidProgram(f"Index out of range")
                if isinstance(objectToBeIndexed, ListLiteral):
                    return objectToBeIndexed.value[i]
                if isinstance(objectToBeIndexed, StringLiteral):
                    return StringLiteral(objectToBeIndexed.value[i]) 
                raise InvalidProgram(f"TypeError: {identifier} is not iterable")
                
                

            case ListOperations(identifier, val, item, indVal):

                if(val == "LEN"):
                    listLit = self.program_env.get(identifier.name)
                    lis = listLit.value
                    a = NumLiteral(len(lis))
                    return a
                elif (val == "HEAD"):
                    listLit = self.program_env.get(identifier.name)
                    l = listLit.value
                    return l[0]
                elif (val == "TAIL"):
                    listLit = self.program_env.get(identifier.name)
                    lis = listLit.value
                    return lis[len(lis)-1]
                elif (val == "APPEND"):
                    a = self.program_env.get(identifier.name)
                    if(isinstance(a, ListLiteral)):
                        a = a.value
                    a.append(item)
                    a = self.program_env.get(identifier.name)
                    return a
                elif (val == "POP"):
                    a = self.program_env.get(identifier.name)
                    if(isinstance(a, ListLiteral)):
                        a = a.value
                    elem = a.pop()
                    
                    return elem
                elif (val == "ChangeOneElement"):
                    a = self.program_env.get(identifier.name)    
                    if(isinstance(a, ListLiteral)):
                        a = a.value
                    a[eval_literals(eval(indVal))] = eval(item)
                return None


            case FunctionCall(function, args):
                self.program_env_copy=Environment()
                self.program_env_copy.envs=self.program_env.envs.copy()

                func=self.program_env.get(function.name)
                func_args=func.args
                # print("function args are ",func_args[0])

                evaled_args=[]
                for i in range(len(args)):
                    evaled_args.append(eval(args[i],self.program_env))


                self.program_env.enter_scope()

                if(len(func_args)!=len(args)):
                    raise InvalidProgram(f"TypeError: {function.name}() takes {len(func_args)} positional arguments but {len(args)} were given")
                for i in range(len(func_args)):

                    self.program_env.add(func_args[i],evaled_args[i])

                rtr_value = None

                try:
                    eval(func.body,self.program_env)
                    rtr_value=None

                except Exception as e:
                    rtr_value=None
                    if(isinstance(rtr_value,AST)):
                        rtr_value = e.args[0]

                    else:
                        print(e)


                # fibo works when we exit scope twice why?
                self.program_env.exit_scope()


                self.program_env.restore(self.program_env_copy.envs)

                return rtr_value

            case Return(val):

                raise Exception(eval(val,self.program_env))

            case Function(name, args, body):
                self.program_env.add(name, Function(name, args, body))
                # add program evironment with function keep track of args
                # initialize args with None
                # replace them while function call
                return None
            
        raise InvalidProgram(f"SyntaxError: {program} invalid syntax")


def eval_of_text(program: str):
    display_output.clear()
    parsed_object = Parser.from_lexer(Lexer.from_stream(Stream.from_string(program)))
    parsed_output = parsed_object.parse_program()
    debug = Debugger()
    debug.eval(parsed_output)

def eval_of_file(file_name: str):
    file = open(file_name, "r")
    program = file.read()
    eval_of_text(program)
    file.close()

if __name__ == "__main__":
    eval_of_file("program.txt")