"""
Associate syntactic elements like "*" recognized
by the parser with semantic classes like TIMES in 
the expr module.

We limit the definitions here to binary (TIMES, PLUS, 
etc) and unary (NEG) operators, whose lexical 
representations are literal strings like *, +, and ~. 
Patterns for numeric constants and identifiers are 
built into the lexical analyzer and not defined 
here to avoid regular expression hell. Take CIS 461 
if you want to learn a more general way to do this. 
"""

import expr

# Category names  (used in parsing)
ASSIGN = "ASSIGN" # Right operand must be a variable
TERNOP = "TERNOP"  # Extra credit
BINOP = "BINOP"   # (number, number) -> number  like Times, Plus
UNOP = "UNOP"     # (number) -> number like Neg
CONST = "CONST"
IDENT = "IDENT"

# Each kind of operation node should be bound to a
# symbol and class here (excluding CONST and IDENT)
OPS = {
    "=": (ASSIGN, expr.Assign)
    , "~": (UNOP, expr.Neg)
     , "*": (BINOP, expr.Times)
     , "+": (BINOP, expr.Plus)
     , "-": (BINOP, expr.Minus)
     , "/": (BINOP, expr.Div)
     , "if": (TERNOP, expr.If) # extra credit 'if' creation
}
