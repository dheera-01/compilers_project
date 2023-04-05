from my_parser import *

def typeerror(message: str) -> None:
    raise Exception(message)

def typecheck(program: AST) -> Value:
    match program:
        case Sequence(statements):
            for statement in statements:
                typecheck(statement)
            return None

        case NumLiteral(value):
            return program

        case FloatLiteral(value):
            return program

        case StringLiteral(value):
            return program

        case BoolLiteral(value):
            return program

        # IMP: Identifier is assumed to be of correct type further in the program
        case Identifier(name):
            return Identifier(name)

        case Let(variable as v, value as val, e2):
            e1 = typecheck(Assign((v,), (val,)))
            e2_val = typecheck(e2)

            return e2_val

        case Assign(identifier, right):
            for i, ident in enumerate(identifier):
                if type(right[i]).__name__ != 'list':
                    value = typecheck(right[i])
            return None

        case Update(identifier, op, right):
            if type(right).__name__ == 'list':
                return None

            value = typecheck(right)
            return None

        case Print(value):
            val = typecheck(value)
            return None

        case While(cond, body):
            c = typecheck(cond)
            b = typecheck(body)
            return None

        case For(exp1, condition, exp2, body):
            exp1 = typecheck(exp1)
            cond = typecheck(condition)
            body = typecheck(body)
            exp2 = typecheck(exp2)
            return None

        case Slice(string_var, start, end, step):
            string_var = typecheck(string_var)
            start = typecheck(start)
            end = typecheck(end)
            step = typecheck(step)

            if isinstance(string_var, Identifier):
                string_var = StringLiteral("")

            if isinstance(start, Identifier):
                start = NumLiteral(0)

            if isinstance(end, Identifier):
                end = NumLiteral(0)

            if isinstance(step, Identifier):
                step = NumLiteral(0)

            if not isinstance(string_var, StringLiteral):
                return typeerror(f"Slice operand must be a string")

            if not isinstance(start, NumLiteral):
                return typeerror(f"Slice start index must be a number")

            if not isinstance(end, NumLiteral):
                return typeerror(f"Slice end index must be a number")

            if not isinstance(step, NumLiteral):
                return typeerror(f"Slice step index must be a number")

            return StringLiteral("") # return type is string

        case IfElse(condition_ast, if_ast, elif_list, else_ast):
            condition_res = typecheck(condition_ast)

            if isinstance(condition_res, Identifier):
                condition_res = BoolLiteral(True)

            if not isinstance(condition_res, BoolLiteral):
                return typeerror(f"TypeError: {condition_res} is not a boolean")

            typecheck(if_ast)

            if len(elif_list) != 0:
                for elif_ast in elif_list:
                    elif_condition = typecheck(elif_ast.condition)

                    if isinstance(elif_condition, Identifier):
                        elif_condition = BoolLiteral(True)

                    if not isinstance(elif_condition, BoolLiteral):
                        return typeerror(f"TypeError: {elif_condition} is not a boolean")

                    typecheck(elif_ast.if_body)

            if else_ast != None:
                typecheck(else_ast)

        # comparison operation
        case ComparisonOp(left, op, right) if op in ["<", ">", "==", "!=", "<=", ">=", "and", "or"]:
            left = typecheck(left)
            right = typecheck(right)

            if isinstance(left, Identifier) or isinstance(right, Identifier):
                left = NumLiteral(0)
                right = NumLiteral(0)

            if type(left).__name__ == type(right).__name__: # same type
                return BoolLiteral(True)
            else:
                return typeerror(f"TypeError: {op} not supported between instances of {left} and {right}")

        # unary operation
        case UnaryOp(op, x) if op in ["-", "+"]:
            x = typecheck(x)

            if isinstance(x, Identifier):
                x = NumLiteral(0)

            if not isinstance(x, NumLiteral) and not isinstance(x, FloatLiteral):
                return typeerror(f"TypeError: {op} not supported for instances of {x}")

            if isinstance(x, FloatLiteral):
                return FloatLiteral(0.0)
            else:
                return NumLiteral(0)

        # binary operation
        case BinOp(left, "+", right):
            typecheck_left = typecheck(left)
            typecheck_right = typecheck(right)

            if isinstance(typecheck_left, Identifier):
                typecheck_left = NumLiteral(0)

            if isinstance(typecheck_right, Identifier):
                typecheck_right = NumLiteral(0)

            if isinstance(typecheck_left, StringLiteral) and isinstance(typecheck_right, StringLiteral):
                return StringLiteral("")
            elif isinstance(typecheck_left, StringLiteral) and isinstance(typecheck_right, NumLiteral):
                return StringLiteral("")
            elif isinstance(typecheck_left, NumLiteral) and isinstance(typecheck_right, StringLiteral):
                return StringLiteral("")
            elif isinstance(typecheck_left, NumLiteral) and isinstance(typecheck_right, NumLiteral):
                return NumLiteral(0)
            elif isinstance(typecheck_left, FloatLiteral) and isinstance(typecheck_right, FloatLiteral):
                return FloatLiteral(0.0)
            elif isinstance(typecheck_left, FloatLiteral) and isinstance(typecheck_right, NumLiteral):
                return FloatLiteral(0.0)
            elif isinstance(typecheck_left, NumLiteral) and isinstance(typecheck_right, FloatLiteral):
                return FloatLiteral(0.0)
            else:
                return typeerror(f"TypeError: + not supported between instances of {left} and {right}")

        case BinOp(left, "-", right):
            typecheck_left = typecheck(left)
            typecheck_right = typecheck(right)

            if isinstance(typecheck_left, Identifier):
                typecheck_left = NumLiteral(0)

            if isinstance(typecheck_right, Identifier):
                typecheck_right = NumLiteral(0)

            if isinstance(typecheck_left, NumLiteral) and isinstance(typecheck_right, NumLiteral):
                return NumLiteral(0)
            elif isinstance(typecheck_left, FloatLiteral) and isinstance(typecheck_right, FloatLiteral):
                return FloatLiteral(0.0)
            elif isinstance(typecheck_left, FloatLiteral) and isinstance(typecheck_right, NumLiteral):
                return FloatLiteral(0.0)
            elif isinstance(typecheck_left, NumLiteral) and isinstance(typecheck_right, FloatLiteral):
                return FloatLiteral(0.0)
            else:
                return typeerror(f"TypeError: - not supported between instances of {left} and {right}")

        case BinOp(left, "*", right):
            typecheck_left = typecheck(left)
            typecheck_right = typecheck(right)

            if isinstance(typecheck_left, Identifier):
                typecheck_left = NumLiteral(0)

            if isinstance(typecheck_right, Identifier):
                typecheck_right = NumLiteral(0)

            if isinstance(typecheck_left, StringLiteral) and isinstance(typecheck_right, NumLiteral):
                return StringLiteral("")
            elif isinstance(typecheck_left, NumLiteral) and isinstance(typecheck_right, NumLiteral):
                return NumLiteral(0)
            elif isinstance(typecheck_left, FloatLiteral) and isinstance(typecheck_right, FloatLiteral):
                return FloatLiteral(0.0)
            elif isinstance(typecheck_left, FloatLiteral) and isinstance(typecheck_right, NumLiteral):
                return FloatLiteral(0.0)
            elif isinstance(typecheck_left, NumLiteral) and isinstance(typecheck_right, FloatLiteral):
                return FloatLiteral(0.0)
            else:
                return typeerror(f"TypeError: * not supported between instances of {left} and {right}")

        case BinOp(left, op, right) if op in ["/", "//", "%"]:
            typecheck_left = typecheck(left)
            typecheck_right = typecheck(right)

            if isinstance(typecheck_left, Identifier):
                typecheck_left = NumLiteral(0)

            if isinstance(typecheck_right, Identifier):
                typecheck_right = NumLiteral(0)

            if (isinstance(typecheck_left, NumLiteral) or isinstance(typecheck_left, FloatLiteral)) and (isinstance(typecheck_right, NumLiteral) or isinstance(typecheck_right, FloatLiteral)):
                if op == "/":
                    return FloatLiteral(0.0)
                else:
                    return NumLiteral(1)
            else:
                return typeerror(f"TypeError: / not supported between instances of {left} and {right}")

        case BinOp(left, "**", right):
            typecheck_left = typecheck(left)
            typecheck_right = typecheck(right)

            return NumLiteral(0)
            #TODO: return according to coercion rules

        case Indexer(identifier, indexVal):
            ch = typecheck(indexVal)
            if isinstance(ch, Identifier):
                ch = NumLiteral(0)

            if not isinstance(ch, NumLiteral):
                return typeerror(f"TypeError: {indexVal} is not an integer")
            return typecheck(identifier)

    raise InvalidProgram(f"SyntaxError: {program} invalid syntax")

if __name__ == "__main__":
    file = open("program.txt", "r")
    program = file.read()
    parsed_output = Parser.from_lexer(Lexer.from_stream(Stream.from_string(program))).parse_program()
    print(f"Parsed Output\n{parsed_output}")
    typecheck(parsed_output)
    file.close()