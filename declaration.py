from dataclasses import dataclass, field
from typing import List


is_line_show = False

# datatype for AST
@dataclass
class Sequence:
    statements: list(["AST"])
    
    def __repr__(self) -> str:
        statement_str = "\n".join([str(statement) for statement in self.statements])
        return f"Sequence begin\n{statement_str}\nend"



@dataclass
class NumLiteral:
    value: int
    line_number: int = 0
    column_number: int = 0
    
    
    # def __repr__(self) -> str:
    #     return f"NumLiteral({self.value}) [{self.line_number}: {self.column_number}]"
    
    def __repr__(self) -> str:
        return f"NumLiteral({self.value})"
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, NumLiteral):
            return self.value == __value.value
        return False


@dataclass
class StringLiteral:
    value: str
    line_number: int = 0
    column_number: int = 0
    
    
    # def __repr__(self) -> str:
    #     return f"StringLiteral(\"{self.value}\") [{self.line_number}: {self.column_number}]"
    
    def __repr__(self) -> str:
        return f"StringLiteral(\"{self.value}\")"
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, StringLiteral):
            return self.value == __value.value
        return False
    


@dataclass
class FloatLiteral:
    value: float
    line_number: int = 0
    column_number: int = 0

    # def __repr__(self) -> str:
    #     return f"FloatLiteral({self.value}) [{self.line_number}: {self.column_number}]"

    def __repr__(self) -> str:
        return f"FloatLiteral({self.value})"
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, FloatLiteral):
            return self.value == __value.value
        return False

@dataclass
class BoolLiteral:
    value: bool
    line_number: int = 0
    column_number: int = 0

    # def __repr__(self) -> str:
    #     return f"BoolLiteral({self.value}) [{self.line_number}: {self.column_number}]"

    def __repr__(self) -> str:
        return f"BoolLiteral({self.value})"
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, BoolLiteral):
            return self.value == __value.value
        return False
    
@dataclass
class ListLiteral:
    value: list
    line_number: int = 0
    column_number: int = 0

    # def __repr__(self) -> str:
    #     return f"ListLiteral({self.value}) [{self.line_number}: {self.column_number}]"
    
    def __repr__(self) -> str:
        return f"ListLiteral({self.value})"
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, ListLiteral):
            return self.value == __value.value
        return False

@dataclass
class Keyword:
    value: str
    line_number: int = 0
    column_number: int = 0

    
    # def __repr__(self) -> str:
    #     return f"Keyword({self.value}) [{self.line_number}: {self.column_number}]"

    def __repr__(self) -> str:
        return f"Keyword({self.value})"
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Keyword):
            return self.value == __value.value
        return False

@dataclass
class Identifier:
    name: str
    is_mutable: bool = True
    line_number: int = 0
    column_number: int = 0

    # def __repr__(self) -> str:
    #     return f"Identifier({self.name}, {self.is_mutable}) [{self.line_number}: {self.column_number}]"
    
    def __repr__(self) -> str:
        return f"Identifier({self.name}, {self.is_mutable})"
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Identifier):
            return self.name == __value.name
        return False


@dataclass
class Operator:
    _operator: str
    line_number: int = 0
    column_number: int = 0

    
    # def __repr__(self) -> str:
    #     return f"Operator({self._operator}) [{self.line_number}: {self.column_number}]"
    
    def __repr__(self) -> str:
        return f"Operator({self._operator})"
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Operator):
            return self._operator == __value._operator
        return False


@dataclass
class Bracket:
    _bracket: str
    line_number: int = 0
    column_number: int = 0
    
    # def __repr__(self) -> str:
    #     return f"Bracket({self._bracket}) [{self.line_number}: {self.column_number}]"

    def __repr__(self) -> str:
        return f"Bracket({self._bracket})"
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Bracket):
            return self._bracket == __value._bracket
        return False


@dataclass
class Comments:
    _comment: str
    line_number: int = 0
    column_number: int = 0

    def __repr__(self) -> str:
        return f"Comments({self._comment})"

    # def __repr__(self) -> str:
    #     return f"Comments({self._comment}) [{self.line_number}: {self.column_number}]"

@dataclass
class EndOfLine:
    _eol: str
    line_number: int = 0
    column_number: int = 0

    
    # def __repr__(self) -> str:
    #     return f"EndOfLine({self._eol}) [{self.line_number}: {self.column_number}]"

    def __repr__(self) -> str:
        return f"EndOfLine({self._eol})"
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, EndOfLine):
            return self._eol == __value._eol
        return False

@dataclass
class EndOfFile:
    _eof: str
    line_number: int = 0
    column_number: int = 0
    
    # def __repr__(self) -> str:
    #     return f"EndOfFile({self._eof}) [{self.line_number}: {self.column_number}]"

    def __repr__(self) -> str:
        return f"EndOfFile({self._eof})"
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, EndOfFile):
            return self._eof == __value._eof
        return False

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
        return f"UnaryOp({self.operator} {self.operand})"

@dataclass
class ComparisonOp:
    left: 'AST'
    operator: str  # >,<
    right: 'AST'

    def __repr__(self) -> str:
        return f"ComparisonOp({self.left} {self.operator} {self.right})"

@dataclass
class Let:
    var: 'AST'
    e1: 'AST'
    e2: 'AST'

    def __repr__(self) -> str:
        return f"Let {self.var} = {self.e1} in {self.e2})"


@dataclass
class Print:
    val: 'AST'
    line_number: int = 0

    # def __repr__(self) -> str:
    #     return f"Print({self.val}) [{self.line_number}]"

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


@dataclass()
class IfElse:
    condition: ComparisonOp
    if_body: Sequence
    elif_body: list(["AST"])
    else_body: Sequence
    line_number: int = 0
    

    # def __init__(self, cond, if_, elif_=[], else_=None) -> None:
    #     self.condition = cond
    #     self.if_body = if_
    #     self.elif_body = elif_
    #     self.else_body = else_

    # def __repr__(self) -> str:
    #     if len(self.elif_body) == 0 and self.else_body == None:
    #         return f"if({self.condition}) then\n{self.if_body} [{self.line_number}]"
    #     if len(self.elif_body) == 0 and self.else_body != None:
    #         return f"if({self.condition}) then\n{self.if_body}\nelse\n{self.else_body} [{self.line_number}]"
    #     if len(self.elif_body) != 0 and self.else_body == None:
    #         elif_string = '\nel'.join(str(e) for e in self.elif_body)
    #         return f"if({self.condition}) then\n{self.if_body}\nel{elif_string}) [{self.line_number}]"
    #     elif_string = '\nel'.join(str(e) for e in self.elif_body)
    #     return f"if({self.condition}) then\n{self.if_body}\nel{elif_string}\nelse\n{self.else_body}) [{self.line_number}]"
    #     # return f"if({self.condition}) then\n{self.if_body}\nelif\n{self.elif_body}\nelse\n{self.else_body})"

    def __repr__(self) -> str:
        if len(self.elif_body) == 0 and self.else_body == None:
            return f"if({self.condition}) then\n{self.if_body}"
        if len(self.elif_body) == 0 and self.else_body != None:
            return f"if({self.condition}) then\n{self.if_body}\nelse\n{self.else_body}"
        if len(self.elif_body) != 0 and self.else_body == None:
            elif_string = '\nel'.join(str(e) for e in self.elif_body)
            return f"if({self.condition}) then\n{self.if_body}\nel{elif_string})"
        elif_string = '\nel'.join(str(e) for e in self.elif_body)
        return f"if({self.condition}) then\n{self.if_body}\nel{elif_string}\nelse\n{self.else_body})"
        # return f"if({self.condition}) then\n{self.if_body}\nelif\n{self.elif_body}\nelse\n{self.else_body})"

@dataclass
class While():

    condition: 'AST'
    body: 'AST'
    line_number: int = 0
    
    def __repr__(self) -> str:
        return f"While({self.condition} do {self.body})"
    
    # def __repr__(self) -> str:
    #     return f"While({self.condition} do {self.body}) [{self.line_number}]"
    

@dataclass
class Assign:
    v: "AST" or list['AST']
    right:'AST' or list['AST'] or list[list['AST']]
    line_number: int = 0
    
    
    # def __repr__(self) -> str:
    #     v_ = self.v
    #     right_ = self.right
    #     # if len(self.v) == 1:
    #     #     v_ = self.v[0]
    #     # if len(self.right) == 1:
    #     #     right_ = self.right[0]
    #
    #     return f"Assign({v_} = {right_}) [{self.line_number}]"

    def __repr__(self) -> str:
        v_ = self.v
        right_ = self.right
        # if len(self.v) == 1:
        #     v_ = self.v[0]
        # if len(self.right) == 1:
        #     right_ = self.right[0]

        return f"Assign({v_} = {right_})"


@dataclass
class Update:
    variable: "AST"
    _operator: Operator # +=, -=, *= etc are all valid assignment operators
    right: 'AST' or list['AST']
    line_number: int = 0
    
    # def __repr__(self) -> str:
    #     right_ = self.right
    #     # if len(self.v) == 1:
    #     #     variable_ = self.variable[0]
    #     # if len(self.right) == 1:
    #     #     right_ = self.right[0]
    #     return f"Update({self.variable} {self._operator} {right_}) [{self.line_number}]"

    def __repr__(self) -> str:
        right_ = self.right
        # if len(self.v) == 1:
        #     variable_ = self.variable[0]
        # if len(self.right) == 1:
        #     right_ = self.right[0]
        return f"Update({self.variable} {self._operator} {right_})"



@dataclass
class For:
    exp1: 'AST'
    condition:'AST'
    exp2:'AST'
    body : Sequence
    line_number: int = 0
    
    def __repr__(self) -> str:
        return f"For(({self.exp1} ;{self.condition};{self.exp2};) do {self.body})"

    # def __repr__(self) -> str:
    #     return f"For(({self.exp1} ;{self.condition};{self.exp2};) do {self.body}) [{self.line_number}]"
    
@dataclass
class Indexer:
    val: Identifier
    index: 'AST'
    index1: 'AST'
    index2 : 'AST'

    def __repr__(self) -> str:
        return f"Indexer({self.val}[{self.index}])"
    
@dataclass
class ListOperations:
    val: Identifier
    operation: str
    itemTobeAdded: 'AST'
    index: 'AST'
    
    def __repr__(self) -> str:
        return f"ListOperations({self.val}.{self.operation}({self.itemTobeAdded},{self.index}))"

@dataclass
class Function:
    name: Identifier
    args: list[Identifier]
    body: Sequence

    def __repr__(self) -> str:
        return f"Function({self.name}({self.args}) )"
@dataclass
class FunctionCall:
    name: Identifier
    args: list['AST']

    def __repr__(self) -> str:
        return f"FunctionCall({self.name}({self.args}))"

@dataclass
class Return:
    val: 'AST'

    def __repr__(self) -> str:
        return f"Return({self.val})"
# error classes
class InvalidProgram(Exception):
    pass

class KeyError(Exception):
    pass

class EndOfLineError(Exception):
    pass


@dataclass
class Struct:
    name: str # string of python
    fields: list
    
    def get(self, key: Identifier):
        """get the value of a field in the struct

        Args:
            key (Identifier): the name of the field

        Returns:
            Value: the value of the field
        """ 
        for field in self.fields:
            if field[0] == key:
                return field[1]
        raise KeyError(f"Struct {self.name} does not have a attribute named {key}")
    
    def set(self, key: Identifier, value: "Value"):
        """set the value of a field in the struct

        Args:
            key (Identifier): the name of the field
            value (Value): the value to set the field to
        """ 
        for field in self.fields:
            if field[0] == key:
                field[1] = value
                return
        raise KeyError(f"Struct {self.name} does not have a attribute named {key}")
    
    def __repr__(self) -> str:
        field_string = ''
        for field in self.fields:
            field_string += f"{field}, "
        return f"Struct {self.name} begin\n{field_string}\nend"


#defining environment class for storing variables and their values in a dictionary 
@dataclass
class Environment:
    envs : List[dict] # environments are stored in a list of dictionaries


    # def __repr__(self):
    #     return_str = "Start ====================\n"
    #     for env in self.envs:
    #         return_str+="Entering new scope \n"
    #         for key in env:
    #             return_str += f"{key} : {env[key][0]} "
    #             return_str+="\n"
    #         return_str+="Exiting scope \n"
    #     return_str+="End ===================="
    #     return return_str
    def __repr__(self):
        rtr = "Program Environment: \n"
        temp_dic = {}
        for env in self.envs:
            for key, val in env.items():
                temp_dic[key] = val[0]
        for key, val in temp_dic.items():
            rtr += f"{key} : {val}\n"
        return rtr
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

    def update(self, identifier: Identifier | Indexer, value):
        """Update the value of a variable in the current scope

        Args:
            identifier (Identifier): the variable to update
            value (Value): the new value of the variable to update

        Raises:
            InvalidProgram: if the variable is immutable and trying to update it
            KeyError: if the variable is not defined in any scope
        """
        for env in reversed(self.envs):
            if isinstance(identifier, Identifier):
                search = identifier.name
            elif isinstance(identifier, Indexer):
                search = identifier.val.name
                pass
            if search in env:
                if env[search][-1].is_mutable:
                    # if str(type(env[identifier.name][0]).__name__) != str(type(value).__name__):
                    #     raise InvalidProgram(
                    #         f"TypeError: Cannot assign {str(type(value).__name__)} to a Identifier of type {str(type(env[identifier.name][0]).__name__)}")

                    # env[identifier.name] = [value, identifier]
                    if isinstance(identifier, Identifier):
                        env[search] = [value, identifier]
                    elif isinstance(identifier, Indexer):
                        env[search][0].set(identifier.index, value)
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

    def restore(self,restore_env):
        self.envs = restore_env.copy()




display_output = [] # list to store the output of print statements as strings
inbuilt_data_types = [NumLiteral, StringLiteral, BoolLiteral, FloatLiteral, ListLiteral] # list of in build datatype data types
user_defined_data_types = {} # dictionary to store user defined data types
# data_type.name = Struct(name, fields)

source_code = []

Value_literal = int | float | bool | str
Value = None | NumLiteral | StringLiteral | BoolLiteral | FloatLiteral | ListLiteral | Struct 
AST = Value | Identifier | Sequence | BinOp | ComparisonOp | UnaryOp | Let | Assign | Update | Indexer| IfElse | While | For | Print | Keyword | Operator | Bracket | Comments | EndOfLine | EndOfFile | Function | FunctionCall | Return
