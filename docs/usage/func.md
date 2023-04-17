# Functions 

Syntax:

```python

func <name>(<arg1>, <arg2>, ...) {
    <body>
}

```

## Some Examples:


### Simple addition function

```python   
func add(a,b) {
    return a+b;
}
```

### Odd or Even Function

```python

func odd_even(a) {
    if(a%2==0) {
        return "Even";
    }
    else {
        return "Odd";
    }
}

```

### Factorial Function (recursive)

```python
func fact(a) {
    if(a==1) {
        return 1;
    }
    else {
        return a*fact(a-1);
    }
}
```

### Fibonacci Function (recursive)

```python
func fib(a) {
    if(a==0) {
        return 0;
    }
    elif(a==1) {
        return 1;
    }
    else {
        return fib(a-1)+fib(a-2);
    }
}
```



