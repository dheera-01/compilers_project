from dataclasses import dataclass
from typing import Union, Mapping
from declaration import *
from parser_1 import *


global_env = {}


def eval_literals(literal: Value) -> Value_literal:
    match literal:
        case NumLiteral(value):
            return value
        
        case FloatLiteral(value):
            return value

        case StringLiteral(value):
            return value

        case BoolLiteral(Value):
            return Value
        
        # This is a case for list literal
        case _ :
            ans = []
            for x in literal:
                ans.append(eval_literals(x))
            return ans
        

def eval(program: AST, program_env:Environment = None) -> Value:
    global global_env
    # if environment is None:
    #     environment = {}
    if program_env is None:
        display_output.clear()
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
        
        
        case Identifier(name):
            return program_env.get(name)

        case Let(assign, e2):
            eval(assign, program_env)

            # try:
            #     program_env.update(identifier, v1)
            # except:
            #
            #     program_env.add(identifier, v1)

            program_env.enter_scope()
            e2_val = eval(e2, program_env)
            
            program_env.exit_scope()
            return e2_val
        
        case Assign(identifier, right):
            value = eval(right, program_env)
            # for env in reversed(program_env.envs):
            #     if identifier.name in env:
            #         program_env.update(identifier, value)
            #         return None
            program_env.add(identifier, value)
            return None
        case Update(identifier, op, right):
            value = eval(right, program_env)
            if op._operator == "=":
                program_env.update(identifier, value)
            else:# op is +=, -=, *=, /=, %=, **= (binop of first to second last char)
                v = eval(BinOp(identifier, op._operator[: len(op._operator) -1], right), program_env)
                program_env.update(identifier, v)
            return None 
        case Print(value):
            # The print function will print the evaluated value of val and return the AST val
            if isinstance(val, NumLiteral) or isinstance(val, StringLiteral) or isinstance(val, BinOp) or isinstance(val, BoolLiteral):
                # print(f"----------------------------------------")
                ans = eval_literals(eval(val, program_env))
                print(ans)
                display_output.append(str(ans))
                # print(eval_literals(eval(val, program_env)))
                # print(f"----------------------------------------")
                return None
            elif (isinstance(val, Identifier)):
                # print("value is", val)
                print(eval_literals(eval(val, program_env)))
                return None
            else:
                raise InvalidProgram(f"SyntaxError: invalid syntax for print")

        # case BoolLiteral(tf):
        #     if tf == "True":
        #         return BoolLiteral(True)
        #     elif tf == "False":
        #         return BoolLiteral(False)
        #     raise InvalidProgram()

        case While(cond, body):
            c = eval(cond, program_env)
            while (eval_literals(c) == True) :
                program_env.enter_scope()
                eval(body, program_env )
                program_env.exit_scope()
                c = eval(cond, program_env)
            return None
            
            
            # program_env.enter_scope()
            # c = eval(cond, program_env, environment)
            # # if(c==True):
            # #     eval(body)
            # #     eval(While(cond,body))
            # body_iteration_lst = []
            # while (eval_literals(c) == True):
            #     body_iteration_lst.append(eval(body, program_env, environment))
            #     c = eval(cond, program_env, environment)
            # # while loop cannot be implemented recursively as max recursion depth of python restricts it
            # program_env.exit_scope()
            # return body_iteration_lst

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
                raise InvalidProgram(f"TypeError: slice indices must be NumLiteral")

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
                raise InvalidProgram(f"TypeError: - not supported between instances of {x}")

        case UnaryOp("+", x):
            try:
                return eval(BinOp(NumLiteral(1), "*", x), program_env)
            except Exception as e:
                raise InvalidProgram(f"TypeError: + not supported between instances of {x}")

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
                raise InvalidProgram(f"+ not supported between instances of {left} and {right}")

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
                return FloatLiteral(res)
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

        # case Seq(lst):
        #     for expr in lst:
        #         eval(expr, program_env, environment)
        #     return None

        case Assign(identifier, right):
            # print(right)
            if(type(right) == list):
                # print("Yes, its a list")
                for env in reversed(program_env.envs):
                    if identifier.name in env:
                        program_env.update(identifier, right)
                        return None
                program_env.add(identifier, right)
            else:
                # print("Its a variable")
                value = eval(right, program_env, environment)
                for env in reversed(program_env.envs):
                    if identifier.name in env:
                        program_env.update(identifier, value)
                        return None

                program_env.add(identifier, value)
            return None
        
        case Indexer(identifier, indexVal):
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
            
        case Boolify(e):
            return bool(eval(e, program_env,environment))

    raise InvalidProgram(f"SyntaxError: {program} invalid syntax")
        
if __name__ == "__main__":
    file = open("program.txt", "r")
    program = file.read()
    parsed_output = Parser.from_lexer(Lexer.from_stream(Stream.from_string(program))).parse_program()
    print(f"Parsed Output\n{parsed_output}")
    eval(parsed_output)
    file.close()