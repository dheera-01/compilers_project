# While loops 
Use:
```while``` loops can we used to repeat a block of code until a condition is met.

Syntax:
```
while(<condition>)
{
    <body>
}
```

Evaluates body until condition evaluates to false. 

Example:
1. Print numbers from 1 to 10
```
assign i=1;
while(i<=10)
{
    print(i);
    i=i+1;
}
```
Output:
```
1
2
3
4
5
6
7
8
9
10
```

2. Nexted while loops
```
assign i=1;
assign n=3;
while(i<=n)
{
    assign j=1;
    while(j<=n)
    {
       print(i+ "  "+ j);
       j=j+1;
    }
    i=i+1;
}

```
Output:
```
1 1
1 2
1 3 
2 1 
2 2
2 3
3 1
3 2
3 3
```
3. Infinite while loop

```
while(true)
{
    print("Hello");
};
```

Output:
```
Hello 
Hello
Hello 
...
```

