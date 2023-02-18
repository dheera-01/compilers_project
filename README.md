# compilers_project
Repository containing the project of compilers course.

## Targets
1.  Unary operators. Example:  `let x = 5 in -x`
2.  String concatenation. Example: `let x = 'hello' in y = 'world' in x~y` outputs `'helloworld'`
3.  Booleans, comparison, if-else etc.
4.  Mutable variables.
5.  Can refer to project Euler for some problems.

## Feature list provided
- [x] M: A number type and arithmetic.
- [ ] I: Multiple number types such as fractions and integers. Quotient and division are different. Quotient has type (integer, integer) -> integer and division has type (fraction, fraction) -> fraction. An integer can be used wherever a fraction can be used.
- [x] M: Let expressions.
- [ ] I: Parallel let (See let..and in Ocaml).
- [x] M: A Boolean type, comparisons, and if-else.
- [ ] I: An explicit unary boolifying operator. In Perl so x where x has any type produces a Boolean value. For example, if x is a number, it is true when non-zero. If x is a string, it is true when non-empty.
- [ ] M: Mutable variables.
- [ ] I: Static type checking. The expression (5>3) + 2 should be an error without evaluating anything.
- [ ] A: Disallow mutable variables to change type. With the binding let mut p = True in ..., the variable p should only be assigned boolean values.
- [x] M: Strings with concatenation and slicing.
- [x] M: A print operation that prints values to screen.
- [x] M: loops.
- [ ] M: Functions
- [ ] M: Lists with operations cons, is-empty?, head, tail.
- [ ] I: for loop to iterate over lists.
- [ ] I: Mutable arrays with indexing, appending, popping, concatenation, element assignment.
- [ ] I: Allow declaration of type of array. For example let xs: Array[int] = [] in ... should prevent xs[0] ← 5/3.
- [ ] A: Step-by-step debugger for your programming language.
- [ ] A: User-defined types – records.
- [ ] A: First-class functions.

## References
[Abstract Syntax Tree Constructs](https://docs.python.org/3/library/ast.html)

## Some conventions we should follow for better workflow
1. Tests for any feature implemented will be written by someone else so that we understand each others code on the go.
2. As all of us are collaborators in the project, we can merge pull requests. But we will only merge our feature branches after everyone has reviewed by commenting on the `pull request`.
3. Obviously `documentation` of feature implemented will be done by the same person who implemented.
4. Create `issue` on GitHub for any error or bug someone finds in the previously pushed code.
5. Workflow:
    1. `Main` Branch: Only working features pushed on this. 
    2. `Dev` Branch:
        1. Create a separate branch for every feature.
            1. Create further branches for other purposes. For example, `ifelse` branch can have further branch as `tests`
6. Whenever you defining a new data type pls define in the declaration.py and then import that file in your code. It will help us all to follow same data structure.
7. From now onwards don't use fraction as used by sir, use the standard datatype like int, str etc.
8. Test case should be made in different files not within same file.
9. Whenever you define a new function use docstring's python to define that function properly. It will help other to understand your code and will come in handy when we are using that function somewhere in the code.


## while loop

### Implementation
While consists of two components, the first being the boolean condition and the second being the body of the while loop. To implement while loop for our language, we evaluate the condition on each iteration. If the condition is true, we evaluate the body, a **sequence** of statements and jump back to re-evaluate the condition. If the condition is false, then we exit the loop. while loop returns value **None** on a complete evaluation. 
### Some Examples
Infinite Loop

```commandline
while(True)
{
    print("Hello")
}
```

Basic Incrementer

```commandline
i=0
while(i<10)
{    
    print(i);
    i=i+1;
}
```

Note: As body of while is sequence of ASTs and parser of sequence is not yet coded this examples cannot be directly used as source code. But once the correct parse tree is given while works correctly. We have confirmed this by making tests for while loop. 
## for loop

### Implementation
for loop consits of four components, the first component is the assignment operator(assigning value to iterator). Second component is condition for halting, third component being assignment again(for incrementing/decrementing value of iterator). Finally fourth component is the body which is **sequence** of ASTs. 
<br><br> for loop returns **None** on complete evalution. In order to implement for loop we first evaluate the first assignment statement, evaluate the condition. If condition is true we evaluate the body then assingment statement for increment/decrement. Now we pass condtion and body combined with increment/decrement statement to the while loop. Thus body is evaluated once in for loop after that it is being passed to while loop for further evaluation. 

### Some Examples 

```commandline
for(i=0;i<10;i=i+1)
{
    print(i);
}
```

**Note**: As body of for is sequence of ASTs and parser of sequence is not yet coded this examples cannot be directly used as source code. But once the correct parse tree is given for works correctly. We have confirmed this by making tests for for loop.

