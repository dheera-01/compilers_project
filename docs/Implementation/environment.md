# Environment
 For storing the Identifier and value pairs, Environment class is declared. This `Environment` object is initialised in the main of parser.py where the program starts. Then same `Environment` is passed on recursively in the eval.
 
## Environment class

```python
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
                    if str(type(env[identifier.name][0]).__name__) != str(type(value).__name__):
                        raise InvalidProgram(
                            f"TypeError: Cannot assign {str(type(value).__name__)} to a Identifier of type {str(type(env[identifier.name][0]).__name__)}")

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
It iterates over all the dictionary starting from last one(reversed order). It also throws error if immutable Identifier is requested for update. Then it checks the type of already assigned value matches the new value to be assigned. Otherwise, it changes the already stored value.

#### get
It returns the value stored in the `name` identifier.