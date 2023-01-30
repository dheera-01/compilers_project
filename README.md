# compilers_project
Repository containing the project of compilers course.

## Targets
1.  Unary operators. Example:  `let x = 5 in -x`
2.  String concatenation. Example: `let x = 'hello' in y = 'world' in x~y` outputs `'helloworld'`
3.  Booleans, comparison, if-else etc.
4.  Mutable variables.
5.  Can refer to project Euler for some problems.

## Feature list provided
1. M: A number type and arithmetic.
2. I: Multiple number types such as fractions and integers. Quotient and division are different. Quotient has type (integer, integer) -> integer and division has type (fraction, fraction) -> fraction. An integer can be used wherever a fraction can be used.
3. M: Let expressions.
4. I: Parallel let (See let..and in Ocaml).
5. M: A Boolean type, comparisons, and if-else.
6. I: An explicit unary boolifying operator. In Perl so x where x has any type produces a Boolean value. For example, if x is a number, it is true when non-zero. If x is a string, it is true when non-empty.
7. M: Mutable variables.
8. I: Static type checking. The expression (5>3) + 2 should be an error without evaluating anything.
9. A: Disallow mutable variables to change type. With the binding let mut p = True in ..., the variable p should only be assigned boolean values.
10. M: Strings with concatenation and slicing.
11. M: A print operation that prints values to screen.
12. M: loops.
13. M: Functions
14. M: Lists with operations cons, is-empty?, head, tail.
15. I: for loop to iterate over lists.
16. I: Mutable arrays with indexing, appending, popping, concatenation, element assignment.
17. I: Allow declaration of type of array. For example let xs: Array[int] = [] in ... should prevent xs[0] ← 5/3.
18. A: Step-by-step debugger for your programming language.
19. A: User-defined types – records.
20. A: First-class functions.

## references
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
