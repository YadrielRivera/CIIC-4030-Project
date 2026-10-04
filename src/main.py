import sys
import ply.lex as lex
import ply.yacc as yacc

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
