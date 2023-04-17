# Functions 

### Functions Definition

Functions consists of a name, a list of arguments and a body. The body is a sequence of statements.
There is not need to mention a explicit return statement. If not return statement is found, the function will return `None`.

```python
@dataclass
class Function:
    name: Identifier
    args: list[Identifier]
    body: Sequence

    def __repr__(self) -> str:
        return f"Function({self.name}({self.args}) )"
```

To evaluate a defination of function we just add the function to current scope and return `None`.

```python
case Function(name, args, body):
    program_env.add(name, Function(name, args, body))
    return None
```

### Function Call

Function call consists namely two components the name of the function and a list of arguments. The arguments are evaluated and then the function is called with the evaluated arguments.

```python
@dataclass
class FunctionCall:
    name: Identifier
    args: list['AST']

    def __repr__(self) -> str:
        return f"FunctionCall({self.name}({self.args}))"
```

Here we can see that to evaluate a function call we first evaluate the arguments and then assign them to corresponding identifiers. Then we evaluate the body of the function and return the result.
There could be multiple return statements in the body of the function. If we reach any of return statement and the we need to stop the further evalaution of the body for that we raise a Expection and catch that in the FunctiionCall.

```python
        case FunctionCall(function, args):
            program_env_copy=Environment()
            program_env_copy.envs=program_env.envs.copy()

            func=program_env.get(function.name)
            func_args=func.args

            evaled_args=[]
            for i in range(len(args)):
                evaled_args.append(eval(args[i],program_env))

            program_env.enter_scope()

            if(len(func_args)!=len(args)):
                raise InvalidProgram(f"TypeError: {function.name}() takes {len(func_args)} positional arguments but {len(args)} were given")
            
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

            program_env.exit_scope()
            program_env.restore(program_env_copy.envs)

            return rtr_value
```

But raising an expection will led to some scopes not closed properly. Hence once a return value is found we change program env to its value before function call.

### Return Statement

```python
@dataclass
class Return:
    val: 'AST'

    def __repr__(self) -> str:
        return f"Return({self.val})"
```

```python
        case Return(val):
            raise Exception(eval(val,program_env))
```

### Parsing Function

To parse the function definition we using the `func` keyword. 
```python
    def parse_func(self):
        """parse the function expression
        """
        self.lexer.match(Keyword("func"))
        func_name,args = self.parse_atom(is_func=True)

        body = self.parse_block()

        return Function(func_name, args, body)
```

Some changes were needed in parse_atom to parse function definition and function call as name of function is tokenized as a identifier. 
Here we can see that difference between function definition and function call in parse_atom is made by passing a boolean variable `is_func` to parse_atom. If `is_func` is true then we are parsing a function definition else we are parsing a function call.

```python
                    case Bracket("("):
                        self.lexer.advance()   

                        # this code logically clashes with custom datatype construct
                        args = []
                        while self.lexer.peek_current_token() != Bracket(")"):
                            args.append(self.parse_simple())
                            if self.lexer.peek_current_token() == Operator(","):
                                self.lexer.advance()
                        self.lexer.match(Bracket(")"))
                        if is_func:
                            return (Identifier(name), args)
                        return FunctionCall(Identifier(name), args)   
```

