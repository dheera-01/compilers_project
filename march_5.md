# Let Statments 

Parser for let statement is implemented. The following examples will help to understand the systax and use of let statements. Let statments will return whatever value written in the parenthesis.
1)
```commandline
let x=1+2*3 (x+1) ;
print(x);
```

Output: 7


2) Nested Let statements 
```
assign v=let u=2
(
    let t=2
        (let a=2(u+ a*t))
);
print(v);
```

Output: 6 

# Variable Scoping

Varibale scoping is now itegrated in the parser. Scope will be created and destroyed wheever enter and exit while loop, for loop, if and else blocks. The following examples will help to understand the scoping of variables.
Currently we have implemented scoping by using a stack. Whenever a new scope is created a new entry is pushed in the stack. Whenever a scope is destroyed the top entry is popped from the stack. 
1. This example will work perfectly fine as the y is only called inside its scope. 
```
assign x=1;
while(x<10)
{
    assign x=x+1;
    assign y=x;
    print(y);
};
```

Output: 2 3 4 5 6 7 8 9 10

2. The following code will throw an error as the variable y is called outside its scope. 

```commandline
assign x=1;
while(x<10)
{
    assign x=x+1;
    assign y=x;
};
print(y);
```

Output: Error: KeyError()

# Performance comparison of our languauge with python 
To know how slow our language is when compared to python we wrote two programs in both the languages. Both this program do logically same thing. 
For measuring time taken by program we have used the time module of pyhton. 
### While loop with 1000 iterations
Pyhton Code:
```python
i=0
    while(i<1000):
        print(i)
        i=i+1
```

Our Language Code:
```
assign i=0;
while(i<1000)
{
    print(i);
    assign i=i+1;
};
```
The following table shows code and mean time taken over 3 iterations. 

| Language     | Mean Time Taken (ms) |
|--------------|----------------------|
| Python       | 27.24                |
| Our Language | 116.38               |

