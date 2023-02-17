from dataclasses import dataclass


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
    var: 'AST'
    e1: 'AST'
    e2: 'AST'

    def __repr__(self) -> str:
        return f"Let({self.var} = {self.e1} in {self.e2})"


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
    lst : ['AST']

@dataclass
class While():

    condn: ComparisonOp
    body: 'AST'




@dataclass
class Assign:
    v:Identifier
    right:'AST'

@dataclass
class For:
    exp1: Assign
    condition:ComparisonOp
    exp2:'AST'
    body : Seq
@dataclass
class IfElse:
    condition: ComparisonOp
    if_body: "AST"
    else_body: "AST"

    def __repr__(self) -> str:
        return f"IfElse({self.condition} then {self.if_body} else {self.else_body})"


AST = NumLiteral | BinOp | Let | StringLiteral | Slice  | ComparisonOp | Identifier | IfElse | Seq | Assign
