# PlsExplain (aka jamlang0001)
A small dynamically typed programming language with first-class comments.

### Running the Interpreter
#### Dependencies
The interpreter depends on python3 and [lark](https://github.com/lark-parser/lark). Lark can be installed with `pip install lark`.
#### REPL
When the interpreter is launched without command line parameters it starts in interactive mode
    
    $ ./pls_explain.py
    >>> print("hello world")
    hello world /*the string "hello world"*/
    >>>
    
  To exit the REPL press `Ctrl-D`.
  
 #### Running a Program from a File
To execute a Program written in *PlsExplain*, pass the pass to the program as the first command line argument.

    $ ./pls_explain.py examples/hello_world.jl
    Hello World /*the string "Hello World"*/
	
### First-Class Comments
Comments are first-class values in *PlsExplain*. This means that they are expressions, can be stored in variables, passed as function arguments and be returned by functions.
    
    >>> let comment = /* This is a comment */;
    >>> print(comment)
    /* This is a comment */
    >>> print(/*another comment*/)
    /*another comment*/
 
At a first glance comments might seem to be equivalent to strings. The difference  is that comments can be used to explain something: In *PlsExplain* all values have an associated comment that explains the value. When called with a single argument, `print` shows the associated comment. To associate a comment with a value, simply write it next to the expression:

    >>> let x = 40 + 2 /* the number fourtytwo */;
    >>> print(x)
    42.0 /* the number fourtytwo */
 
 Explaining comments don't have to be comment-literals:
 
     >>> let comment = /* this is a comment */
     >>> let x = 42.0 comment
 
 Trying to explain a value with something that is not a comment obviously results in a type error.
 
    >>> 42 "this is not a comment"
    Backtrace (most recent call last):

    line 1:
    42 "this is not a comment"
    ^~~~~~~~~~~~~~~~~~~~~~~~~~
    type error: type JlString can not be used to explain values
    
    >>> let s = "not a comment either"
    >>> 42 s
    Backtrace (most recent call last):

    line 1:
    42 s
    ^~~~
    type error: type JlString can not be used to explain values
    
 #### Auto-Comments
 If a value is not explained by an explicit comment, the interpreter automagically generates a helpful comment.
 
    >>> let x = 4
    >>> print(x)
    4.0 /* the number 4.0 */
    >>> let y = x + 10
    >>> print(y)
    14.0 /* the sum of the number 4.0 and the number 10.0 */
    
 #### The *explain* operator
 The comment explaining a value can be retrieved with the `?`operator.

    >>> print(x?)
    /* the number 4.0 */

#### Manipulating Comments
The auto-generated comment can sometimes be a little bit verbose:

    let fact = fn(n) {
         if (n == 0) {
            1
         } else {
            fact(n - 1) * n;
         }
    };
    print(fact(4));
    
This program prints:

    24.0 /*the product of the product of the product of the product 
    of the number 1.0 and the difference of the difference of 
    the difference of the number 4.0 and the number 1.0 and the 
    number 1.0 and the number 1.0 and the difference of the 
    difference of the number 4.0 and the number 1.0 and the number
    1.0 and the difference of the number 4.0 and the number 1.0
    and the number 4.0*/


Since comments are first-class values we can manipulate them on the fly. This allows us to generate even more helpful comments.

    let fact = fn(n) {
         if (n == 0) {
            1
         } else {
            /* lets generate a helpful comment for the return value */;
            /* (Comments can be concatenated with +) */
            let comment = /* the factorial of */ + n?;
            /* explain the return value with the generated comment, by writing it to the right of the return value */
            (fact(n - 1) * n) comment;
         }
    };
    let h = 4 /*the number of hours i've slept*/;
    print(fact(h));

The output of this program is more concise:
    
    24.0 /* the factorial of the number of hours i've slept*/

#### Meta-Comments and Meta-Meta-Comments and ...
Since comments are first-class values, comments can also be explained by comments. Obviously comments explaining a comment can also be explained by comments.

    >>> let x = a /* comment */ /* meta-comment */ /* meta-meta-comment */

Comments are right-associativ, so the previous statement is equivialent to

    >>> let x = (a {/* comment */ {/* meta-comment */ /* meta-meta-comment */}}}

Note: If we would use parenthesis to group the comments, the parser would interpret the expression as an attempt to call the function`a`. Conveniently, blocks delimited by curly-braces evaluate to the value of the their last expression, which means that they can be used instead.

### Datatypes
|Type| Description |
|--|--|
| `Comment` | the most important type |
| `String`| unicode strings |
| `Number`| floating point numbers |
| `Bool`| `True`or `False`|
| `Unit`| only the value `()`|

### Syntax
The Syntax is Expression based.
#### Literals
| Type  | Examples |
|--|--|
| `Comment`| `/* this is a comment */`
| `String` | `"hello"` `"with\n escape \" chars"` |
| `Number` | `1`, `-1.0`, `42.5` |
| `Bool`| `True`, `False` |
| `Unit`| `()`|

#### Grouping
`(a + b) * c`

#### Blocks
`{ print("hello"); print("world") }`

Multiple expressions can be grouped with curly braces. Expressions are separated with semicolons. The semicolon after the last Expression is optional. Blocks evaluate to the value of their last expression.

#### Functions
##### Definition
    let f = fn (arg) {
	    print(arg);
    };
  
 Functions can be defined with the keyword `fn`followed by a parenthesized list of parameters and the function body. The braces are optional, when the body is a single expression. All functions are anonymous and first-class.
#####  Calling a function
`print("hello")`
Nothing special here.

#### Variables
##### Declaration
`let x = 42`
Variables are declared with the keyword `let` and must be initialized. Variables are lexicaly scoped. Declarations evaluate to the assigned value.

##### Assignment
`x = 100`
Assignments evaluate to the assigned value.

#### Binary Expressions
`a + b`
Operators ordered by decreasing precedence:
| Operators | Examples |
|--|--|
| `?` | `x?` |
| `*`, `-`, `%` | `x * y`, `x % 5` |
| `+`, `-` | `x + y` |
| `==`, `<`, `>` | `x < y` |
| `&` | `x & y` |
| `|` | `x | y` |

The only unusual operator is the *explain* operator (`?`). See **First Class Comments** for more details.
The logic operators `&`and `|`are not short circuiting.


#### Control Flow Expressions
##### If
`if (condition) { "true" } else { "false" }`
Parenthesis around the condition are mandatory. Braces around single expressions and the `else` branch are optional. If expressions evaluate to the value of the taken branch.
##### While
`while (condition) { do_something() }`
Parenthesis around the condition are mandatory. The Braces cant be omitted, if the body is a single expression. While loops evaluate to the value of the loop body during the last iteration.

### Build in Functions

| Function | No. of Arguments | Description  |
|--|--|--|
|  `print(*arg)` | any | Print any number of values. When called with a single argument, the arguments comment is printed as well |
|`input()` | 0 |  Read single line and return it as a string. |
| `str(arg)`| 1 |  Convert value to string.|
| `cmnt()` | 1 | Convert value to comment.|




