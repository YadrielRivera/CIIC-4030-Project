import sys
import ply.lex as lex
import ply.yacc as yacc

def OpenFile():
  file_name = sys.argv[1]

  if (not ".uedge" in file_name):
    print("Error: Invalid file type")
    return None

  fd = open(file_name, 'r')
  # This code only tests that the file contents are being received
  # print("Successfully accessed file for read.")
  # print("Showing file contents...\n")

  # for exp in fd:
  #   print(exp)
  # print("EOF")

  return fd


def main() -> int:

  if (len(sys.argv) < 1):
    print("Error: invalid argument count.")
    return -1
  
  file = OpenFile()

  if (not file):
    print("File output is None")
    return -1

  return 0
  

main()