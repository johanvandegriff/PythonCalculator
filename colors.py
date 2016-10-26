#!/usr/bin/python
# Text attributes
END = 0
BOLD = 1
SPECIAL = 2
ITALIC = 3
UNDERLINE = 4
REVERSE = 7
CONCEALED = 8
STRIKE = 9

# Foreground colors
BLACK = 30
D_RED = 31
D_GREEN = 32
D_YELLOW = 33
D_BLUE = 34
D_MAGENTA = 35
D_CYAN = 36
GRAY = 37

D_GRAY = 90
RED = 91
GREEN = 92
YELLOW = 93
BLUE = 94
MAGENTA = 95
CYAN = 96

# Background colors
B_BLACK = 40
B_D_RED = 41
B_D_GREEN = 42
B_D_YELLOW = 43
B_D_BLUE = 44
B_D_MAGENTA = 45
B_D_CYAN = 46
B_L_GRAY = 47

B_GRAY = 100
B_RED = 101
B_GREEN = 102
B_YELLOW = 103
B_BLUE = 104
B_MAGENTA = 105
B_CYAN = 106
B_WHITE = 107

def code(i):
    return '\033[' + str(i) + 'm'

endCode = code(END)

def color(text, color):
    mycode = code(color)
    return mycode + str(text).replace(endCode, endCode + mycode) + endCode

def bold(t): return color(t, BOLD)
def special(t): return color(t, SPECIAL)
def italic(t): return color(t, ITALIC)
def uline(t): return color(t, UNDERLINE)
def rev(t): return color(t, REVERSE)
def concealed(t): return color(t, CONCEALED)
def strike(t): return color(t, STRIKE)

def black(t): return color(t, BLACK)
def Dred(t): return color(t, D_RED)
def Dgreen(t): return color(t, D_GREEN)
def Dyellow(t): return color(t, D_YELLOW)
def Dblue(t): return color(t, D_BLUE)
def Dmagenta(t): return color(t, D_MAGENTA)
def Dcyan(t): return color(t, D_CYAN)
def gray(t): return color(t, GRAY)

def Dgray(t): return color(t, D_GRAY)
def red(t): return color(t, RED)
def green(t): return color(t, GREEN)
def yellow(t): return color(t, YELLOW)
def blue(t): return color(t, BLUE)
def magenta(t): return color(t, MAGENTA)
def cyan(t): return color(t, CYAN)

def Bblack(t): return color(t, B_BLACK)
def BDred(t): return color(t, B_D_RED)
def BDgreen(t): return color(t, B_D_GREEN)
def BDyellow(t): return color(t, B_D_YELLOW)
def BDblue(t): return color(t, B_D_BLUE)
def BDmagenta(t): return color(t, B_D_MAGENTA)
def BDcyan(t): return color(t, B_D_CYAN)
def BLgray(t): return color(t, B_L_GRAY)

def Bgray(t): return color(t, B_GRAY)
def Bred(t): return color(t, B_RED)
def Bgreen(t): return color(t, B_GREEN)
def Byellow(t): return color(t, B_YELLOW)
def Bblue(t): return color(t, B_BLUE)
def Bmagenta(t): return color(t, B_MAGENTA)
def Bcyan(t): return color(t, B_CYAN)
def Bwhite(t): return color(t, B_WHITE)

if __name__ == '__main__':
    print(bold('bold("text")'))
    print(special('special("text")'))
    print(italic('italic("text")'))
    print(uline('uline("text")'))
    print(rev('rev("text")'))
    print(concealed('concealed("text")'))
    print(strike('strike("text")'))
    print('\n')
    print(black('black("text")'))
    print(Dred('Dred("text")'))
    print(Dgreen('Dgreen("text")'))
    print(Dyellow('Dyellow("text")'))
    print(Dblue('Dblue("text")'))
    print(Dmagenta('Dmagenta("text")'))
    print(Dcyan('Dcyan("text")'))
    print(gray('gray("text")'))
    print('\n')
    print(Dgray('Dgray("text")'))
    print(red('red("text")'))
    print(green('green("text")'))
    print(yellow('yellow("text")'))
    print(blue('blue("text")'))
    print(magenta('magenta("text")'))
    print(cyan('cyan("text")'))
    print('\n')
    print(Bblack('Bblack("text")'))
    print(BDred('BDred("text")'))
    print(BDgreen('BDgreen("text")'))
    print(BDyellow('BDyellow("text")'))
    print(BDblue('BDblue("text")'))
    print(BDmagenta('BDmagenta("text")'))
    print(BDcyan('BDcyan("text")'))
    print(BLgray('Blight gray("text")'))
    print('\n')
    print(Bgray('Bgray("text")'))
    print(Bred('Bred("text")'))
    print(Bgreen('Bgreen("text")'))
    print(Byellow('Byellow("text")'))
    print(Bblue('Bblue("text")'))
    print(Bmagenta('Bmagenta("text")'))
    print(Bcyan('Bcyan("text")'))
    print(Bwhite('Bwhite("text")'))
