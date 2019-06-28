#Enrique Lira Martinez A01023351

from globalTypes import *

def globales(prog, pos, long):

    global codigo
    global posicion #posicion del caracter que se esta analizando 
    global Longitud#longitud del codigo analizando
    codigo = prog
    posicion = pos
    Longitud = long

def getToken(imprime = False):
    global posicion
    #ignoring any space newline or tab character
    while(codigo[posicion] == ' ' or codigo[posicion] == '\n' or codigo[posicion]== '\t'):
        posicion += 1
    #ignoring comments
    if(codigo[posicion] == '/'):
        if(codigo[posicion+1] == '*'):
            while(True):
                posicion += 1
                if(codigo[posicion] == '*'):
                    if(codigo[posicion+1] == '/'):
                        posicion+= 2
                        break
    while(codigo[posicion] == ' ' or codigo[posicion] == '\n' or codigo[posicion]== '\t'):
        posicion += 1
    if(codigo[posicion] == '$'):
        return (printToken(TokenType.ENDFILE, '$', imprime, 1))
    elif(codigo[posicion] == '+'):
        return (printToken(TokenType.PLUS, '+', imprime, 1))
    elif(codigo[posicion] == '-'):
        return (printToken(TokenType.MINUS, '-', imprime, 1))
    elif(codigo[posicion] == ';'):
        return (printToken(TokenType.SEMICOLON, ';', imprime, 1))
    elif(codigo[posicion] == ','):
        return (printToken(TokenType.COMMA, ',', imprime, 1))
    elif(codigo[posicion] == '('):
        return (printToken(TokenType.OPEN_PARENTHESIS, '(', imprime, 1))
    elif(codigo[posicion] == ')'):
        return (printToken(TokenType.CLOSE_PARENTHESIS, ')', imprime,1 ))
    elif(codigo[posicion] == '['):
        return (printToken(TokenType.OPEN_BRACKETS, '[', imprime, 1))
    elif(codigo[posicion] == ']'):
        return (printToken(TokenType.CLOSE_BRACKETS, ']', imprime, 1))
    elif(codigo[posicion] == '{'):
        return (printToken(TokenType.OPEN_KEYS, '{', imprime, 1))
    elif(codigo[posicion] == '}'):
        return (printToken(TokenType.CLOSE_KEYS, '}', imprime, 1))
    elif(codigo[posicion] == '<'):
        if(codigo[posicion+1] == '='):
            return (printToken(TokenType.LESS_THAN_EQUAL_TO, '<=', imprime, 2))
        return (printToken(TokenType.LESS_THAN, '<', imprime, 1))
    elif(codigo[posicion] == '>'):
        if(codigo[posicion+1] == '='):
            return (printToken(TokenType.GREATER_THAN_EQUAL_TO, '>=', imprime, 2))
        return (printToken(TokenType.GREATER_THAN, '>', imprime, 1))
    elif(codigo[posicion] == '*'):
        return (printToken(TokenType.ASTERISK, '*', imprime, 1))
    elif(codigo[posicion] == '/'):
        return (printToken(TokenType.SLASH, '/', imprime, 1))
    elif(codigo[posicion] == '='):
        if(codigo[posicion+1] == '='):
            return (printToken(TokenType.EQUAL, '==', imprime, 2))
        return (printToken(TokenType.ASSIGNMENT, '=', imprime, 1))
    elif(codigo[posicion] == '!'):
        if(codigo[posicion+1] == '='):
            return (printToken(TokenType.DIFFERENT, '!=', imprime, 2))
        else:
            return(printToken(TokenType.ERROR, 'error', imprime, 2, "Error en la formacion de expresion", posicion))
    elif(codigo[posicion].isalpha()):
        size = 1# variable para almacenar el tamano del string 
        token = codigo[posicion]
        while(True):
            if(codigo[posicion+size].isalnum()):#mientras no se algo diferente a un numero
                token += codigo[posicion + size]#agregamos al token cada letra con su tamano 
                size +=1
            else:
                break#si la palabra es una palabra reservada de c tiny 
        if(token == 'else'):
            return (printToken(TokenType.ELSE, token, imprime, size))
        elif(token == 'if'):
            return (printToken(TokenType.IF, token, imprime, size))
        elif(token == 'int'):
            return (printToken(TokenType.INT, token, imprime, size))
        elif(token == 'return'):
            return (printToken(TokenType.RETURN, token, imprime, size))
        elif(token == 'void'):
            return (printToken(TokenType.VOID, token, imprime, size))
        elif(token == 'while'):
            return (printToken(TokenType.WHILE, token, imprime, size))
        else:
            return(printToken(TokenType.ID, token, imprime, size))
    elif(codigo[posicion].isdigit()):
        size = 1
        token = codigo[posicion]
        while(True):
            if(codigo[posicion+size].isdigit()):
                token += codigo[posicion + size]
                size +=1
            elif(codigo[posicion + size].isalpha()):
                pos = posicion + size
                PosError = posicion + size
                while(True):
                    if(codigo[posicion+size] == ' ' or codigo[posicion+size] == '\n' or codigo[posicion+size] == '\t'):
                        return(printToken(TokenType.ERROR, 'error', imprime, size, "Error en la formacion de un entero", PosError))
                    else:
                        size += 1
            else:
                break
        return(printToken(TokenType.NUM, token, imprime, size))
    else:
        return(printToken(TokenType.ERROR, 'error', imprime, 1))

def printToken(TokenType, valor, imprime, longitud, MessajeError = "", PosError = 0):#funcion para imprimir los token encontrados asi sea un error 
    global posicion
    posicion += longitud
    if(valor == 'error'):#si el token es un error entonces este se ira a la funcion de imprimir error
        printError(PosError, MessajeError)
    if(imprime):
        print("(", TokenType, ",", valor, ")")#si no imprime el token 
    return(TokenType, valor)

def printError(posicion, MessajeError):# funcion para identificar la linea del error 
    lineaError = posicion
    print("Linea : ", MessajeError )#imprimimos la linea del error
    while(True):
        lineaError -= 1
        if(codigo[lineaError] == '\n'):
            break
    pos = lineaError
    while(True):#encontramos el final del error
        lineaError += 1
        if(codigo[lineaError] == '\n'):
            break
        print(codigo[lineaError], end= "")
    print("\n")
    while(True):#imprime la posicion del error 
        if(pos == posicion-1):
            print("^")
            break
        else:
            print(" ", end="")
        pos +=1




