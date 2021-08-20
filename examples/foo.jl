ct = /*comment*/

f = [foo bar]
s = string([/*buzz*/])
add [/*6*/ /*7*/] /*this is a comment*/
seven = [/*7*/]

seven = fn () {
   return 7
}

comment('(/*comment*/))

x = 7 /*the number seven*/
y = 42 /*the number fourtytwo*/
a = x + y
b = x +/*the variable b*/ y
print(x + y) -> 49 /*the number seven plus the number fourtytwo*/
print(a) -> 49 /*the number seven plus the number fourtytwo*/
print(b) -> 49 /*the variable b*/