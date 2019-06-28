from globalTypes import *
from lexer import *
from parser import *



f = open('sample.txt', 'r')
programa = f.read()     # lee todo el archivo a compilar
progLong = len(programa)   # longitud original del programa
programa = programa + '$'   # agregar un caracter $ que represente EOF
posicion = 0       # posición del caracter actual del string
# función para pasar los valores iniciales de las variables globales
globales(programa, posicion, progLong)
token = None
while (True):
    token = getToken()
    tokenList.append(token[0])
    tokenListValues.append(token[1])
    if(token[0] == TokenType.ENDFILE):
        break

AST = parser(True)