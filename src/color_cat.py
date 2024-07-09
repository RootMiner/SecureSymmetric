# prints plain text data on terminal in beautified way
from rich.panel import Panel
from rich.syntax import Syntax
from rich.console import Console
from pygments.util import ClassNotFound
from pygments.lexers import guess_lexer_for_filename

from src.colors import *

# prints plain text data directly on terminal interface
def print_decrypted_data(dec_data, mod_file_name):
  try:
    content = dec_data.decode('UTF-8')
    try:
      lexer = guess_lexer_for_filename(mod_file_name, content)
      # Themes : monokai, dracula, solarized-dark
      syntax = Syntax(content, lexer, theme="dracula", line_numbers=True)
      console = Console()
      syntax_with_border = Panel(syntax, title=mod_file_name)
      console.print(syntax_with_border)
    except ClassNotFound: 
      print(f"\n[{E}] No valid file extension, trying to read..\n")
      print(dec_data.decode('UTF-8')) 
      pass
  except UnicodeDecodeError: print(f"[{E}] Error reading data in {R}{mod_file_name}{r}")