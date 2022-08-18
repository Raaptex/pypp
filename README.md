# Py++

> Compiler for Py++ to Python or Executable
## Compiler
Basic command : 
```batch
py pypp.py -m {main.pypp} -o {out_file}
```
## Options
> (* is required)

`-m FILE(.pypp)`*
The file that will be compiled

`-o OUT_FILE`*
The name of the compiler file (without the extension)

`-b`
Create a .exe

`-r`
Auto run after the compilation

### Exemple
To compile and create a `compiled.py` and `compiled.exe` file, and launch the `compiled.exe` file after compilation
```batch
py pypp.py -m script.pypp -o compiled -b -r
```
## Getting started

### Variables
```py
a = 10;
a++;
a--;

b = "Hello";
c = True;
```
### Functions
```py
def add(a, b) {
	return a + b;
}
```
### If Statements
```py
if(a == b) {
	print("a is equal to b");
} else {
	print("a is not equal to b");
}
```
**`elif` is not implemented**

### For Loop
```py
for(i in range(10)) {
	print(i)
}
```

### While Loop
```py
i = 0;
while(i < 10) {
	print(i)
	i++;
}
```
