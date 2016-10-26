#!/usr/bin/python
import math
import os
import sys
import readline
import random
import re
from collections import Counter
#from colors import *

try: import cPickle as pickle #cPickle is faster than pickle
except: import pickle #if cPickle does not exist, use pickle

#TODO implement: nCr, nPr, xor, !=, >=, <=


#######################    COLORS SETUP    ################################
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


#######################    SETUP    ################################

#unchangeable values
constants = {'e': math.e, 'pi': math.pi, 'phi': 1.61803398875}

#function names are not allowed as variable names
functions = set(['_', 'e', 'pi', 'phi', 'round', 'not', 'abs', 'floor', 'ceil', 'ceiling',
                 'sqrt', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'int', 'ln', 'log',
                 'degrees', 'deg', 'radians', 'rad', 'sinh', 'cosh', 'tanh', 'asinh',
                 'acosh', 'atanh', 'csc', 'sec', 'del', 'expr'])

ops = tuple('^%/*-+<>=&|@') #operations
letters = set('abcdefghijklmnopqrstuvwxyz_')
numbers = set('0123456789.')
steps = echo = False
helpIndex = 0


def tryFloat(num):
    try: return float(num)
    except:
        message = 'invalid symbol'
        if num in functions: message = 'missing argument for function'
        elif num in ops: message = 'missing argument for operator'
        elif num in ('(', ')'): message = 'parentheses error'
        elif num[-1] in numbers: message = 'invalid number'
        elif num[-1] in letters: message = 'uninitialized variable'
        raise ValueError(message + ' "' + str(num) + '"')


def highlight(text):
    if text in ops: return yellow(bold(text))
    if text in functions: return cyan(bold(text))
    return text


#take a string and evaluate it as an expression
#def calculate(expression, echo=False, steps=False):
def calculate(expression, variables={}, steps=False, echo=False):
    if not 'ans' in variables: variables['ans'] = 0
    constants['random'] = random.random()
    #######################    SPLITTER    ################################
    expr = []
    item = ''
    typeOld = "none"
    for char in expression + ' ': #break the expression into items
        if char == '[': char = '(' #convert brackets to parentheses
        if char == ']': char = ')'

        if char in ops: type = "operator" #1 #determine the type of the char
        elif char in letters: type = "letter" #2
        elif char in numbers: type = "number" #3
        elif char in ('(', ')'): type = "parenthesis" #4
        elif char == '!': type = "factorial" #5
#        elif char == '#':
#            expr.append(item)
#            break
        else: type = "unknown" #0
        #make a new item when the types are different or the char is an operation or parenthesis
        if (type != typeOld or type in ("operator", "parenthesis", "factorial")) and not item == '': #(1, 4, 5)
            last = '('
            if len(expr) > 0:
                last = expr[-1]
            if item in constants and last != '@':
                item = str(constants[item]) #replace constants with their values
            elif item in variables and last != '@' and not last == 'del':
                item = str(variables[item]) #replace user variables with their values unless there is a delete command
            if last == '-' and item == '>':
                expr[-1] = '@' #the '@' symbol is used for storing variables, but the user can type '->' and it will be converted here
            elif (last[-1] in numbers or last in (')', '!')) and (item[-1] in numbers or item[-1] in letters or item == '('):
                expr.extend(['*', item]) #detect implied multiplication and add the operator
            elif last == '*' and item == '*': # '**' goes to ^
                expr[-1] = '^'
            elif last in ops and item == '-': #manage sign changes
                if last == '+': # 1+-1
                    expr[-1] = '-'
                elif last == '-': # 1--1
                    expr[-1] = '+'
                else: # 1*-1
#                    expr.extend(['-1', '*'])
                    expr.extend(['_'])
            elif (last == '(' or last in functions) and item == '-':
#                expr.extend(['-1', '*'])
                expr.extend(['_'])
            elif last == '=' and item == '=':
                pass
            elif item != '+' or (item == '+' and not last in ops and not last == '('): #takes care of 1++1, 1*+1, and (+1)
                expr.append(item)
            item = ''
#        if not char == ' ': item += char
        if not type == "unknown": item += char
        typeOld = type #store the type for next time
        ###########    DISPLAY    ###########
        if steps:
            #convert the list to a colored string
            print(
                magenta(bold('[')) + ' '.join(highlight(item2) for item2 in expr) +
                magenta(bold('] [')) + bold(blue(char) + ' (' + str(type) + ')' + magenta(']'))
#                magenta(bold('] [')) + bold(blue(item) + magenta('] [') + red(char) + magenta(']'))
            )
        ###########    END DISPLAY    ###########
    if echo:
        exprStr = ' '.join(highlight(item) for item in expr).replace('@', '->')
    if steps: print(red('---------------------------------'))
    #######################    PARENTHESIS CHECKER    ################################
    parens = 0
    last = ''
    for item in expr:
        if item == '(': parens += 1
        elif item == ')':
            if last == '(': raise ValueError('empty parentheses "()"')
            parens -= 1
            if parens < 0: raise ValueError('unmatched ")"')
        last = item
    if parens > 0:
        if expr[-1] == '(':
            raise ValueError('unmatched "("') #if there is an unmatched ( at the end, raise an error
        else:
            for i in range(parens):
                expr.append(')') #fix unmatched (
    #######################    EVALUATOR    ################################
    markers = [(0, 0)] #this stores the start and stop positions for recursive evaluation
    while len(expr) > 1: #evaluate the expression until it is only one element long
        start, stop = markers[-1] #retrieve the most recent marker
        stop = len(expr) - stop
        ###########    DISPLAY    ############
        if steps:
            leftMarkers = Counter(pair[0] for pair in markers)
            rightMarkers = Counter(len(expr) - pair[1] - 1 for pair in markers)

            for key in range(len(expr)):
                leftMarkers[key] = red(bold('> ' * leftMarkers[key]))
                rightMarkers[key] = red(bold(' <' * rightMarkers[key]))

            out = ['', '', '']
            for i, item in enumerate(expr):
                item = highlight(item)

                posInc = (i >= start) + (i > stop - 1) #inclusive
                posExc = (i > start) + (i >= stop - 1) #exclusive

                out[posExc] += leftMarkers[i]
                if i == stop:
                    out[posInc] += ' '
                out[posInc] += highlight(item)
                out[posExc] += rightMarkers[i]
                if i != stop - 1 and i != len(expr) - 1:
                    out[posInc] += ' '

            print(magenta(bold('[')) + out[0] + uline(out[1]) + out[2] + magenta(bold(']')))
        ###########    END DISPLAY    ############
        subexpr = expr[start:stop] #copy the reigon from start to stop into a sub list
        length = len(subexpr)
        if length < 3 or (length == 3 and subexpr[1] in ops):
            expr = expr[:start] + expr[stop:]
            markers.pop()
            out = subexpr[0]
            if length == 3:
                op = subexpr[1]
                a = tryFloat(subexpr[0])
                b = subexpr[2]
                if op == '@':
                    out = a
                    if b in functions: #disallow function names
                        raise ValueError('illegal variable "' + str(b) + '"')
                    else:
                        store = a
                        if a == int(a): store = int(a)
                        variables[b] = store
                        #setVars(variables)
                else:
                    b = tryFloat(b)
                    if   op == '&': out = int(bool(a and b))
                    elif op == '|': out = int(bool(a or b))
                    elif op == '^': out = a ** b
                    elif op == '%': out = a % b
                    elif op == '/': out = a / b
                    elif op == '*': out = a * b
                    elif op == '-': out = a - b
                    elif op == '+': out = a + b
                    elif op == '=': out = int(a == b)
                    elif op == '>': out = int(a > b)
                    elif op == '<': out = int(a < b)
            elif length == 2:
                op = subexpr[0]
                var = subexpr[1]
                if var == '!': #var and op are switched for factorial
                    out = math.factorial(tryFloat(op))
                elif op == 'del':
                    if var in variables:
                        out = variables[var]
                        del variables[var]
                    else: out = var
                    #setVars(variables)
                else:
                    var = tryFloat(var)
                    if op in ('ceiling', 'ceil'):	out = math.ceil(var)
                    elif op in ('floor', 'int'):	out = math.floor(var)
                    elif op in ('degrees', 'deg'):	out = math.degrees(var)
                    elif op in ('radians', 'rad'):	out = math.radians(var)
                    elif op == '_':		out = -var
                    elif op == 'abs':	out = abs(var)
                    elif op == 'acosh':	out = math.acosh(var)
                    elif op == 'acos':	out = math.acos(var)
                    elif op == 'asinh':	out = math.asinh(var)
                    elif op == 'asin':	out = math.asin(var)
                    elif op == 'atanh':	out = math.atanh(var)
                    elif op == 'atan':	out = math.atan(var)
                    elif op == 'cosh':	out = math.cosh(var)
                    elif op == 'cos':	out = math.cos(var)
                    elif op == 'cot':	out = 1.0 / math.tan(var)
                    elif op == 'csc':	out = 1.0 / math.sin(var)
                    elif op == 'ln':	out = math.log(var)
                    elif op == 'log':	out = math.log10(var)
                    elif op == 'not':	out = int(not var)
                    elif op == 'round':	out = int(var + 0.5)
                    elif op == 'sec':	out = 1.0 / math.cos(var)
                    elif op == 'sinh':	out = math.sinh(var)
                    elif op == 'sin':	out = math.sin(var)
                    elif op == 'sqrt':	out = math.sqrt(var)
                    elif op == 'tanh':	out = math.tanh(var)
                    elif op == 'tan':	out = math.tan(var)
            elif length == 1:
                out = subexpr[0]
            expr.insert(start, str(out))
        else:
            i = start
            while expr[i] != '(' and i < stop - 1: i += 1
            if i < stop - 1:
                newStart = i
                i += 1
                parens = 1
                while parens > 0:
                    if i > stop:
                        raise ValueError('unmatched "("')
                    if expr[i] == '(': parens += 1
                    if expr[i] == ')': parens -= 1
                    i += 1
                expr.pop(i - 1)
                expr.pop(newStart)
                markers.append((newStart, len(expr) - i + 2))
            else:
                i = start
                while i < stop - 1 and not (expr[i][-1] in letters and expr[i + 1][-1] in numbers) and not (expr[i] == 'del' and expr[i + 1][-1] in letters) and not (expr[i][-1] in numbers and expr[i + 1] == '!'):
                    i += 1
                if i < stop - 1:
                    markers.append((i, len(expr) - i - 2))
                else:
                    i = 0
                    while i < len(ops):
                        j = start
                        while expr[j] != ops[i] and j < stop - 1:
                            j += 1
                        if j < stop - 1:
                            break
                        i += 1
                    if j >= stop:
                        return None #TODO
                    markers.append((j - 1, len(expr) - j - 2))
    #######################    RESULT FORMATTER    ################################
    result = tryFloat(expr[0])
    result = round(result, 11) #round to 11 decimal places to avoid machine precision error
    if int(result) == result:
        result = int(result)
    variables['ans'] = result
    #setVars(variables)
    if echo:
        variables['expr'] = exprStr
    return variables


help = ['''Commands:
<tab>		autocomplete command
clear		clear the screen
echo [on]	display the expression as part of the result
echo off	do not display the expression
examples	sample expressions
exit, quit	exit the program
help <page>	look at a page of this help text
reset		delete all the user variables
silent		turn both steps and echo off
vars		display variables
verbose		turn both steps and echo on
steps [on]	show steps taken to solve the expression
steps off	hide steps taken

Constants:
e	2.71828182846
pi	3.14159265359
phi	1.61803398875''',

        '''Other Variables
random	random number from 0 to 1
ans	value of the last calculation

Operators:
+	addition
-	subtraction
*	multiplication
/	division
**, ^	exponent
%	remainder
=	equal to (boolean)
<	less than (boolean)
>	greater than (boolean)
&	and (boolean)
|	or (boolean)
!	factorial
_	unary minus (times -1)
->, @	store (e.g. 10->var)''',

#removed:
#	comment (ignore everything after)

        '''Functions:
abs		absolute value
acos		arccosine
acosh		hyperbolic arccosine
asin		arcsine
asinh		hyperbolic arcsine
atan		arctangent
atanh		hyperbolic arctangent
ceiling, ceil	round up
cos		cosine
cosh		hyperbolic cosine
cot		cotangent (1/tan)
csc		cosecant (1/sin)'
degrees, deg	convert radians to degrees''',
        '''del		delete a variable
floor, int	round down
ln		natural logarithm
log		logarithm (base 10)
not		inverse (boolean)
radians, rad	convert degrees to radians
round		round to the nearest integer
sec		secant (1/cos)
sinh		hyperbolic sine
sin		sine
sqrt		square root
tanh		hyperbolic tangent
tan		tangent''']

examples = '''steps;123*sin(4!rad(56+log4))/(3+ln(3!))
steps off;echo;3->a;2->b;a+b;a*b;a/b;a%b;a!(a+b);sqrt(a**2+b**2);vars
'''

commands = ['clear', 'echo', 'echo off', 'echo on', 'examples', 'exit', 'help',
            'quit', 'reset', 'silent', 'steps', 'steps off', 'steps on', 'vars']
for i in range(len(help)): commands.append('help' + str(i))

varsFile = os.path.join(os.path.expanduser('~'), '.calc') #user-defined variables


def getVars():
    try: #try to read the file, otherwise make a new dict
        return pickle.load(open(varsFile, 'rb'))
    except:
        return {}


def setVars(variables): #write to the file
    pickle.dump(variables, open(varsFile, 'wb'))


def command(expression):
    global steps, echo, helpIndex
    expression = str(expression).lower() #convert the expression to lowercase
    expr = expression.strip() #temporarily remove whitespace
    if expr in ('exit', 'quit'): quit()
    if expr == 'echo on' or expr == 'echo':
        echo = True
        print(green('echo mode is ON'))
    elif expr == 'echo off':
        echo = False
        print(red('echo mode is OFF'))
    elif expr == 'steps on' or expr == 'steps':
        steps = True
        print(green('steps mode is ON'))
    elif expr == 'steps off':
        steps = False
        print(red('steps mode is OFF'))
    elif expr == 'silent':
        steps = echo = False
        print(red('echo mode is OFF\nsteps mode is OFF'))
    elif expr == 'verbose':
        steps = echo = True
        print(green('echo mode is ON\nsteps mode is ON'))
    elif expr == 'examples':
        print(yellow(uline('Examples:\n')) + bold(blue(examples)) + '\n')
    elif expr == 'clear': #clear variables
        os.system('clear')
    elif expr[:4] == 'help':
        os.system('clear')
        page = expr[4:].strip()
        try:
            page = int(page)
            if page > len(help): page = len(help)
            if page < 1: page = 1
            helpIndex = page - 1
        except:
            page = helpIndex + 1
            helpIndex = (helpIndex + 1) % (len(help))
        print(yellow(uline('Help page ' + str(page) + '/' + str(len(help)))) + '\n' + bold(blue(help[page - 1])) + '\n')
    elif expr == 'reset': #delete variables
        variables = {}
        setVars(variables)
        print(green('all variables deleted'))
    else:
        variables = getVars() #retrieve the variables from the file
        if expr == 'vars':
          print(re.sub("['{}]", '', str(variables).replace(', ', ',\n'))) #display variables
          return
        variables = calculate(expression, variables, steps, echo)
        result = str(variables['ans'])
        if echo:
            result = variables['expr'] + bold(green(' = ')) + result
            del variables['expr']
        if len(result) > 0:
            print(result)
        setVars(variables)

#use the calculate function multiple times
#entries are separated by: , ; \n
def multiCommand(expression):
    for expr in re.findall(r'[^,;\n]+', expression):
        command(expr)


def completer(text, state):
        options = [x for x in commands if x.startswith(text)]
        try:
                return options[state]
        except IndexError:
                return None


def console():
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    print(blue(bold('Type help for more info.')))
#    print(blue(bold('Welcome to the coolest calculator ever!\nType help for more info.')))

    prompt = bold(cyan('~ '))
    lastCommand = ''
    try:
        while True:
            #TODO fix buggy input field
            try:
                command = raw_input(prompt)
            except NameError:
                command = input(prompt)
            if command.strip() == '':
                command = lastCommand
            try:
                multiCommand(command)
            except Exception as e:
                print(uline(Dred(e)))
            lastCommand = command
    except (KeyboardInterrupt, EOFError) as e:
        print('')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        for expr in sys.argv[1:]:
            multiCommand(expr)
#        multiCommand(' '.join(sys.argv[1:]))
    else:
        console()
