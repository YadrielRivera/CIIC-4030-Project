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


lexer = lex.lex()

# Parser START
start = 'program'

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
   #TO DO: 'statement' grammar rule must be defined before the complete parser can be initialized. 
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

#TO DO: Catch MemoryAnnotationError in main() during parser integration to report invalid units without a traceback
class MemoryAnnotationError(Exception):
    pass


def p_unit(p):
   'unit : IDENTIFIER'
   
   valid_units = {
      'kb', 'Mb', 'Gb', 'Tb', 'Pb', 'Eb', 'Zb', 'Yb',
   }
   if p[1] not in valid_units:
      raise MemoryAnnotationError(
         f"Error: invalid memory unit '{p[1]}' "
         f"at line {p.lineno(1)}"
      )
   p[0] = p[1]

def p_function_def(p):
   # TO DO: 'block' grammar rule must be implemented before the complete parser can be initialized.
   """function_def : FUNC IDENTIFIER '(' param_list_opt ')' block"""

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

# Parser END

def OpenFile():
  file_name = sys.argv[1]

  if (not ".uedge" in file_name):
    print("Error: Invalid file type")
    return None

  fd = open(file_name, 'r')

  return fd


def main():

  if (len(sys.argv) < 1):
    print("Error: invalid argument count.")
    return
  
  file = OpenFile()

  if (not file):
    print("File output is None")
    return

  #numbertest.uedge Testing
  # data = file.read()          
  # file.close()                

  # lexer.input(data)           
  # for tok in lexer:           
      # print(tok)              

  return
  

main()
