from dataclasses import dataclass
from typing import Union, Mapping
from declaration import *

Value = str | BinOp | float | bool | None | int

global_env = {}

global_env = {}


def eval(program: AST, program_env, environment: Mapping[str, Value] = None) -> Value:
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
            return value

        case FloatLiteral(value):
            return value

        case StringLiteral(value):
            return value

        case Identifier(name):
            return program_env.get(name)

        case Let(Identifier(name), e1, e2):
            v1 = eval(e1, program_env, environment)
            global_env[name] = v1
            return eval(e2, program_env, environment | {name: v1})

        case Print(val):
            # The print function will print the evaluated value of val and return the AST val
            if isinstance(val, NumLiteral) or isinstance(val, StringLiteral) or isinstance(val, BinOp) or isinstance(
                    val, Identifier):
                print(eval(val, program_env))
                return val
            else:
                raise InvalidProgram()

        case BoolLiteral(tf):
            if (tf == "True"):
                return True
            elif (tf == "False"):
                return False
            raise InvalidProgram()

        # case Assign(left, right):
        #     right_val = eval(right, environment)
        #     global_env[left.name] = right_val
        #     return None

        case While(cond, body):

            c = eval(cond, program_env, environment)
            # if(c==True):
            #     eval(body)
            #     eval(While(cond,body))
            body_iteration_lst = []
            while (c == True):
                body_iteration_lst.append(eval(body, program_env, environment))
                c = eval(cond, program_env, environment)
            # while loop cannot be implemented recursively as max recursion depth of python restricts it
            return body_iteration_lst

        case For(exp1, condition, exp2, body):
            eval(exp1, program_env, environment)
            cond = eval(condition, program_env, environment)
            body_iteration_lst = []
            if (cond == True):
                temp = (eval(body, program_env, environment))
                temp.append(eval(exp2, program_env, environment))
                body.statements.append(exp2)
                body_iteration_lst = (eval(While(condition, body), program_env))
                body_iteration_lst.insert(0, temp)
            return body_iteration_lst

        case Slice(string_var, start, end, step):
            # How are handling the case a[1:] and its other variants

            string_var = eval(string_var, program_env, environment)
            start = eval(start, program_env, environment)
            end = eval(end, program_env, environment)
            step = eval(step, program_env, environment)
            if isinstance(string_var, str) and isinstance(start, int) and isinstance(end, int) and isinstance(step,
                                                                                                              int):
                return string_var[int(start):int(end):int(step)]
            else:
                raise InvalidProgram(
                    f"TypeError: slice indices must be NumLiteral")

        case IfElse(condition_ast, if_ast, else_ast):
            condition_res = eval(condition_ast, program_env, environment)
            # print(f"The condition result {condition_res}")
            if condition_res == True:
                # print(f"Inside the if of IfElse")
                return eval(if_ast, program_env, environment)
            else:
                # print('Inside else of IfElse')
                return eval(else_ast, program_env, environment)

        # comparison operation
        case ComparisonOp(x, ">", const):
            try:
                if eval(x, program_env, environment) > eval(const, program_env, environment):
                    return True
                return False
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: > not supported between instances of {x} and {const}")

        case ComparisonOp(x, "<", const):
            try:
                if eval(x, program_env, environment) < eval(const, program_env, environment):
                    return True
                return False
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: < not supported between instances of {x} and {const}")

        case ComparisonOp(x, "==", const):
            try:
                if eval(x, program_env, environment) == eval(const, program_env, environment):
                    return True
                return False
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: == not supported between instances of {x} and {const}")

        case ComparisonOp(x, "!=", const):
            try:
                if eval(x, program_env, environment) != eval(const, program_env, environment):
                    return True
                return False
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: != not supported between instances of {x} and {const}")

        case ComparisonOp(x, "<=", const):
            try:
                if eval(x, program_env, environment) <= eval(const, program_env, environment):
                    return True
                return False
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: <= not supported between instances of {x} and {const}")

        case ComparisonOp(x, ">=", const):
            try:
                if eval(x, program_env, environment) >= eval(const, program_env, environment):
                    return True
                return False
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: >= not supported between instances of {x} and {const}")

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
            eval_left = eval(left, program_env, environment)
            eval_right = eval(right, program_env, environment)
            try:
                if isinstance(eval_left, str) and isinstance(eval_right, int) or isinstance(eval_left,
                                                                                            int) and isinstance(
                        eval_right, str):
                    return str(eval_left) + str(eval_right)
                else:
                    return eval_left + eval_right
            except Exception as e:
                # raise TypeError(f"+ not supported between instances of {type(eval_left).__name__} and {type(eval_right).__name__}")
                raise InvalidProgram(
                    f"+ not supported between instances of {left} and {right}")

        case BinOp(left, "-", right):
            eval_left = eval(left, program_env, environment)
            eval_right = eval(right, program_env, environment)
            try:
                return eval_left - eval_right
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: - not supported between instances of {left} and {right}")

        case BinOp(left, "*", right):
            eval_left = eval(left, program_env, environment)
            eval_right = eval(right, program_env, environment)
            try:
                return eval_left * eval_right
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: ** not supported between instances of {left} and {right}")

        case BinOp(left, "/", right):
            eval_left = eval(left, program_env, environment)
            eval_right = eval(right, program_env, environment)
            try:
                return eval_left / eval_right
            except ZeroDivisionError as e:
                raise InvalidProgram(f"ZeroDivisionError: division by zero")
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: / not supported between instances of {left} and {right}")

        case BinOp(left, "//", right):
            eval_left = eval(left, program_env, environment)
            eval_right = eval(right, program_env, environment)
            try:
                return eval_left // eval_right
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
                return eval_left % eval_right
            except ZeroDivisionError as e:
                raise InvalidProgram(f"ZeroDivisionError: modulo by zero")
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: % not supported between instances of {left} and {right}")

        case BinOp(left, "**", right):
            eval_left = eval(left, program_env, environment)
            eval_right = eval(right, program_env, environment)
            try:
                return eval_left ** eval_right
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: ** not supported between instances of {left} and {right}")
        case Seq(lst):
            for expr in lst:
                eval(expr, program_env, environment)
            return None

        case While_Seq(cond, body):

            c = eval(cond, program_env, environment)

            while (c == True):
                eval(body, program_env, environment)
                c = eval(cond, program_env, environment)
            # while loop cannot be implemented recursivly as max recursion depth of python restricts it
            return None

        # case While(cond, body):
        #     c = eval(cond, environment)
        #     # if(c==True):
        #     #     eval(body)
        #     #     eval(While(cond,body))
        #     while (c == True):
        #         eval(body, environment)
        #         c = eval(cond, environment)
        #     # while loop cannot be implemented recursivly as max recursion depth of python restricts it
        #     return None

        case For(exp1, condition, exp2, Seq(lst)):
            eval(exp1)
            cond = eval(condition, program_env)
            if (cond == True):
                eval(Seq(lst), program_env)
                eval(exp2, program_env)
                lst.append(exp2)
                eval(While_Seq(condition, Seq(lst)), program_env)
            return None

        # case Assign(identifier, right):
        #     value = eval(right, program_env, environment)
        #     curr_env = program_env.envs[-1]
        #     if identifier.name in curr_env:
        #         program_env.update(identifier, value)
        #     else:
        #         program_env.add(identifier, value)
        #     return None
        case Assign(left, right):
        
            curr_env = program_env.envs[-1]
            if isinstance(left, tuple):  # check if left-hand side is a tuple
    
                value = [eval(i, program_env, environment) for i in right]
       
                for i, identifier in enumerate(left):
                    if identifier.name in curr_env:
                        program_env.update(identifier, value[i])
                    else:
                        program_env.add(identifier, value[i])
        
                return None
        
            else:  # left-hand side is a single identifier
        
       
                value = eval(right, program_env, environment)
        
                if left.name in curr_env:
                    program_env.update(left, value)
                else:
                    program_env.add(left, value)
                return None
    raise InvalidProgram(f"SyntaxError: {program} invalid syntax")
