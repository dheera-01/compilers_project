# Assign and const

`assign` keyword is used for declaring or updating variables. Following class is instantiated whenever parser detects a assign.
```python
@dataclass
class Assign:
    v:Identifier
    right:'AST'
    
    def __repr__(self) -> str:
        return f"Assign({self.v} = {self.right})"
```
`Assign` class has 2 members where v stores the Identifier and right stores the AST which can be any expression. Following is the Identifier class which stores the name of the Identifier and property(`is_mutable`) whether this Identifier can be reassigned in future.

```python
@dataclass
class Identifier:
    name: str
    is_mutable: bool = True

    def __repr__(self) -> str:
        return f"Identifier({self.name})"
```
By default, `is_mutable` is set to `True`. Whenever `const` keyword is used infront of `assign`, then `is_mutable` is set to `False`.

## Parser for assign and const
Following function is called after parser detects a `assign` keyword. This function parses a Identifier and "=" and an expression.
```python
    def parse_assign(self):
        """
        parse the assign expression
        """
        self.lexer.advance()
        left_part = self.parse_atom()
        self.lexer.match(Operator("="))
        right_part = self.parse_expr()
        return Assign(left_part, right_part)
```
Everthing is same as above in whenever 'const' keyword is parsed except that `is_mutable = False`.
```python
    def parse_const(self):
        self.lexer.advance()
        self.lexer.match(Keyword("assign"))
        identifier = self.parse_atom()
        identifier.is_mutable = False
        self.lexer.match(Operator("="))
        right_part = self.parse_expr()
        return Assign(identifier, right_part)
```

## Eval for assign
Once the assign object is constructed, it is evaluated using following case where right AST is first evaluated. Now if the Identifier name is already present in any environment, then Environment `update` is called, else `add`.
Following function searches in the previous environments before adding.
```python
case Assign(identifier, right):
            value = eval(right, program_env, environment)
            for env in reversed(program_env.envs):
                if identifier.name in env:
                    program_env.update(identifier, value)
                    return None

            program_env.add(identifier, value)
            return None
```

