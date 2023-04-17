# Bytecode and VM

This code implements a simple bytecode and a virtual machine (VM) to execute it. The bytecode is a sequence of instructions that are emitted during code generation. The VM loads the bytecode, restarts the program, and executes the instructions until a halt instruction is reached. The VM has a stack data structure to hold intermediate values.

The instructions are defined using Python's dataclass decorator, which allows the creation of classes with built-in data management methods, like init and repr. The instructions implemented are:

- `JMP`: jumps to a label's target instruction
- `JMP_IF_FALSE`: jumps to a label's target instruction if the top value of the stack is False
- `JMP_IF_TRUE`: jumps to a label's target instruction if the top value of the stack is True
- `ENTER_SCOPE`: enters a new scope for variable bindings
- `EXIT_SCOPE`: exits the current scope and returns to the previous one
- `PUSH`: pushes a value onto the stack
- `ADD`: pops two values from the stack, adds them, and pushes the result onto the stack
- `SUB`: pops two values from the stack, subtracts the second from the first, and pushes the result onto the stack
- `MUL`: pops two values from the stack, multiplies them, and pushes the result onto the stack
- `DIV`: pops two values from the stack, divides the first by the second, and pushes the result onto the stack
- `UMINUS`: negates the top value of the stack
- `UPLUS`: leaves the top value of the stack unchanged
- `POP`: pops the top value from the stack
- `HALT`: stops the program execution
- `E`: pops two values from the stack and pushes True if they are equal, False otherwise
- `NE`: pops two values from the stack and pushes True if they are not equal, False otherwise
- `LT`: pops two values from the stack and pushes True if the first is less than the second, False otherwise
- `GT`: pops two values from the stack and pushes True if the first is greater than the second, False otherwise
- `LE`: pops two values from the stack and pushes True if the first is less than or equal to the second, False otherwise
- `GE`: pops two values from the stack and pushes True if the first is greater than or equal to the second, False otherwise
- `LOAD_FAST`: loads a variable's value from the current scope onto the stack
- `STORE_FAST`: stores a value on the top of the stack in a variable in the current scope
- `STORE_FAST_UPDATE`: updates a variable's value in the current scope
- `PRINT`: prints the top value of the stack to the console

The bytecode is defined using the ByteCode class, which contains the instructions emitted during code generation.

The VM class is responsible for loading the bytecode, restarting the program, and executing the instructions. The execute() method runs a while loop that matches the current instruction and executes its corresponding action. The ENTER_SCOPE and EXIT_SCOPE instructions are responsible for creating and destroying variable scopes.

The do_codegen() function is responsible for generating bytecode from the AST. Below are the implementations of the do_codegen() function for the different AST nodes:


- `Sequence`: generates bytecode for the sequence's statements
- `NumLiteral & StringLiteral`: generates bytecode for the literal
- `BinOp`: generates bytecode for the left and right operands, then generates bytecode for the operator
- `ComparisonOp`: generates bytecode for the left and right operands, then generates bytecode for the comparison operator like `==`, `!=`, `<`, `>`, `<=`, `>=`, etc.
- `Assign`: generates bytecode for assigning the value to the Identifier
- `Identifier`: generates bytecode for loading the value of the Identifier
- `Update`: generates bytecode for updating the value of the Identifier
- `Print`: generates bytecode for the expression to be printed
- `ListLiteral`: generates bytecode for the list's elements
- `ListOperations`: generates bytecode for the list's elements, then generates bytecode for the operation
- `Indexer`: generates bytecode for the list and index
- `IfElse`: generates bytecode for the condition, then generates bytecode for the if and else statements
- `While`: generates bytecode for the condition, then generates bytecode for the loop body
- `For`: generates bytecode for the loop variable, then generates bytecode for the list, then generates bytecode for the loop body

The do_codegen() function returns a ByteCode object, which is then loaded into the VM and executed.

## Bytecode code for different AST nodes

### For Loop
```python
case For(exp1, condition, exp2, body):
    label1 = code.label()
    label2 = code.label()
    # label3 = code.label()
    codegen_(exp1)
    code.emit_label(label1)
    codegen_(condition)
    code.emit(I.JMP_IF_FALSE(label2))
    # Enter scope
    code.emit(I.ENTER_SCOPE())
    
    codegen_(body)
    # Exit scope
    codegen_(exp2)
    
    code.emit(I.JMP(label1))
    
    code.emit_label(label2)
    code.emit(I.EXIT_SCOPE())
```

- The code is handling the For loop construct. The For loop has four components: initialization expression (exp1), loop condition (condition), loop update expression (exp2), and the loop body (body).

- First, two Label instances are created, label1 and label2, using the code.label() method. These labels will be used to mark the beginning and end of the loop.

- The code generator function codegen_() is then called on the exp1 component to generate bytecode for it. After that, an instruction is emitted to mark the beginning of the loop using code.emit_label(label1).

- The condition component is then processed by calling codegen_() on it and an instruction is emitted to jump to label2 if the condition is False. This is done using code.emit(I.JMP_IF_FALSE(label2)).

- After this, the loop body body is processed by calling codegen_() on it. Since scoping is handled, nested loops are also supported.

- Next, the exp2 component is processed by calling codegen_() on it. This component typically contains the update expression for the loop variable.

- After this, an instruction is emitted to jump back to the beginning of the loop using code.emit(I.JMP(label1)).

- Finally, a label is emitted using code.emit_label(label2) to mark the end of the loop. An instruction is also emitted to exit the loop scope using code.emit(I.EXIT_SCOPE()).

- Since scoping is handled, the cases for nested loops also works.

### While Loop

```python
case While(condition, body):
    label1 = code.label()
    label2 = code.label()
    code.emit_label(label1)
    code.emit(I.ENTER_SCOPE())
    codegen_(condition)
    
    code.emit(I.JMP_IF_FALSE(label2))
    
    
    codegen_(body)
    
    
    code.emit(I.JMP(label1))
    code.emit_label(label2)
    code.emit(I.EXIT_SCOPE())
```

- This code block is a case statement that handles the while loop construct in the input program.

- It begins by creating two labels, label1 and label2, to mark the start and end of the loop respectively. Then, the code.emit_label(label1) instruction is used to add the label1 to the generated bytecode, serving as a reference point for the jump back to the beginning of the loop.

- Next, the ENTER_SCOPE() instruction is added to the bytecode to enter a new scope before the loop starts, and the condition expression is generated. The JMP_IF_FALSE instruction is added to the bytecode with label2 as its target label. If the condition evaluates to false, the bytecode will jump to the end of the loop, marked by label2.

- The body of the loop is generated next, followed by a JMP instruction to jump back to the beginning of the loop (label1). Finally, label2 is emitted to mark the end of the loop, followed by the EXIT_SCOPE() instruction to exit the scope created before the loop started.

- This code block handles the while loop construct by generating the necessary bytecode to execute the loop, handle the loop condition, and properly handle scoping.


### ListLiteral

```python
case ListLiteral(value):
    code.emit(I.PUSH('LIST_BEGIN'))
    for element in value:
        codegen_(element)
    code.emit(I.MAKE_LIST())
```

- The ListLiteral case is a part of the code generation process for a Python list literal. It emits instructions to the bytecode to create a new list and add each element to it.

- First, it emits an instruction to push a marker 'LIST_BEGIN' onto the stack to indicate the beginning of the list. Then, it iterates over each element of the list and generates code for it using `codegen_()` function. Finally, it emits an instruction `MAKE_LIST()` to make the list by consuming all elements of the list from the stack and building a new list object from them. The resulting list is then pushed back onto the stack.

### ListOperations

```python
case ListOperations(identifier, val, item, indVal):
    if val == "LEN":
        codegen_(identifier)
        code.emit(I.LIST_OP('LEN'))
    elif val == "HEAD":
        codegen_(identifier)
        code.emit(I.LIST_OP('HEAD'))
    elif val == "TAIL":
        codegen_(identifier)
        code.emit(I.LIST_OP('TAIL'))
    elif val == "APPEND":
        codegen_(item)
        codegen_(identifier)
        code.emit(I.LIST_OP('APPEND'))
    elif val == "POP":
        codegen_(identifier)
        code.emit(I.LIST_OP('POP'))
        code.emit(I.STORE_FAST_UPDATE(identifier.name))
    elif val == "ChangeOneElement":
        codegen_(indVal)
        codegen_(item)
        codegen_(identifier)
        code.emit(I.LIST_OP('UPDATE'))
```
- This code appears to be a Python function called ListOperations that takes in four arguments: identifier, val, item, and indVal.

- The function contains an if-else block that checks the value of val. Depending on the value, the function emits a corresponding instruction using the emit() method of an object called code.

- For example, if val is equal to "LEN", the function emits the instruction LIST_OP('LEN'). If val is equal to "APPEND", the function first generates code for item and identifier using the codegen_() function, and then emits the instruction LIST_OP('APPEND').

- If val is equal to "POP", the function generates code for identifier, emits the instruction LIST_OP('POP'), and then emits the instruction STORE_FAST_UPDATE(identifier.name) to store the result of the operation in the corresponding identifier.

- Finally, if val is equal to "ChangeOneElement", the function generates code for indVal, item, and identifier using the codegen_() function and emits the instruction LIST_OP('UPDATE').

### IFElse

```python
case IfElse(condition, if_body, elif_body, else_body):
    elif_list = []

    new_if = IfElse(condition, if_body, [], None)
    elif_list.append(new_if)

    labels = []
    for elif_ in elif_body:
        elif_list.append(elif_)

    for elif_ in elif_list:
        label1 = code.label()
        label2 = code.label()
        codegen_(elif_.condition)
        
        code.emit(I.JMP_IF_FALSE(label1))
        
        code.emit(I.ENTER_SCOPE())
        codegen_(elif_.if_body)
        code.emit(I.JMP(label2))
        
        code.emit(I.EXIT_SCOPE())
        code.emit_label(label1)
        
        labels.append(label2)

    code.emit(I.ENTER_SCOPE())
    codegen_(else_body)
    code.emit(I.EXIT_SCOPE())
    for label in labels:
        code.emit_label(label)
```
Explain the logic here.


# Execution of code in the VM

The VM includes a switch statement that handles different opcodes. The following is a breakdown of how each opcode is handled:

- `I.JMP(label)`: This opcode causes the program to jump to the target of the given label. The instruction pointer (ip) is set to the target of the label.
- `I.JMP_IF_FALSE(label)`: This opcode checks whether the top of the stack is falsy. If it is falsy, the program jumps to the target of the given label. Otherwise, the program moves to the next instruction. The ip is updated appropriately to point to the next instruction to be executed after the jump.
- `I.PUSH(value)`: This opcode pushes the given value onto the stack.
- The `I.PUSH(val)`: The instruction pushes a value onto the stack.
- `I.ADD()`: The instruction pops the top two values from the stack, adds them, and pushes the result back onto the stack. 
- `I.SUB()`: The instruction pops the top two values from the stack, subtracts the second from the first, and pushes the result back onto the stack.
- `I.GE()`: The instruction pops the top two values from the stack, checks if the first is greater than or equal to the second, and pushes a boolean value back onto the stack.

- Other instructions in the code block include `I.GT()`, `I.LT()`, `I.FLOORDIV()`, `I.POW()`, `I.LE()`, `I.E()`, `I.NE()`, `I.MUL()`, `I.DIV()`, and `I.MOD()`, each of which performs a different operation on the stack.

- In addition to stack manipulation, the virtual machine also includes instructions for working with variables and lists. `I.STORE_FAST(name, is_mutable)`: The instruction stores a value in a variable.
- `I.LOAD_FAST(name)`: The instruction loads the value of a variable onto the stack.
- `I.STORE_FAST_UPDATE(name)`: The instruction updates the value of a variable.
- `I.PRINT()`: The instruction prints the top value on the stack.

- The virtual machine also includes instructions for working with lists, such as `I.MAKE_LIST()`, which creates a new list, and `I.LIST_OP(op)`, which performs various operations on a list, such as getting its length, appending a value, and updating an element. The `I.INDEX()` instruction retrieves an element from a list.

Finally, the virtual machine includes instructions for entering and exiting a scope, which allows variables to be stored in different environments.