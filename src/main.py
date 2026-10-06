import sys
import ply.lex as lex
import ply.yacc as yacc

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

tokens = tuple(keywords.values()) + ('MEMORY', 'IDENTIFIER')

t_MEMORY = r'@memory\b'
t_ignore = ' \t\r'


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

  return
  

main()
