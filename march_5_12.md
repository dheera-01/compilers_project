# Sequential Let Statments 

Parser for let statement is implemented. The following examples will help to understand the systax and use of let statements. Let statments will return whatever value written in the parenthesis.
1)
```commandline
let x=1+2*3 (x+1) ;
print(x);
```

Output: 7


2) Nested Let statements 
```
assign v=let u=2
(
    let t=2
        (let a=2(u+ a*t))
);
print(v);
```

Output: 6 

# Variable Scoping

Varibale scoping is now itegrated in the parser. Scope will be created and destroyed wheever enter and exit while loop, for loop, if and else blocks. The following examples will help to understand the scoping of variables.
Currently we have implemented scoping by using a stack. Whenever a new scope is created a new entry is pushed in the stack. Whenever a scope is destroyed the top entry is popped from the stack. 
1. This example will work perfectly fine as the y is only called inside its scope. 
```
assign x=1;
while(x<10)
{
    assign x=x+1;
    assign y=x;
    print(y);
};
```

Output: 2 3 4 5 6 7 8 9 10

2. The following code will throw an error as the variable y is called outside its scope. 

```commandline
assign x=1;
while(x<10)
{
    assign x=x+1;
    assign y=x;
};
print(y);
```

Output: Error: KeyError()

# Performance comparison of our languauge with python 
To know how slow our language is when compared to python we wrote two programs in both the languages. Both this program do logically same thing. 
For measuring time taken by program we have used the time module of pyhton. 
### While loop with 1000 iterations
Pyhton Code:
```python
i=0
 while(i<1000):
    print(i)
    i=i+1
```

Our Language Code:
```python
assign i=0;
while(i<1000)
{
    print(i);
    i=i+1;
}
```
The following table shows code and mean time taken over 3 iterations. 

| Language     | Mean Time Taken (ms) |
|--------------|----------------------|
| Python       | 27.24                |
| Our Language | 116.38               |

# Functions 

To use functions in our langauge we need two essential things. First is the function definition and second is the function call. 
Functions mainly consists of four components.
1. Function name
2. Function parameters
3. Function body
4. Return value

Return value could be None as well (for void functions). As our langauge is dynamically typed we do not need to specify the type of the return value.
The following is the declaration of a function in our language. 
```python
@dataclass
class Function:
    name: str
    args:List[Identifier]
    body:'AST'
    return_value: 'AST'
    '''
    Function class takes in a name, list of arguments, body and return value
    return value could be none if it should not return anything (void functions)
    '''
    def __init__(self, name: str, args: List[Identifier], body : 'AST', return_value:'AST') -> None:
        self.name = name
        self.args = args
        self.body = body
        self.return_value = return_value

```

The following is the function call in our language. 
```python
@dataclass
class FunctionCall:
    function_name: str
    args: List['AST']
    def __init__(self, function_name, args) -> None:
        self.function_name=function_name
        self.args=args
    def __repr__(self) -> str:
        return f"FunctionCall({self.function_name}({self.args}))"
```

## Function Scoping
As we are calling functions using functions name, we need to keep track name of function with its definition. To do so we have added functions to the environment, with key as function name and value as function definition. 
Hence whenever is functions is defined it is added to the environment with add_function method.
Whenever a function is called it is fetched from the environment using get_function method.

The folllowing code shows how function and function call are evaluated. 
```python
case FunctionCall(name, args):
    program_env.enter_scope()
    func=program_env.get_function(name)
    if(len(args)!=len(func.args)):
        raise InvalidProgram("Unexpected number of arguments")
    else:
        for i in range(len(args)):
            program_env.add(func.args[i],eval(args[i]))

    rtr=eval(func,program_env)
    program_env.exit_scope()
    return rtr

case Function(name,args , body,return_value):

    eval(body,program_env)
    if(return_value==None):
        return None
    rtr= eval(return_value, program_env)
```

add_function and get_function methods:

```python
def add_function(self,function:Function)->None:
    '''
    Adds function to the environment
    :param function: Function
    :return: None
    '''
    curr_env = self.envs[-1]
    if function.name in curr_env:
        raise InvalidProgram(f"Variable {function.name} already defined")
        return

    self.envs[-1][function.name] = function

def get_function(self,name:str):
    for env in reversed(self.envs):
        if name in env:
            return env[name]
    raise KeyError(f"Function {name} not defined")
```

## Function Parameters

For assigning the argument values to the parameters we iterate over the parameters and assign the value of the argument to the parameter. 
If the number of arguments and parameters do not match we throw an error.

Example:
```python
env=Environment()
addition=Function(name="addition",args=[Identifier("a"),Identifier("b")],body=Sequence([]),return_value=BinOp(Identifier("a"),"+",Identifier("b")))
env.add_function(addition)
addition_call=FunctionCall("addition",[NumLiteral(4),NumLiteral(5)])
print(eval(addition_call,env)) 
```

Output:
```python
9
```


Parser for function definition and function call is not yet implemented. In the next week we will implement the parser for function definition and function call.