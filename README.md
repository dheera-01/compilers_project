# compilers_project
Repository containing the project of compilers course.

## Feature list provided
- [x] M: A number type and arithmetic.
- [x] I: Multiple number types such as fractions and integers. Quotient and division are different. Quotient has type (integer, integer) -> integer and division has type (fraction, fraction) -> fraction. An integer can be used wherever a fraction can be used.
- [x] M: Let expressions.
- [x] I: Parallel let (See let..and in Ocaml).
- [x] M: A Boolean type, comparisons, and if-else.
- [ ] I: An explicit unary boolifying operator. In Perl so x where x has any type produces a Boolean value. For example, if x is a number, it is true when non-zero. If x is a string, it is true when non-empty.
- [x] M: Mutable variables.
- [x] I: Static type checking. The expression (5>3) + 2 should be an error without evaluating anything.
- [x] A: Disallow mutable variables to change type. With the binding let mut p = True in ..., the variable p should only be assigned boolean values.
- [x] M: Strings with concatenation and slicing.
- [x] M: A print operation that prints values to screen.
- [x] M: loops.
- [x] M: Functions
- [x] M: Lists with operations cons, is-empty?, head, tail.
- [x] I: for loop to iterate over lists.
- [x] I: Mutable arrays with indexing, appending, popping, concatenation, element assignment.
- [ ] I: Allow declaration of type of array. For example let xs: Array[int] = [] in ... should prevent xs[0] ← 5/3.
- [ ] A: Step-by-step debugger for your programming language.
- [x] A: User-defined types – records.
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
    2. `Developement` Branch:
        1. Create a separate branch for every feature.
            1. Create further branches for other purposes. For example, `ifelse` branch can have further branch as `tests`
6. Whenever you defining a new data type pls define in the declaration.py and then import that file in your code. It will help us all to follow same data structure.
7. From now onwards don't use fraction as used by sir, use the standard datatype like int, str etc.
8. Test case should be made in different files not within same file.
9. Whenever you define a new function use docstring's python to define that function properly. It will help other to understand your code and will come in handy when we are using that function somewhere in the code.
