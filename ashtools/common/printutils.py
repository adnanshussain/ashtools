from collections import namedtuple
import logging

# define a named tuple for color and font weight
Color = namedtuple("Color", "ascii")

YELLOW = Color(ascii="\033[0;33m")
GREEN = Color(ascii="\033[0;32m")
BRIGHT_GREEN = Color(ascii="\033[92m")
GREEN_BOLD = Color(ascii="\033[1;32m")
GREEN_BOLD_ITALIC = Color(ascii="\033[1;3;32m")
ORANGE = Color(ascii="\033[0;91m")
RED = Color(ascii="\033[0;31m")
RED_BOLD = Color(ascii="\033[1;31m")
BRIGHT_RED = Color(ascii="\033[91m")
RESET = Color(ascii="\033[0m")

# print('\033[0;31m' + 'This text is red.' + '\033[0m')
print_seperator_line = lambda len=120: print(GRAY + "-" * len + RESET)
print_bold = lambda msg: print(BOLD + msg + RESET)
print_italic = lambda msg: print(ITALIC + msg + RESET)
