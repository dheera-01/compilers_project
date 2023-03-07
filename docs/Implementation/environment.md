# Environment
 For storing the Identifier and value pairs, Environment class is declared. This `Environment` object is initialised in the main of parser.py where the program starts. Then same `Environment` is passed on recursively in the eval.
 
## Environment class

```python
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

    def add(self, identifier, value):
        curr_env = self.envs[-1]
        if identifier.name in curr_env:
            raise InvalidProgram(f"Variable {identifier.name} already defined")
            return
        self.envs[-1][identifier.name] = [value, identifier]

    def update(self, identifier, value):
        for env in reversed(self.envs):
            if identifier.name in env:
                if env[identifier.name][-1].is_mutable:
                    env[identifier.name] = [value, identifier]
                else:
                    raise InvalidProgram(f"Variable {identifier.name} is immutable")
                return
        raise KeyError()

    def get(self, name):
        for env in reversed(self.envs):
            if name in env:
                return env[name][0]
        raise KeyError()
```

### Members
It has a member `envs` which is a list of dictionaries. It simulates the behaviour of stack for implementing scope where is latest scope is last element in the list. Dictionary contains the mapping of `Identifier.name` and list of value(NumLiteral, FloatLiteral, BoolLiteral, etc) and `Identifier` object.

### Methods

#### enter_scope
This adds a new empty dictionary at the end of list.

#### exit_scope
This removes the last element from the list.

#### add
Adds a new mapping in the last dictionary(latest scope) via `self.envs[-1][identifier.name] = [value, identifier]`.

#### update
It iterates over all the dictionary starting from last one(reversed order). It also throws error if immutable Identifier is requested for update. Otherwise, it changes the already stored value.

#### get
It returns the value stored in the `name` identifier.