from dataclasses import dataclass, field
from typing import List


# datatype for AST
@dataclass
class Sequence:
    statements: list(["AST"])
    
    def __repr__(self) -> str:
        return f"Sequence({self.statements})"


@dataclass
class NumLiteral:
    value: int
    
    def __repr__(self) -> str:
        return f"NumLiteral({self.value})"


# Define a StringLiteral class for testing in test_print
@dataclass
class StringLiteral:
    value: str

    def __repr__(self) -> str:
        return f"StringLiteral(\"{self.value}\")"


@dataclass
class FloatLiteral:
    value: float

    def __repr__(self) -> str:
        return f"FloatLiteral({self.value})"


@dataclass
class BoolLiteral:
    value: bool

    def __repr__(self) -> str:
        return f"BoolLiteral({self.value})"


@dataclass
class Keyword:
    value: str

    def __repr__(self) -> str:
        return f"Keyword({self.value})"


@dataclass
class Identifier:
    name: str
    is_mutable: bool = True
    first_assign = []

    def __repr__(self) -> str:
        return f"Identifier({self.name})"


@dataclass
class Operator:
    _operator: str

    def __repr__(self) -> str:
        return f"Operator({self._operator})"


@dataclass
class Bracket:
    _bracket: str

    def __repr__(self) -> str:
        return f"Bracket({self._bracket})"


@dataclass
class Comments:
    _comment: str

    def __repr__(self) -> str:
        return f"Comments({self._comment})"


@dataclass
class EndOfLine:
    _eol: str

    def __repr__(self) -> str:
        return f"EndOfLine({self._eol})"


@dataclass
class EndOfFile:
    _eof: str

    def __repr__(self) -> str:
        return f"EndOfFile({self._eof})"


@dataclass
class BinOp:
    left: 'AST'
    operator: str
    right: 'AST'

    def __repr__(self) -> str:
        return f"BinOp({self.left} {self.operator} {self.right})"

@dataclass
class UnaryOp:
    operator: str
    operand: 'AST'

    def __repr__(self) -> str:
        return f"UnaryOp({self.operator}, {self.operand})"

@dataclass
class ComparisonOp:
    left: 'AST'
    operator: str  # >,<
    right: 'AST'

    def __repr__(self) -> str:
        return f"ComparisonOp({self.left} {self.operator} {self.right})"

@dataclass
class Let:
    assign: 'AST'
    e2: 'AST'

    def __repr__(self) -> str:
        return f"Let({self.assign} in {self.e2})"


@dataclass
class Print:
    val: 'AST'

    def __repr__(self) -> str:
        return f"Print({self.val})"


@dataclass
class Slice:
    string_var: 'AST'
    start: 'AST'
    end: 'AST'
    step: 'AST'

    def __repr__(self) -> str:
        return f"Slice({self.string_var}[{self.start}:{self.end}:{self.step}])"


@dataclass
class IfElse:
    condition: ComparisonOp
    if_body: Sequence
    elif_body: list(["AST"])
    else_body: Sequence

    def __init__(self, cond, if_, elif_ = [], else_ = None) -> None:
        self.condition = cond
        self.if_body = if_
        self.elif_body = elif_
        self.else_body = else_    
    
    def __repr__(self) -> str:
        return f"\nIfElse\n{self.condition}\n{self.if_body}\n{self.elif_body}\n{self.else_body})"

@dataclass
class While():

    condition: 'AST'
    body: 'AST'
    
    def __repr__(self) -> str:
        return f"While({self.condition} do {self.body})"
    
@dataclass
class Assign:
    v: "AST" # for parallel let assign a,b = 1,2
    right:'AST'
    
    def __repr__(self) -> str:
        return f"Assign({self.v} = {self.right})"


@dataclass
class Update:
    variable: "AST"
    _operator: Operator # +=, -=, *= etc are all valid assignment operators
    right: "AST"
    
    def __repr__(self) -> str:
        return f"Update({self.variable} {self._operator} {self.right})"



@dataclass
class For:
    exp1: 'AST'
    condition:'AST'
    exp2:'AST'
    body : Sequence
    
    def __repr__(self) -> str:
        return f"For(({self.exp1} ;{self.condition};{self.exp2}) do {self.body})"


# @dataclass
# class Seq:
#     lst : list['AST']

# @dataclass
# class While_Seq():

#     condn: ComparisonOp
#     body: 'AST'





# error classes
class InvalidProgram(Exception):
    pass

class KeyError(Exception):
    pass

class EndOfLineError(Exception):
    pass



#defining environment class for storing variables and their values in a dictionary 
@dataclass
class Environment:
    envs : List[dict] # environments are stored in a list of dictionaries
    
    def __init__(self):
        self.envs=[{}]

    def enter_scope(self):
        """Enter a new scope
        """
        self.envs.append({})

    def exit_scope(self):
        """Exit the current scope
        """
        
        assert self.envs
        self.envs.pop()

    def add(self, identifier, value):
        """Add a new variable to the current scope

        Args:
            identifier (Identifier): the variable to add
            value (Value): the value of the variable

        Raises:
            InvalidProgram: if the variable is already defined in the current scope
        """
        
        curr_env = self.envs[-1]
        if identifier.name in curr_env:
            raise InvalidProgram(f"Variable {identifier.name} already defined")
            return
        self.envs[-1][identifier.name] = [value, identifier]

    def update(self, identifier: Identifier, value):
        """Update the value of a variable in the current scope

        Args:
            identifier (Identifier): the variable to update
            value (Value): the new value of the variable to update

        Raises:
            InvalidProgram: if the variable is immutable and trying to update it
            KeyError: if the variable is not defined in any scope
        """
        for env in reversed(self.envs):
            if identifier.name in env:
                if env[identifier.name][-1].is_mutable:
                    if type(identifier.first_assign[0]).__name__ != type(value).__name__:
                        raise InvalidProgram(
                            f"TypeError: Cannot assign {type(value).__name__} to a Identifier of type {type(identifier.first_assign[0]).__name__}")

                    env[identifier.name] = [value, identifier]
                else:
                    raise InvalidProgram(f"Variable {identifier.name} is immutable")
                return
        raise KeyError(f"Variable {identifier.name} not defined")

    def get(self, name: str):
        """Get the value of a variable

        Args:
            name (str): the variable to get

        Raises:
            KeyError: if the variable is not defined in any scope

        Returns:
            Value: the value of the variable
        """
        for env in reversed(self.envs):
            if name in env:
                return env[name][0]
        raise KeyError(f"Variable {name} not defined")

display_output = [] # list to store the output of print statements as strings

Value_literal = int | float | bool | str
Value = None | NumLiteral | StringLiteral | BoolLiteral | FloatLiteral

AST = Value | Identifier | Sequence | BinOp | ComparisonOp | UnaryOp | Let | Assign| Update | IfElse | While | For | Print | Keyword | Operator | Bracket | Comments | EndOfLine | EndOfFile


