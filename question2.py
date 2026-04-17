"""
HIT137 Group Assignment 2, Question 2
=======================================================
Reads mathematical expressions from a text file (one per line),
evaluates each using a hand-written recursive-descent parser, and
writes an output file with four lines per expression:
    Input   - the original expression string
    Tree    - the parse tree in prefix notation, or ERROR
    Tokens  - the token stream in [TYPE:value] format, or ERROR
    Result   - the computed numeric result, or ERROR

Supported features: 


  - Four binary operators:  +  -  *  /
  - Correct operator precedence (* / before + -)
  - Parenthesised sub-expressions (nested to any depth)
  - Unary negation:  -5,  --5,  -(3+4),  3 * -2
  - Unary + is NOT supported (produces ERROR)
  - Implicit multiplication:  2(3+4)  →  (* 2 (+ 3 4))
  - Integer results displayed without decimal point (8 not 8.0)
  - Non-integer results rounded to 4 decimal places
  - Division by zero produces ERROR (tree still shown)
  - Unknown characters produce ERROR on all four lines

"""

import os

#  TOKENISER

def tokenise(expression):
    """
    Convert an expression string into a list of (TYPE, value) tuples.

    """
    tokens = []
    i = 0
    s = expression.strip()

    while i < len(s):
        ch = s[i]

        if ch in ' \t':
            i += 1
            continue

        if ch.isdigit() or (ch == '.' and i + 1 < len(s) and s[i + 1].isdigit()):
            j = i
            while j < len(s) and (s[j].isdigit() or s[j] == '.'):
                j += 1
            tokens.append(('NUM', s[i:j]))
            i = j
            continue

        if ch in '+-*/':
            tokens.append(('OP', ch))
            i += 1
            continue

        if ch == '(':
            tokens.append(('LPAREN', ch))
            i += 1
            continue

        if ch == ')':
            tokens.append(('RPAREN', ch))
            i += 1
            continue

        return None

    tokens.append(('END', ''))
    return tokens


def format_tokens(tokens):
    """
    Render a token list as the required output string.
    Example:  [NUM:3] [OP:+] [NUM:5] [END]
    """
    parts = []
    for typ, val in tokens:
        if typ == 'END':
            parts.append('[END]')
        else:
            parts.append(f'[{typ}:{val}]')
    return ' '.join(parts)


#  PARSER  (recursive descent)


def _current(state):
    """Return the token at the current position without advancing."""
    return state['tokens'][state['pos']]

def _consume(state):
    """Return the current token and advance the position by one."""
    tok = state['tokens'][state['pos']]
    state['pos'] += 1
    return tok

def _peek_type(state):
    """Return the type of the current token."""
    return _current(state)[0]

def _peek_val(state):
    """Return the value of the current token."""
    return _current(state)[1]


# grammar rules 

def _parse_expression(state):
    """
    Top-level entry point.  Parses a complete expression and checks
    that no tokens remain afterwards.
    """
    node = _parse_add(state)
    if _peek_type(state) != 'END':
        raise ValueError(
            f"Unexpected token after expression: {_current(state)}"
        )
    return node


def _parse_add(state):
    """
    Handle addition and subtraction (lowest precedence, left-associative).
    add_expr ::= mul_expr ( ('+' | '-') mul_expr )*
    """
    left = _parse_mul(state)
    while _peek_type(state) == 'OP' and _peek_val(state) in ('+', '-'):
        op = _consume(state)[1]
        right = _parse_mul(state)
        left = (op, left, right)
    return left


def _parse_mul(state):
    """
    Handle multiplication, division, and implicit multiplication
    (middle precedence, left-associative).
    mul_expr ::= unary ( ('*' | '/') unary | unary )*
    """
    left = _parse_unary(state)
    while True:
        # explicit * or /
        if _peek_type(state) == 'OP' and _peek_val(state) in ('*', '/'):
            op = _consume(state)[1]
            right = _parse_unary(state)
            left = (op, left, right)
        # implicit multiplication: a number or '(' immediately follows
        elif _peek_type(state) in ('NUM', 'LPAREN'):
            right = _parse_unary(state)
            left = ('*', left, right)
        else:
            break
    return left


def _parse_unary(state):
    """
    Handle unary negation (right-associative, higher precedence than binary ops).
    Unary '+' is explicitly rejected as per the spec.
    unary ::= '-' unary | primary
    """
    if _peek_type(state) == 'OP' and _peek_val(state) == '-':
        _consume(state)                        # discard the '-'
        operand = _parse_unary(state)          # right-associative
        return ('neg', operand)

    if _peek_type(state) == 'OP' and _peek_val(state) == '+':
        raise ValueError("Unary '+' is not supported")

    return _parse_primary(state)


def _parse_primary(state):
    """
    Handle numeric literals and parenthesised sub-expressions.
    primary ::= NUM | '(' add_expr ')'
    """
    typ, val = _current(state)

    if typ == 'NUM':
        _consume(state)
        return float(val)

    if typ == 'LPAREN':
        _consume(state)                        
        node = _parse_add(state)               
        if _peek_type(state) != 'RPAREN':
            raise ValueError("Missing closing parenthesis ')'")
        _consume(state)                        
        return node

    raise ValueError(f"Unexpected token in primary position: {_current(state)}")



#  TREE FORMATTER


def format_tree(node):
    """
    Recursively render an AST node as a prefix-notation string.

    number literal  →  its integer or float string (no trailing .0)
    binary op       →  (op left right)
    unary negation  →  (neg operand)
    """
    if isinstance(node, float):
        return str(int(node)) if node == int(node) else str(round(node, 4))

    if isinstance(node, tuple):
        if node[0] == 'neg':
            return f'(neg {format_tree(node[1])})'
        op, left, right = node
        return f'({op} {format_tree(left)} {format_tree(right)})'

    return str(node)


