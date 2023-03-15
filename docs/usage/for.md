# for loops
Syntax:
```
for(<assignment> ;<condition> ; <update>;)
{
    <body>
}
```

Declares/update a variable (generally the iterator), evaluates body until condition evaluates to false. Updates the variable (generally the iterator) after each iteration.

Example:
1. Print numbers from 1 to 10
```
for(assign i=1; i<=10; i=i+1;)
{
    print(i);
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

2. Nexted for loops
```
for(assign i=1; i<=3; i=i+1;)
{
    for(assign j=1; j<=3; j=j+1;)
    {
        print(i+ " "+j);
    }
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