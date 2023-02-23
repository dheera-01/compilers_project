class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.vars = {}

    def get(self, var):
        if var in self.vars:
            return self.vars[var]
        elif self.parent is not None:
            return self.parent.get(var)
        else:
            raise Exception(f"Undefined variable '{var}'")

    def set(self, var, value):
        self.vars[var] = value

def let(var, value, env):
    env.set(var, value)

# creates a new environment
global_env = Environment()

# creates a child environment
child_env = Environment(global_env)

# sets a variable in the child environment
let("x", 1, child_env)

# sets a variable in the parent environment
let("y", 2, global_env)

# gets the values of the variables in the child and parent environments
x = child_env.get("x")
y = global_env.get("y")

def test_environment():
    global_env = Environment()

    let("x", 1, global_env)
    assert global_env.get("x") == 1

    child_env = Environment(global_env)
    let("y", 2, child_env)
    assert child_env.get("y") == 2
    #assert global_env.get("y") == pytest.raises(Exception, match="Undefined variable 'y'")
    assert child_env.get("y") == 2

    let("z", 3, global_env)
    assert global_env.get("z") == 3
    assert child_env.get("z") == 3
