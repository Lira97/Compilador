#Enrique Lira Martinez A01023351
from parser import *

class Scope:
    def __init__(self, nivel, padre):
        self.nivel = nivel
        self.simbolos = {}
        self.childScopes = []
        self.padre = padre

    def ImprimirTabla(self):
        print("NIVEL ", self.nivel)#imprimimos el nivel del scope 
        print(self.simbolos)#junto con los simbolos  de cada rama
        if(self.childScopes != []):
            for i in range(len(self.childScopes)):
                self.childScopes[i].ImprimirTabla()

def AnalizadorSemantico(arbol, scopes, scopeIndex):
    if type(arbol.childNodes) == list:#si detectamos una lista
        for i in range(len(arbol.childNodes)):
            if type(arbol.childNodes[i]) == list:#si detectamos otra una lista
                for j in range(len(arbol.childNodes[i])):
                    AnalizadorSemantico(arbol.childNodes[i][j],scopes, scopeIndex)
            else:
                if(arbol.childNodes[i].type == "expression"):#si se detecta una expresion  
                    if not types(arbol.childNodes[i], scopes[scopeIndex]):#si no es un scope esperado
                        print("error")
                        return 0
                elif(arbol.childNodes[i].type == "fun-declaration"):#si es la fun declaration
                    scopeIndex +=1
                AnalizadorSemantico(arbol.childNodes[i],scopes, scopeIndex)
    return 0

def checkTree(arbol, Current):
    '''Checamos si es una definicion de la variable o function definition'''
    if type(arbol.childNodes) == list:#si detectamos una lista
        for i in range(len(arbol.childNodes)):
            if(type(arbol.childNodes[i]) == list):#si detectamos otra una lista
                for j in range(len(arbol.childNodes[i])):
                    checkTree(arbol.childNodes[i][j],Current)
            else:
                if(arbol.childNodes[i].type == "localDeclarations"): #local-declarations -> type-specifier ID ; | type-specifier ID [NUM]
 
                    Current.simbolos = VarDeclaration(arbol.childNodes[i], Current.simbolos)

                elif(arbol.childNodes[i].type == "fun-declaration"):#type-specifier ID (params) { local-declarations statement-list } 
                    Current.simbolos = FunctionProps(arbol.childNodes[i], Current.simbolos)
                    newScope = Scope(Current.nivel + 1, Current)
                    Current.childScopes.append(newScope)
                    newScope.simbolos = FunctionProps(arbol.childNodes[i], newScope.simbolos)
                    checkTree(arbol.childNodes[i], newScope)

                checkTree(arbol.childNodes[i],Current)
    return Current

def VarDeclaration(nodo, tabla):
    for i in range(len(nodo.childNodes)):#pasamos por todo el arbol para poder analizar la regla que hemos creado
        tabla[(nodo.childNodes[i].childNodes[1].value)] = nodo.childNodes[i].childNodes[0].type
    return tabla

def FunctionProps(nodo, tabla):#pasamos por todo el arbol para poder analizar la regla que hemos creado
    params = getParams(nodo.childNodes[2][1].childNodes)
    tabla[nodo.childNodes[1].value] = [nodo.childNodes[0].type, params]
    return tabla

def getParams(params):#pasamos por todo el arbol para poder analizar la regla que hemos creado
    paramsArray = []
    for i in range(len(params)):#detectamos todos los tipos que existen
        if(params[i].type == "param"):
            paramsArray.append(params[i].childNodes[0].type)
        elif(params[i].type =="void"):
            paramsArray.append("void")
    return paramsArray

def tabla( AST, imprime = True):
    initialScope = Scope(0, None)
    return checkTree(AST, initialScope)


def types(nodo, scope):#pasamos por todo el arbol para poder analizar la regla que hemos creado
    if nodo.childNodes[1].childNodes[0].type == 'additive-expression':
        if nodo.childNodes[1].childNodes[0].childNodes[0].childNodes[0].childNodes[0].type  == 'call':
            if nodo.childNodes[1].childNodes[0].childNodes[0].childNodes[0].childNodes[0].childNodes[0].value != 'input' and nodo.childNodes[1].childNodes[0].childNodes[0].childNodes[0].childNodes[0].childNodes[0].value!= 'output':
                try:
                    if scope.simbolos[nodo.childNodes[1].childNodes[0].childNodes[0].childNodes[0].childNodes[0].childNodes[0].value]:
                        return True
                except Exception as e:
                    return True
    return True


def GetArray(scope, array):#detectamos el arreglo para la regla creada
    array.append(scope)#metemos el scope en el arreglo
    if len(scope.childScopes) > 0:
        for i in range(len(scope.childScopes)):
            GetArray(scope.childScopes[i], array)#hasta que ya no detecta otro arreglo 
    return array

def semantica(AST, imprime = True):
    checkTree = tabla(AST)
    scopes = []
    if imprime:
        checkTree.ImprimirTabla()
    scopes = GetArray(checkTree, [])
    AnalizadorSemantico(AST, scopes, 0)
    return 0

if __name__ == '__main__':
    AST = parser(False)
    semantica(AST)

