from dataclasses import dataclass
from typing import Union, Mapping
from declaration import *
from my_parser import *
from my_lexer import *
from declaration import *
import copy


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
                if type(right[i]).__name__ == 'list':
                    program_env.add(ident, right[i])
                else:
                    # print("Right value", right[i])
                    value = eval(right[i], program_env)
                    # print("Value is", value)
                    program_env.add(ident, value)
            return None
        
        case Update(identifier, op, right):
            # if type(right).__name__ == 'list':
            #     program_env.update(identifier, right)
            #     return None

            value = eval(right, program_env)
            if op._operator == "=":
                program_env.update(identifier, value)
            else:# op is +=, -=, *=, /=, %=, **= (binop of first to second last char)
                v = eval(BinOp(identifier, op._operator[: len(op._operator) -1], right), program_env)
                program_env.update(identifier, v)
            return None 
        
        case Print(value):
            # The print function will print the evaluated value of val and return the AST val
            val = eval(value, program_env)
            # print(f"val: {val}")
            if isinstance(val, NumLiteral) or isinstance(val, StringLiteral)  or isinstance(val, Identifier) or isinstance(val, BoolLiteral) or isinstance(val, FloatLiteral) or isinstance(val, ListLiteral) or isinstance(val, Struct):
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
                eval(body, program_env )
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
                eval(if_ast, program_env)
                program_env.exit_scope()
                return None
            
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
                eval(else_ast, program_env)
                program_env.exit_scope()
                return None
            
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

        case Indexer(identifier, indexVal):
            if(type(indexVal) == Identifier):
                i = eval_literals(eval(program_env.get(indexVal.name)))
            else:
                i = eval_literals(indexVal)
                
            objectToBeIndexed = eval_literals(program_env.get(identifier.name))
            if(len(objectToBeIndexed) <= i):
                print("Index out of range")
            for env in reversed(program_env.envs):
                if identifier.name in env:
                    if(type(program_env.get(identifier.name)) == list):
                        return program_env.get(identifier.name)[i]
                    elif(type(program_env.get(identifier.name)) == StringLiteral):
                        res = eval_literals(program_env.get(identifier.name))[i]
                        return StringLiteral(res)        
                    else:
                        print(f"The Indentifier {identifier} is not iterable")
                        return None
        case ListOperations(identifier, val, item, indVal):
            # print(val)
            # print(item)
            # print(len(program_env.get(identifier.name)))
            if(val == "LEN"):
                a = NumLiteral(len(program_env.get(identifier.name)))
                return a
            elif (val == "HEAD"):
                a = NumLiteral(program_env.get(identifier.name)[0])
                return eval_literals(a)
            elif (val == "TAIL"):
                a = NumLiteral(program_env.get(identifier.name)[len(program_env.get(identifier.name))-1])
                return eval_literals(a)
            elif (val == "APPEND"):
                a = program_env.get(identifier.name)
                a.append(item)
                return a
            elif (val == "POP"):
                a = program_env.get(identifier.name)
                a.pop()
                return a
            elif (val == "ChangeOneElement"):
                a = program_env.get(identifier.name)    
                a[eval_literals(indVal)] = item
            return None


    raise InvalidProgram(f"SyntaxError: {program} invalid syntax")


def eval_of_text(program: str):
    display_output.clear()
    parsed_object = Parser.from_lexer(Lexer.from_stream(Stream.from_string(program)))
    parsed_output = parsed_object.parse_program()
    eval(parsed_output)


if __name__ == "__main__":
    file = open("program.txt", "r")
    program = file.read()
    eval_of_text(program)
    file.close()