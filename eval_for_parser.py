from dataclasses import dataclass
from typing import Union, Mapping
from declaration import *
from my_parser import *
from my_lexer import *
from declaration import *
import copy


def ReturnException(value: Value):
    return value


struct_instance = []
def eval_literals(literal: Value) -> Value_literal:
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

            
            
        # # This is a case for list literal
        # case _ :
        #     ans = []
        #     print(f"literal: {literal}")
        #     for x in literal:
        #         ans.append(eval_literals(x))
        #     return ans
        



def eval(program: AST, program_env:Environment = None) -> Value:

    if program_env is None:
        display_output.clear()
        user_defined_data_types.clear()
        program_env = Environment()

    match program:
        case Sequence(statements):
            for statement in statements:
                # print(f"statement: {statement}")
                if(isinstance(statement,Return)):

                    e=eval(statement, program_env)

                    return e
                else:

                    eval(statement, program_env)

            return None
            # print(f"ans: {ans}")
            # ans = []
            # for statement in statements:
            #     # print(f"statement: {statement}")
            #     ans.append(eval(statement, environment))
            # # print(f"ans: {ans}")
            # return ans

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
                value[i] = eval(x, program_env)
            return program
        
        case Identifier(name):
            return program_env.get(name)

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
        
        case Let(variable as v, value as val, e2):  
            program_env.enter_scope()
            eval(Assign((v,), (val,)), program_env)
            program_env.enter_scope()
            e2_val = eval(e2, program_env)
            program_env.exit_scope()
            program_env.exit_scope()
            return e2_val
        
        case Assign(identifier, right):
            for i, ident in enumerate(identifier):
                # if type(right[i]).__name__ == 'list':
                #     program_env.add(ident, right[i])
                # else:
                    # print("Right value", right[i])
                value = eval(right[i], program_env)
                # print(f"i = {i}, ident = {ident}, value = {value}")
                # print("Value is", value)
                if isinstance(value, Struct):
                    struct_instance.append(ident)
                    
                    
                program_env.add(ident, value)
            return None
        
        case Update(identifier, op, right):
            # if type(right).__name__ == 'list':
            #     program_env.update(identifier, right)
            #     return None

            value = eval(right, program_env)
            if op._operator == "=":
                program_env.update(identifier, value)
            else:# op is +=, -=, *= (binop of first to second last char)
                v = eval(BinOp(identifier, op._operator[: len(op._operator) -1], right), program_env)
                program_env.update(identifier, v)
            return None 
        
        case Print(value):
            # The print function will print the evaluated value of val and return the AST val
            val = eval(value, program_env)
            # print(f"val: {val}")
            # print(f"type of val: {type(val)}")
            if isinstance(val, NumLiteral) or isinstance(val, StringLiteral)  or isinstance(val, Identifier) or isinstance(val, BoolLiteral) or isinstance(val, FloatLiteral) or isinstance(val, ListLiteral) or isinstance(val, Struct) or  val is None:
                # print(f"----------------------------------------")
                ans = eval_literals(val)
                print(f"{ans}")
                display_output.append(str(ans))
                # print(eval_literals(eval(val, program_env)))
                # print(f"----------------------------------------")
                return None
            else:
                raise InvalidProgram(f"SyntaxError: invalid syntax for print")

        case While(cond, body):
            c = eval(cond, program_env)
            while (eval_literals(c) == True) :
                program_env.enter_scope()
                eval(body, program_env)
                program_env.exit_scope()
                c = eval(cond, program_env)
            return None
            

        case For(exp1, condition, exp2, body):
            program_env.enter_scope()
            eval(exp1, program_env)
            cond=eval(condition,program_env)

            while(cond==BoolLiteral(True)):
                program_env.enter_scope()
                eval(body,program_env)
                eval(exp2,program_env)
                cond=eval(condition,program_env)
                program_env.exit_scope()

            program_env.exit_scope()
            return None
            
            # program_env.enter_scope()
            # eval(exp1, program_env, environment)
            # cond = eval(condition, program_env, environment)
            # body_iteration_lst = []
            # if (eval_literals(cond) == True):
            #     temp = eval(body, program_env, environment)
            #     temp.append(eval(exp2, program_env, environment))
            #     body.statements.append(exp2)
            #     body_iteration_lst = (eval(While(condition, body), program_env))
            #     body_iteration_lst.insert(0, temp)
            # program_env.exit_scope()
            # return body_iteration_lst

        case Slice(string_var, start, end, step):
            string_var = eval(string_var, program_env)
            start = eval(start, program_env)
            end = eval(end, program_env)
            step = eval(step, program_env)
            if isinstance(string_var, StringLiteral) and isinstance(start, NumLiteral) and isinstance(end, NumLiteral) and isinstance(step,NumLiteral):
                string_var = eval_literals(string_var)
                start = eval_literals(start)
                end = eval_literals(end)
                step = eval_literals(step)
                res = string_var[start:end:step]
                return StringLiteral(res)
            else:
                raise InvalidProgram(
                    f"TypeError: slice indices must be NumLiteral")

        case IfElse(condition_ast, if_ast, elif_list ,else_ast):
            condition_res = eval(condition_ast, program_env)
            # print(f"The condition result {condition_res}")
            if eval_literals(condition_res) == True:
                # print(f"Inside the if of IfElse")
                program_env.enter_scope()
                rtr_value=eval(if_ast, program_env)
                program_env.exit_scope()
                return rtr_value
            
            if len(elif_list) != 0:
                for elif_ast in elif_list:
                    elif_condition = eval(elif_ast.condition, program_env )
                    if eval_literals(elif_condition) == True:
                        program_env.enter_scope()

                        eval(elif_ast.if_body, program_env)
                        program_env.exit_scope()
                        return None
            
            if else_ast != None:
                # print('Inside else of IfElse')
                program_env.enter_scope()
                rtr_value=eval(else_ast, program_env)
                program_env.exit_scope()
                return rtr_value
            
            return None

        # comparison operation
        case ComparisonOp(x, ">", const):
            try:
                if eval_literals(eval(x, program_env)) > eval_literals(eval(const, program_env)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: > not supported between instances of {x} and {const}")

        case ComparisonOp(x, "<", const):
            try:
                if eval_literals(eval(x, program_env)) < eval_literals(eval(const, program_env)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: < not supported between instances of {x} and {const}")

        case ComparisonOp(x, "==", const):
            try:
                if eval_literals(eval(x, program_env)) == eval_literals(eval(const, program_env)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: == not supported between instances of {x} and {const}")

        case ComparisonOp(x, "!=", const):
            try:
                if eval_literals(eval(x, program_env)) != eval_literals(eval(const, program_env)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: != not supported between instances of {x} and {const}")

        case ComparisonOp(x, "<=", const):
            try:
                if eval_literals(eval(x, program_env)) <= eval_literals(eval(const, program_env)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: <= not supported between instances of {x} and {const}")

        case ComparisonOp(x, ">=", const):
            try:
                if eval_literals(eval(x, program_env)) >= eval_literals(eval(const, program_env)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: >= not supported between instances of {x} and {const}")
        
        case ComparisonOp(cond1, "and", cond2):
            try:
                if eval_literals(eval(cond1, program_env)) and eval_literals(eval(cond2, program_env)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: and not supported between instances of {cond1} and {cond2}")
        
        case ComparisonOp(cond1, "or", cond2):
            try:
                if eval_literals(eval(cond1, program_env)) or eval_literals(eval(cond2, program_env)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: or not supported between instances of {cond1} and {cond2}")

        # unary operation
        case UnaryOp("-", x):
            try:
                return eval(BinOp(NumLiteral(-1), "*", x), program_env)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: - not supported between instances of {x}")

        case UnaryOp("+", x):
            try:
                return eval(BinOp(NumLiteral(1), "*", x), program_env)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: + not supported between instances of {x}")

        # binary operation
        case BinOp(left, "+", right):
            eval_left = eval(left, program_env)
            eval_right = eval(right, program_env)

            try:
                if isinstance(eval_left, StringLiteral) or isinstance(eval_right, StringLiteral):
                    res = str(eval_literals(eval_left)) + str(eval_literals(eval_right))
                    return StringLiteral(res)
                else:
                    res = eval_literals(eval_left) + eval_literals(eval_right)
                    if isinstance(eval_left, FloatLiteral) or isinstance(eval_right, FloatLiteral):
                        return FloatLiteral(res)
                    else:
                        return NumLiteral(res)
            except Exception as e:
                # raise TypeError(f"+ not supported between instances of {type(eval_left).__name__} and {type(eval_right).__name__}")
                raise InvalidProgram(
                    f"+ not supported between instances of {left} and {right}")

        case BinOp(left, "-", right):
            eval_left = eval(left, program_env)
            eval_right = eval(right, program_env)
            try:
                res = eval_literals(eval_left) - eval_literals(eval_right)
                if isinstance(eval_left, FloatLiteral) or isinstance(eval_right, FloatLiteral):
                    return FloatLiteral(res)
                else:
                    return NumLiteral(res)
            except Exception as e:
                raise InvalidProgram(f"TypeError: - not supported between instances of {left} and {right}")

        case BinOp(left, "*", right):
            eval_left = eval(left, program_env)
            eval_right = eval(right, program_env)
            try:
                res = eval_literals(eval_left) * eval_literals(eval_right)
                if isinstance(eval_left, StringLiteral) and isinstance(eval_right, NumLiteral):
                    return StringLiteral(res)
                elif isinstance(eval_left, FloatLiteral) or isinstance(eval_right, FloatLiteral):
                    return FloatLiteral(res)
                else:
                    return NumLiteral(res)
            except Exception as e:
                raise InvalidProgram(f"TypeError: * not supported between instances of {left} and {right}")

        case BinOp(left, "/", right):
            eval_left = eval(left, program_env)
            eval_right = eval(right, program_env)
            try:
                res = eval_literals(eval_left) / eval_literals(eval_right)
                return FloatLiteral(res)
            except ZeroDivisionError as e:
                raise InvalidProgram(f"ZeroDivisionError: division by zero")
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: / not supported between instances of {left} and {right}")

        case BinOp(left, "//", right):
            eval_left = eval(left, program_env)
            eval_right = eval(right, program_env)
            try:
                res = eval_literals(eval_left) // eval_literals(eval_right)
                return NumLiteral(res)
            except ZeroDivisionError as e:
                raise InvalidProgram(
                    f"ZeroDivisionError: floor division by zero")
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: // not supported between instances of {left} and {right}")

        case BinOp(left, "%", right):
            eval_left = eval(left, program_env)
            eval_right = eval(right, program_env)
            try:
                res = eval_literals(eval_left) % eval_literals(eval_right)
                return NumLiteral(res)
            except ZeroDivisionError as e:
                raise InvalidProgram(f"ZeroDivisionError: modulo by zero")
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: % not supported between instances of {left} and {right}")

        case BinOp(left, "**", right):
            eval_left = eval(left, program_env)
            eval_right = eval(right, program_env)
            try:
                res = eval_literals(eval_left) ** eval_literals(eval_right)
                return NumLiteral(res)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: ** not supported between instances of {left} and {right}")

        # concatenation operation
        case BinOp(left, "~", right):
            eval_left = eval(left, program_env)
            eval_right = eval(right, program_env)
            try:
                concat_similar_addition = ["StringLiteral", "NumLiteral", "FloatLiteral"]
                if eval_left.__class__.__name__ in concat_similar_addition and eval_right.__class__.__name__ in concat_similar_addition:
                    res = str(eval_literals(eval_left)) + str(eval_literals(eval_right))
                    return StringLiteral(res)
                raise InvalidProgram(
                    f"~ not supported between instances of {eval_left} and {eval_right}")
            except Exception as e:
                raise TypeError(
                    f"+ not supported between instances of {type(eval_left).__name__} and {type(eval_right).__name__}")
                raise InvalidProgram(
                    f"~ not supported between instances of {eval_left} and {eval_right}")

        case Indexer(identifier, indexVal1, indexVal2, indexVal3):
            # print(f"identifier: {identifier}, indexVal: {indexVal}")
            # print(f'user defined dat {user_defined_data_types}')
            if identifier in struct_instance:
                i = indexVal1
            else:
                i = eval_literals(eval(indexVal1, program_env))
                if(indexVal2 != None):
                    j = eval_literals(eval(indexVal2, program_env))
                if(indexVal3 != None):
                    k = eval_literals(eval(indexVal3, program_env))
                
   
            objectToBeIndexed = eval(program_env.get(identifier.name), program_env)
            
            if isinstance( objectToBeIndexed, Struct):
                return objectToBeIndexed.get(i)

            if(len(objectToBeIndexed.value) <= i):
                raise InvalidProgram(f"Index out of range")
            if isinstance(objectToBeIndexed, ListLiteral):
                if(isinstance(objectToBeIndexed.value[i], ListLiteral) and indexVal2 != None):
                    if(len(objectToBeIndexed.value[i].value) <= j):
                        raise InvalidProgram(f"Index out of range")
                    if(isinstance(objectToBeIndexed.value[i].value[j], ListLiteral) and indexVal3 != None):
                        if(len(objectToBeIndexed.value[i].value[j].value) <= k):
                            raise InvalidProgram(f"Index out of range")
                        return objectToBeIndexed.value[i].value[j].value[k]
                    return objectToBeIndexed.value[i].value[j]
                    
                return objectToBeIndexed.value[i]
            if isinstance(objectToBeIndexed, StringLiteral):
                if(isinstance(objectToBeIndexed.value[i], StringLiteral) and indexVal2 != None):
                    if(len(objectToBeIndexed.value[i].value) <= j):
                        raise InvalidProgram(f"Index out of range")
                    if(isinstance(objectToBeIndexed.value[i].value[j], StringLiteral) and indexVal3 != None):
                        if(len(objectToBeIndexed.value[i].value[j].value) <= k):
                            raise InvalidProgram(f"Index out of range")
                        return objectToBeIndexed.value[i].value[j].value[k]
                    return objectToBeIndexed.value[i].value[j]
                return StringLiteral(objectToBeIndexed.value[i]) 
            raise InvalidProgram(f"TypeError: {identifier} is not iterable")
            
        

        case ListOperations(identifier, val, item, indVal):

            if(val == "LEN"):
                listLit = program_env.get(identifier.name)
                lis = listLit.value
                a = NumLiteral(len(lis))
                return a
            elif (val == "HEAD"):
                listLit = program_env.get(identifier.name)
                l = listLit.value
                return l[0]
            elif (val == "TAIL"):
                listLit = program_env.get(identifier.name)
                lis = listLit.value
                return lis[len(lis)-1]
            elif (val == "APPEND"):
                a = program_env.get(identifier.name)
                if(isinstance(a, ListLiteral)):
                    a = a.value
                a.append(eval(item, program_env))
                a = program_env.get(identifier.name)
                return a
            elif (val == "POP"):
                a = program_env.get(identifier.name)
                if(isinstance(a, ListLiteral)):
                    a = a.value
                elem = a.pop()
                
                return elem
            elif (val == "ChangeOneElement"):
                a = program_env.get(identifier.name)    
                if(isinstance(a, ListLiteral)):
                    a = a.value
                a[eval_literals(eval(indVal, program_env))] = eval(item, program_env)
            return None


        case FunctionCall(function, args):
            program_env_copy=Environment()
            program_env_copy.envs=program_env.envs.copy()

            func=program_env.get(function.name)
            func_args=func.args
            # print("function args are ",func_args[0])

            evaled_args=[]
            for i in range(len(args)):
                evaled_args.append(eval(args[i],program_env))


            program_env.enter_scope()

            if(len(func_args)!=len(args)):
                raise InvalidProgram(f": {function.name}() takes {len(func_args)} positional arguments but {len(args)} were given")
            for i in range(len(func_args)):

                program_env.add(func_args[i],evaled_args[i])

            rtr_value = None

            try:
                eval(func.body,program_env)
                rtr_value=None

            except Exception as e:
                rtr_value=None
                if(isinstance(rtr_value,AST)):
                    rtr_value = e.args[0]

                else:
                    print(e)


            # fibo works when we exit scope twice why?
            program_env.exit_scope()


            program_env.restore(program_env_copy.envs)

            return rtr_value

        case Return(val):

            raise Exception(eval(val,program_env))

        case Function(name, args, body):
            program_env.add(name, Function(name, args, body))
            # add program evironment with function keep track of args
            # initialize args with None
            # replace them while function call
            return None

        case Boolify(e):
            return BoolLiteral(bool(eval_literals(eval(e, program_env))))
        
    raise InvalidProgram(f"SyntaxError: {program} invalid syntax")


def eval_of_text(program: str):
    display_output.clear()
    parsed_object = Parser.from_lexer(Lexer.from_stream(Stream.from_string(program)))
    parsed_output = parsed_object.parse_program()
    eval(parsed_output)


if __name__ == "__main__":
    # file = open("ensure_func.txt", "r")
    # file = open("Euler14.txt", "r")
    # file = open("struct.txt", "r")
    file = open("program.txt", "r")
    program = file.read()
    eval_of_text(program)
    file.close()