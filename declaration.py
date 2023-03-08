from dataclasses import dataclass
from typing import List


@dataclass
class Sequence:
    statements: ["AST"]
    
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

    def __repr__(self) -> str:
        return f"Identifier({self.name})"


@dataclass
class Operator:
    _operator: str

    def __repr__(self) -> str:
        return f"Operator({self._operator})"


@dataclass
class BinOp:
    left: 'AST'
    operator: str
    right: 'AST'

    def __repr__(self) -> str:
        return f"BinOp({self.left}, {self.operator}, {self.right})"


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
class UnaryOp:
    operator: str
    operand: 'AST'

    def __repr__(self) -> str:
        return f"UnaryOp({self.operator}, {self.operand})"


@dataclass
class Let:
    assign: 'AST'
    e2: 'AST'

    def __repr__(self) -> str:
        return f"Let({self.assign} {self.e2})"


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
class ComparisonOp:
    left: 'AST'
    operand: str  # >,<
    right: 'AST'

    def __repr__(self) -> str:
        return f"ComparisonOp({self.left} {self.operand} {self.right})"

@dataclass
class Seq:
    lst : list['AST']

@dataclass
class While_Seq():

    condn: ComparisonOp
    body: 'AST'

# @dataclass
# class While():
#
#     condn: ComparisonOp
#     body: 'AST'

@dataclass
class Assign:
    v:Identifier
    right:'AST'

# @dataclass
# class For:
#     exp1: Assign
#     condition:ComparisonOp
#     exp2:'AST'
#     body : Seq

@dataclass
class IfElse:
    condition: ComparisonOp
    if_body: Sequence
    else_body: Sequence

    def __repr__(self) -> str:
        return f"IfElse({self.condition} then {self.if_body} else {self.else_body})"

@dataclass
class While():

    condn: 'AST'
    body: 'AST'
    
    def __repr__(self) -> str:
        return f"While({self.condn} do {self.body})"
    
@dataclass
class Assign:
    v:Identifier
    right:'AST'
    
    def __repr__(self) -> str:
        return f"Assign({self.v} = {self.right})"

@dataclass
class For:
    exp1: 'AST'
    condition:'AST'
    exp2:'AST'
    body : Sequence
    
    def __repr__(self) -> str:
        return f"For(({self.exp1} ;{self.condition};{self.exp2}) do {self.body})"

class InvalidProgram(Exception):
    pass

@dataclass
class Enviroment:
    envs : List[dict]

    def __init__(self):
        self.envs=[{}]

    def enter_scope(self):
        self.envs.append({})

    def exit_scope(self):
        assert self.envs
        self.envs.pop()

    # value here is also a Literal
    def add(self, identifier, value):
        curr_env = self.envs[-1]
        if identifier.name in curr_env:
            raise InvalidProgram(f"Variable {identifier.name} already defined")
            return

        self.envs[-1][identifier.name] = [value, identifier]
        return

    def update(self, identifier:Identifier, value):
        for env in reversed(self.envs):
            if identifier.name in env:
                if env[identifier.name][-1].is_mutable:
                    env[identifier.name] = [value, identifier]

                else:
                    raise InvalidProgram(f"Variable {identifier.name} is immutable")
                return
        raise InvalidProgram(f"Variable {identifier.name} is not defined")

    def get(self, name):
        for env in reversed(self.envs):
            if name in env:

                return env[name][0]
        raise InvalidProgram(f"Variable {name} is not defined")

AST = NumLiteral | BinOp | Let | StringLiteral | Slice | Assign | ComparisonOp | Identifier | IfElse | Sequence | Print | FloatLiteral | BoolLiteral | Keyword | Operator | Bracket | Comments | EndOfLine | EndOfFile | UnaryOp| While
