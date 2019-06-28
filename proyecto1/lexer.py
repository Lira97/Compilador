from globalTypes import *

def globales(prog, pos, long):
	global codigo#string del codigo entero
	global posicion  #posicion del caracter que se esta analizando 
	global Longitud #longitud del codigo analizando
	codigo = prog
	posicion = pos
	Longitud = long

def getToken(imprime = True):
	global posicion

	while(codigo[posicion] == ' ' or codigo[posicion] == '\n' or codigo[posicion]== '\t'):
		posicion += 1
	if(codigo[posicion] == '$'): 
		return (printToken(TokenType.ENDFILE, '$',  1))
	elif(codigo[posicion] == '+'): 
		return (printToken(TokenType.PLUS, '+',  1))
	elif(codigo[posicion] == '-'):
		return (printToken(TokenType.MINUS, '-',  1))
	elif(codigo[posicion] == ';'):
		return (printToken(TokenType.SEMICOLON, ';',  1))
	elif(codigo[posicion] == ','):
		return (printToken(TokenType.COMMA, ',',  1))
	elif(codigo[posicion] == '('):
		return (printToken(TokenType.OPEN_PARENTHESIS, '(',  1))
	elif(codigo[posicion] == ')'):
		return (printToken(TokenType.CLOSE_PARENTHESIS, ')', 1 ))
	elif(codigo[posicion] == '['):
		return (printToken(TokenType.OPEN_BRACKETS, '[',  1))
	elif(codigo[posicion] == ']'):
		return (printToken(TokenType.CLOSE_BRACKETS, ']',  1))
	elif(codigo[posicion] == '{'):
		return (printToken(TokenType.OPEN_KEYS, '{',  1))
	elif(codigo[posicion] == '}'):
		return (printToken(TokenType.CLOSE_KEYS, '}',  1))
	elif(codigo[posicion] == '<'):
		if(codigo[posicion+1] == '='):
			return (printToken(TokenType.LESS_THAN_EQUAL_TO, '<=',  2))
		return (printToken(TokenType.LESS_THAN, '<',  1))
	elif(codigo[posicion] == '>'):
		if(codigo[posicion+1] == '='):
			return (printToken(TokenType.GREATER_THAN_EQUAL_TO, '>=',  2))
		return (printToken(TokenType.GREATER_THAN, '>',  1))
	elif(codigo[posicion] == '*'):
		return (printToken(TokenType.ASTERISK, '*',  1))
	elif(codigo[posicion] == '/'):
		return (printToken(TokenType.SLASH, '/',  1))
	elif(codigo[posicion] == '='):
		if(codigo[posicion+1] == '='):
			return (printToken(TokenType.EQUAL, '==',  2))
		return (printToken(TokenType.ASSIGNMENT, '=',  1))
	elif(codigo[posicion] == '!'):
		if(codigo[posicion+1] == '='):
			return (printToken(TokenType.DIFFERENT, '!=',  2))
		else:
			return(printToken(TokenType.ERROR, 'error',  2, "Error en la formacion de expresion", posicion))
	elif(codigo[posicion].isalpha()):#checa si es una palabra 
		size = 1 # variable para almacenar el tamano del string 
		token = codigo[posicion]
		while(True):
			if(codigo[posicion+size].isalnum()):#mientras no se algo diferente a un numero
				token += codigo[posicion + size]#agregamos al token cada letra con su tamano 
				size += 1
			else:
				break#si la palabra es una palabra reservada de c tiny 
		if(token == 'else'):
			return (printToken(TokenType.ELSE, token, size))
		elif(token == 'if'):
			return (printToken(TokenType.IF, token, size))
		elif(token == 'int'):
			return (printToken(TokenType.INT, token, size))
		elif(token == 'return'):
			return (printToken(TokenType.RETURN, token, size))
		elif(token == 'void'):
			return (printToken(TokenType.VOID, token, size))
		elif(token == 'while'):
			return (printToken(TokenType.WHILE, token,  size))
		else:
			return(printToken(TokenType.ID, token, size))
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
						return(printToken(TokenType.ERROR, 'error',  size, "Error en la formacion de un entero", PosError))
					else:
						size += 1
			else:
				break
		return(printToken(TokenType.NUM, token,  size))
	else:
		return(printToken(TokenType.ERROR, 'error',  1))
		
		
def printToken(TokenType, valor, longitud, MessajeError = "", PosError = 0):#funcion para imprimir los token encontrados asi sea un error 
	global posicion
	posicion += longitud 
	if(valor == 'error'):#si el token es un error entonces este se ira a la funcion de imprimir error
		printError(PosError, MessajeError)
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
