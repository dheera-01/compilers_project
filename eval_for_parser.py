from dataclasses import dataclass
from typing import Union, Mapping
from declaration import *

Value_literal = int | float | bool | str
Value = None | NumLiteral | StringLiteral | BoolLiteral | FloatLiteral

global_env = {}


def eval_literals(Literal: AST) -> Value_literal:
    match Literal:
        case NumLiteral(value):
            return value

        case FloatLiteral(value):
            return value

        case StringLiteral(value):
            return value

        case BoolLiteral(Value):
            return Value
        

def eval(program: AST, program_env:Enviroment, environment: Mapping[str, Value] = None) -> Value:
    global global_env
    if environment is None:
        environment = {}

    match program:
        case Sequence(statements):
            ans = []
            for statement in statements:
                ans.append(eval(statement, program_env, environment))
            return ans

        case NumLiteral(value):
            return program

        case FloatLiteral(value):
            return program

        case StringLiteral(value):
            return program

        case BoolLiteral(Value):
            return program
        
        case Identifier(name):
            # This will return the Literal stored
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

        case Print(val):
            # The print function will print the evaluated value of val and return the AST val
            if isinstance(val, NumLiteral) or isinstance(val, StringLiteral) or isinstance(val, BinOp) or isinstance(val, Identifier) or isinstance(val, BoolLiteral):
                # print(f"----------------------------------------")
                print(eval_literals(eval(val, program_env)))
                # print(f"----------------------------------------")
                return None
            elif (isinstance(val, Identifier)):
                print(eval(val, program_env))
                return None
            else:
                raise InvalidProgram()

        case BoolLiteral(tf):
            if tf == "True":
                return BoolLiteral(True)
            elif tf == "False":
                return BoolLiteral(False)
            raise InvalidProgram()

        case While(cond, body):
            program_env.enter_scope()
            c = eval(cond, program_env, environment)
            # if(c==True):
            #     eval(body)
            #     eval(While(cond,body))
            body_iteration_lst = []
            while (eval_literals(c) == True):
                body_iteration_lst.append(eval(body, program_env, environment))
                c = eval(cond, program_env, environment)
            # while loop cannot be implemented recursively as max recursion depth of python restricts it
            program_env.exit_scope()
            return body_iteration_lst

        case For(exp1, condition, exp2, body):
            program_env.enter_scope()
            eval(exp1, program_env, environment)
            cond = eval(condition, program_env, environment)
            body_iteration_lst = []
            if (eval_literals(cond) == True):
                temp = eval(body, program_env, environment)
                temp.append(eval(exp2, program_env, environment))
                body.statements.append(exp2)
                body_iteration_lst = (eval(While(condition, body), program_env))
                body_iteration_lst.insert(0, temp)
            program_env.exit_scope()
            return body_iteration_lst

        case Slice(string_var, start, end, step):
            string_var = eval(string_var, program_env, environment)
            start = eval(start, program_env, environment)
            end = eval(end, program_env, environment)
            step = eval(step, program_env, environment)
            if isinstance(string_var, StringLiteral) and isinstance(start, NumLiteral) and isinstance(end, NumLiteral) and isinstance(step,NumLiteral):
                string_var = eval_literals(string_var)
                start = eval_literals(start)
                end = eval_literals(end)
                step = eval_literals(step)
                res = string_var[start:end:step]
                return StringLiteral(res)
            else:
                raise InvalidProgram(f"TypeError: slice indices must be NumLiteral")

        case IfElse(condition_ast, if_ast, else_ast):
            condition_res = eval(condition_ast, program_env, environment)
            # print(f"The condition result {condition_res}")
            if eval_literals(condition_res) == True:
                # print(f"Inside the if of IfElse")
                program_env.enter_scope()
                rtr= eval(if_ast, program_env, environment)
                program_env.exit_scope()
                return rtr
            else:
                # print('Inside else of IfElse')
                program_env.enter_scope()
                rtr= eval(else_ast, program_env, environment)
                program_env.exit_scope()
                return rtr

        # comparison operation
        case ComparisonOp(x, ">", const):
            try:
                if eval_literals(eval(x, program_env, environment)) > eval_literals(eval(const, program_env, environment)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: > not supported between instances of {x} and {const}")

        case ComparisonOp(x, "<", const):
            try:
                if eval_literals(eval(x, program_env, environment)) < eval_literals(eval(const, program_env, environment)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: < not supported between instances of {x} and {const}")

        case ComparisonOp(x, "==", const):
            try:
                if eval_literals(eval(x, program_env, environment)) == eval_literals(eval(const, program_env, environment)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: == not supported between instances of {x} and {const}")

        case ComparisonOp(x, "!=", const):
            try:
                if eval_literals(eval(x, program_env, environment)) != eval_literals(eval(const, program_env, environment)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: != not supported between instances of {x} and {const}")

        case ComparisonOp(x, "<=", const):
            try:
                if eval_literals(eval(x, program_env, environment)) <= eval_literals(eval(const, program_env, environment)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: <= not supported between instances of {x} and {const}")

        case ComparisonOp(x, ">=", const):
            try:
                if eval_literals(eval(x, program_env, environment)) >= eval_literals(eval(const, program_env, environment)):
                    return BoolLiteral(True)
                return BoolLiteral(False)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: >= not supported between instances of {x} and {const}")

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
            eval_left = eval(left, program_env, environment)
            eval_right = eval(right, program_env, environment)

            try:
                if isinstance(eval_left, StringLiteral) and isinstance(eval_right, NumLiteral) or isinstance(eval_left,
                                                                                            NumLiteral) and isinstance(eval_right, StringLiteral):
                    res = str(eval_literals(eval_left)) + str(eval_literals(eval_right))
                    return StringLiteral(res)
                else:
                    res = eval_literals(eval_left) + eval_literals(eval_right)
                    if isinstance(eval_left, StringLiteral) and isinstance(eval_right, StringLiteral):
                        return StringLiteral(res)
                    elif isinstance(eval_left, FloatLiteral) or isinstance(eval_right, FloatLiteral):
                        return FloatLiteral(res)
                    else:
                        return NumLiteral(res)
            except Exception as e:
                raise InvalidProgram(f"+ not supported between instances of {left} and {right}")

        case BinOp(left, "-", right):
            eval_left = eval(left, program_env, environment)
            eval_right = eval(right, program_env, environment)
            try:
                res = eval_literals(eval_left) - eval_literals(eval_right)
                if isinstance(eval_left, FloatLiteral) or isinstance(eval_right, FloatLiteral):
                    return FloatLiteral(res)
                else:
                    return NumLiteral(res)
            except Exception as e:
                raise InvalidProgram(f"TypeError: - not supported between instances of {left} and {right}")

        case BinOp(left, "*", right):
            eval_left = eval(left, program_env, environment)
            eval_right = eval(right, program_env, environment)
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
            eval_left = eval(left, program_env, environment)
            eval_right = eval(right, program_env, environment)
            try:
                res = eval_literals(eval_left) / eval_literals(eval_right)
                return FloatLiteral(res)
            except ZeroDivisionError as e:
                raise InvalidProgram(f"ZeroDivisionError: division by zero")
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: / not supported between instances of {left} and {right}")

        case BinOp(left, "//", right):
            eval_left = eval(left, program_env, environment)
            eval_right = eval(right, program_env, environment)
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
            eval_left = eval(left, program_env, environment)
            eval_right = eval(right, program_env, environment)
            try:
                res = eval_literals(eval_left) % eval_literals(eval_right)
                return FloatLiteral(res)
            except ZeroDivisionError as e:
                raise InvalidProgram(f"ZeroDivisionError: modulo by zero")
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: % not supported between instances of {left} and {right}")

        case BinOp(left, "**", right):
            eval_left = eval(left, program_env, environment)
            eval_right = eval(right, program_env, environment)
            try:
                res = eval_literals(eval_left) % eval_literals(eval_right)
                return NumLiteral(res)
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: ** not supported between instances of {left} and {right}")

        case Seq(lst):
            for expr in lst:
                eval(expr, program_env, environment)
            return None

        case Assign(identifier, right):
            value = eval(right, program_env, environment)
            for env in reversed(program_env.envs):
                if identifier.name in env:
                    program_env.update(identifier, value)
                    return None

            program_env.add(identifier, value)
            return None

    raise InvalidProgram(f"SyntaxError: {program} invalid syntax")
