import sys
import ply.lex as lex
import ply.yacc as yacc

# Lexing code

keywords = {
  'let': 'LET',
  'func': 'FUNC',
  'if': 'IF',
  'else': 'ELSE',
  'while': 'WHILE',
  'for': 'FOR',
  'return': 'RETURN',
  'print': 'PRINT',
  'true': 'TRUE',
  'false': 'FALSE',
}

literals = [';', '(', ')', '{', '}', ','] # Special symbols

tokens = tuple(keywords.values()) + ('MEMORY', 'IDENTIFIER', 'INTEGER', 'FLOAT', 'ASSIGN',
                                     'PLUS', 'MINUS', 'MULTIPLY', 
                                     'DIVIDE', 'MODULO', 'EQUALS', 'NOTEQUALS', 
                                     'LESSTHAN', 'GREATERTHAN', 'LESSTHANEQUAL'
                                     , 'GREATERTHANEQUAL', 'STRING')

#Operators
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_EQUALS = r'=='
t_ASSIGN = r'=' 
t_NOTEQUALS = r'!='
t_LESSTHAN = r'<'
t_GREATERTHAN = r'>'
t_LESSTHANEQUAL = r'<='
t_GREATERTHANEQUAL = r'>='

t_MEMORY = r'@memory\b'
t_ignore = ' \t\r'


def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFIER(t):
  r'[A-Za-z_][A-Za-z0-9_]*'
  t.type = keywords.get(t.value, 'IDENTIFIER')
  return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'//.*'
    pass

def t_STRING(t):
    r'"[^"]*"'
    # Strip the surrounding quotes to get the actual value
    t.value = t.value[1:-1]
    return t

def t_error(t):
    print(f"Error: unexpected token ‘{t.value[0]}’ at line {t.lineno}") #Retrieves first unrecognized character from line number maintained by the lexer
    sys.exit(0)

lexer = lex.lex()

# Parser START
start = 'program'

precedence = (
  ('left', 'EQUALS', 'NOTEQUALS', 'LESSTHAN', 'GREATERTHAN',
   'LESSTHANEQUAL', 'GREATERTHANEQUAL'),
  ('left', 'PLUS', 'MINUS'),
  ('left', 'MULTIPLY', 'DIVIDE', 'MODULO'),
)

def p_program(p):
   'program : top_level_elements'
   p[0] = {
      'type': 'program', 
      'body': p[1]
   }

def p_top_level_elements_multiple(p):
   'top_level_elements : top_level_elements top_level_element'
   p[0] = p[1] + [p[2]]

def p_top_level_elements_empty(p):
   'top_level_elements : empty'
   p[0] = []

def p_top_level_element(p):
   '''top_level_element : decorator function_def 
                        | function_def 
                        | statement'''
   
   if len(p) == 3:
      p[0] = p[2]
      p[0]['memory'] = p[1]
   else:
      p[0] = p[1]

def p_decorator(p):
   "decorator : MEMORY '(' INTEGER unit ')'"
   p[0] = {
      'type': 'memory_annotation',
      'amount': p[3],
      'unit': p[4],
      'line': p.lineno(1)
   }


def p_unit(p):
   'unit : IDENTIFIER'
   
   valid_units = {
      'kb', 'Mb', 'Gb', 'Tb', 'Pb', 'Eb', 'Zb', 'Yb',
   }
   if p[1] not in valid_units:
      print(f"Error: invalid memory unit '{p[1]}' at line {p.lineno(1)}")
      sys.exit(0)

   p[0] = p[1]

def p_function_def(p):
   """function_def : FUNC IDENTIFIER '(' param_list_opt ')' block_stmt"""

   p[0] = {
        'type': 'function',
        'name': p[2],
        'params': p[4],
        'body': p[6],
        'memory': None,   #p_top_level_element() recognizes if a memory decorator is present and assigns it to this field
        'line': p.lineno(1)
    }

def p_param_list_opt_present(p):
    'param_list_opt : param_list'
    p[0] = p[1]

def p_param_list_opt_empty(p):
    'param_list_opt : empty'
    p[0] = []

def p_param_list_single(p):
    'param_list : IDENTIFIER'
    p[0] = [p[1]]

def p_param_list_multiple(p):
   "param_list : param_list ',' IDENTIFIER"
   p[0] = p[1] + [p[3]]

def p_empty(p):
   'empty :'
   p[0] = None

#Assig statement, Let x = expression   
def p_assing_stmt(p):
    'assing_stmt : LET IDENTIFIER ASSIGN expression'
    
    p[0] = {
        'type' : 'assignment',
        'target' : p[2],
        'value' : p[4],
        'line' : p.lineno(1)
    }
    
#Update statement, x = new expression
def p_update_stmt(p):
    'update_stmt : IDENTIFIER ASSIGN expression'
    p[0] = {
      'type': 'update',
      'target' : p[1],
      'value' : p[3],
      'line' : p.lineno(1)
    }

def p_for_loop(p):
    'for_loop : FOR "(" init_stmt expression ";" update_expr ")" block_stmt'
    p[0] = {
      'type': 'for',
      'init': p[3],
      'condition': p[4],
      'update': p[6],
      'body': p[8],
      'line': p.lineno(1)
    }

def p_init_stmt(p):
    '''init_stmt : assing_stmt ';'
                 | update_stmt ';'
                 | ';' '''
    p[0] = None if len(p) == 2 else p[1]

def p_update_expr(p):
    'update_expr : update_stmt'
    p[0] = p[1]
    
#Return statement, return expression
def p_return_stmt(p):
    '''return_stmt : RETURN expression
                   | RETURN'''
    if len(p) == 3:
        p[0] = {
            'type': 'return',
            'value': p[2],
            'line': p.lineno(1)
        }
    else:
        p[0] = {
            'type': 'return',
            'value': None,
            'line': p.lineno(1)
        }
    
#Expression statement, expression;
def p_expr_stmt(p):
    'expr_stmt : expression'
    p[0] = {
      'type': 'expression_statement',
      'expression' : p[1],
      "line" : p[1].get('line') if isinstance(p[1], dict) else None
    }
    
#Statement list, multiple statements
def p_statement_list_multiple(p):
    'statement_list : statement_list statement'
    p[0] = p[1] + [p[2]]
    
#statement list, empty statement   
def p_statement_list_empty(p):
    'statement_list : empty'
    p[0] = []
    
#Statement, can be assig, update, return, expression, print or block statement
def p_statement(p):
    '''statement : assing_stmt ';' 
                | update_stmt ';' 
                | return_stmt ';' 
                | expr_stmt ';' 
                | if_stmt 
                | for_loop
                | while_stmt
                | block_stmt'''
    p[0] = p[1]

def p_while_stmt(p):
  'while_stmt : WHILE "(" expression ")" block_stmt'
  p[0] = {
    'type': 'while',
    'condition': p[3],
    'body': p[5],
    'line': p.lineno(1)
  }

#Print statement, print(expression);
def p_expression_print(p):
    'expression : PRINT "(" expression ")"'
    p[0] = {
      'type' : 'print',
      'value' : p[3],
      'line' : p.lineno(1)
    }

# Binary Operations, which precedence is handled by the precedence tuple above.
def p_expression_binary(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULTIPLY expression
                  | expression DIVIDE expression
                  | expression MODULO expression
                  | expression EQUALS expression
                  | expression NOTEQUALS expression
                  | expression LESSTHAN expression
                  | expression GREATERTHAN expression
                  | expression LESSTHANEQUAL expression
                  | expression GREATERTHANEQUAL expression'''
    p[0] = {
        'type': 'binary',
        'op': p[2],
        'left': p[1],
        'right': p[3],
        'line': p[1].get('line') if isinstance(p[1], dict) else p.lineno(2)
    }

# An expression can be a single term.
def p_expression_term(p):
    'expression : term'
    p[0] = p[1] 

# Terms are literals, identifiers, function calls, or parenthesized expressions.
def p_term_num_literal(p):
    'term : num_literal'
    p[0] = p[1]

def p_term_string(p):
    'term : STRING'
    p[0] = {
        'type': 'string',
        'value': p[1],
        'line': p.lineno(1)
    }

def p_term_bool_true(p):
    'term : TRUE'
    p[0] = {
        'type': 'boolean',
        'value': True,
        'line': p.lineno(1)
    }

def p_term_bool_false(p):
    'term : FALSE'
    p[0] = {
        'type': 'boolean',
        'value': False,
        'line': p.lineno(1)
    }

def p_term_identifier(p):
    'term : IDENTIFIER'
    p[0] = {
        'type': 'identifier',
        'name': p[1],
        'line': p.lineno(1)
    }

def p_term_function_call(p):
    'term : function_call'
    p[0] = p[1]

def p_term_paren(p):
    'term : "(" expression ")"'
    p[0] = p[2]   # keep the inner expression; parentheses only group


# Numeric literals.
def p_num_literal_integer(p):
    'num_literal : INTEGER'
    p[0] = {
        'type': 'number',
        'value': p[1],
        'line': p.lineno(1)
    }

def p_num_literal_float(p):
    'num_literal : FLOAT'
    p[0] = {
        'type': 'number',
        'value': p[1],
        'line': p.lineno(1)
    }

# Function calls: name(args...)
def p_function_call(p):
    'function_call : IDENTIFIER "(" arg_list_opt ")"'
    p[0] = {
        'type': 'call',
        'callee': p[1],
        'args': p[3],
        'line': p.lineno(1)
    }

# Optional argument list.
def p_arg_list_opt_present(p):
    'arg_list_opt : arg_list'
    p[0] = p[1]

def p_arg_list_opt_empty(p):
    'arg_list_opt : empty'
    p[0] = []

# One or more arguments separated by commas.
def p_arg_list_single(p):
    'arg_list : expression'
    p[0] = [p[1]]

def p_arg_list_multiple(p):
    'arg_list : arg_list "," expression'
    p[0] = p[1] + [p[3]]
    
#Block statement, { statement_list }   
def p_block_stmt(p):
    'block_stmt :  "{" statement_list "}" '
    p[0] = {
      'type' : 'block',
      'statements' : p[2],
      'line' : p.lineno(1)
    }

#If statement, if (expression) block else_opt
def p_if_stmt(p):
    'if_stmt : IF "(" expression ")" block_stmt else_opt'
    p[0] = {
      'type' : 'if',
      'condition' : p[3],
      'then' : p[5],
      'else' : p[6],
      'line' : p.lineno(1)
    }
    
# Optional else statement, else block or empty   
def p_else_opt(p):
    '''else_opt : ELSE block_stmt
                | empty'''
    p[0] = p[2] if len(p) == 3 else None

# Parser END

def p_error(p):
  if p:
    print(f"Syntax error at line {p.lineno}: unexpected token {p.value!r}")
  else:
    print(f"Syntax error at end of input at line {lexer.lineno}")

  sys.exit(0)


parser = yacc.yacc()


def parse(source):
  lexer.lineno = 1
  return parser.parse(source, lexer=lexer)


def OpenFile():
   file_name = sys.argv[1]

   if not file_name.endswith(".uedge"):
      print("Error: Invalid file type")
      return None

   fd = open(file_name, 'r')

   return fd


def main():

  if len(sys.argv) < 2:
      print("Error: invalid argument count.")
      return
  
  file = OpenFile()

  if (not file):
      print("File output is None")
      return

  with file:
      parse(file.read())

  print("Parsed successfully")
  

if __name__ == '__main__':
   main()
