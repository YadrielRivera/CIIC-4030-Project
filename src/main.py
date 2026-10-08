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

literals = [';', '(', ')', '{', '}'] # Special symbols

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
