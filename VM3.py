from typing import List

class BytecodeGenerator:
    def __init__(self):
        self.code = []
        self.labels = {}

    def generate(self, ast):
        self.visit(ast)
        return self.code

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise NotImplementedError(f"No visit_{type(node).__name__} method defined")

    def visit_Num(self, node):
        self.code.append(("LOAD_CONST", node.n))

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        opname = node.op.__class__.__name__.upper()
        self.code.append((opname,))

    def visit_Assign(self, node):
        self.visit(node.value)
        if isinstance(node.target, ast.Name):
            self.code.append(("STORE_NAME", node.target.id))
        elif isinstance(node.target, ast.Subscript):
            self.visit(node.target.value)
            self.visit(node.target.slice.value)
            self.code.append(("STORE_SUBSCR",))

    def visit_Name(self, node):
        self.code.append(("LOAD_NAME", node.id))

    def visit_Subscript(self, node):
        self.visit(node.value)
        self.visit(node.slice.value)
        self.code.append(("BINARY_SUBSCR",))

    def visit_If(self, node):
        self.visit(node.test)
        end_label = self.new_label()
        self.code.append(("POP_JUMP_IF_FALSE", end_label))
        self.visit(node.body)
        if node.orelse:
            else_label = self.new_label()
            self.code.append(("JUMP_FORWARD", else_label))
        self.code.append((end_label, None))
        if node.orelse:
            self.visit(node.orelse)
            self.code.append((else_label, None))

    def visit_While(self, node):
        start_label = self.new_label()
        end_label = self.new_label()
        self.code.append((start_label, None))
        self.visit(node.test)
        self.code.append(("POP_JUMP_IF_FALSE", end_label))
        self.visit(node.body)
        self.code.append(("JUMP_ABSOLUTE", start_label))
        self.code.append((end_label, None))

    def visit_FunctionDef(self, node):
        self.labels[node.name] = len(self.code)
        self.code.append(("MAKE_FUNCTION", 0))
        for arg in node.args.args:
            self.code.append(("STORE_NAME", arg.arg))
        self.visit(node.body)
        self.code.append(("RETURN_VALUE",))

    def visit_Call(self, node):
        for arg in node.args:
            self.visit(arg)
        self.visit(node.func)
        self.code.append(("CALL_FUNCTION", len(node.args)))

    def visit_Return(self, node):
        if node.value:
            self.visit(node.value)
        else:
            self.code.append(("LOAD_CONST", None))
        self.code.append(("RETURN_VALUE",))

    def new_label(self):
        label = len(self.code)
        self.code.append(None)
        return label
