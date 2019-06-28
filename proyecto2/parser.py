from globalTypes import *
from lexer import *

ListOfTokens = []
currentToken = -1

class Node:
    def __init__(self, type, childNodes = None, value =None):
        self.type = type
        self.value = value
        if childNodes :
            self.childNodes = childNodes
        else:
            self.childNodes = []
    def printTree(self, level = 0):
        print((level*1)*'| ', self.type)
        if(self.childNodes != []):
            if(type(self.childNodes) == Node):
                self.childNodes.printTree(level+1)
            else:
                for i in range(len(self.childNodes)):
                    if(type(self.childNodes[i]) == list):
                        for j in range(len(self.childNodes[i])):
                            self.childNodes[i][j].printTree(level+1)
                    else:
                        self.childNodes[i].printTree(level+1)
                        
def parser(imprime = True):
    AST = Program()
    if(imprime == True):
        AST.printTree(0)
    return AST
    
def nextToken():#obtenemos el siguite token del array
    global currentToken
    currentToken += 1
    return ListOfTokens[currentToken]

def getCurrenToken():# regresamos el token actual 
    return ListOfTokens[currentToken]
    
def match(ttype):#verificamos el token 
    global token
    if nextToken() == ttype:
        return True
    return False
def matchCurrent(ttype):
    global token
    if getCurrenToken() == ttype:
        return True
    return False

def Program():
    """program -> declaration-list """ 
    return Node("program", [DeclarationList()])#entramos a la gramatica 

def DeclarationList():
    """
    declaration-list ->declaration | declaration declaration-list 
    """   
    childNodes = []
    while(True):
        if(ListOfTokens[currentToken + 1] == TokenType.ENDFILE):#detectamos el fin del programa 
            break
        else:
            declaration =  Declaration()#entramos en la funcion declarion para detectar los terminales
            if(declaration):
                childNodes.append(declaration)
    return(Node("declaration-list", childNodes))


def Declaration():
    """ 
    declaration -> var-declaration | fun-declaration 
    """
    typespecifier = TypeSpecifier()#esta gramatica empieza con tipo de especificador 
    childNodes = [] 
    if(typespecifier):
        childNodes.append(typespecifier)
        if match(TokenType.ID):
            childNodes.append(Node("ID"))#agramos el ID 
            if match(TokenType.OPEN_PARENTHESIS):#decide si va a ser un Var o fun declaration 
                fun = funDeclaration()
                if(fun):
                    childNodes.append(fun)
                    return (Node("funDeclaration", childNodes))
            else:
                var = varDeclaration()
                if(var):
                    childNodes.append(var)
                    return(Node("varDeclaration", childNodes))

    return None


def varDeclaration():
    """
    var-declaration -> type-specifier ID ; | type-specifier ID [NUM] ; 
    """
    childNodes = []
    if match(TokenType.SEMICOLON):
        childNodes.append(Node(";"))#agregamose un ; si se detecta type-specifier ID ;
        return childNodes
    elif match(TokenType.OPEN_BRACKETS):#agregamose un ; si se detecta type-specifier ID [NUM] ; 
        childNodes.append(Node("["))
        if match(TokenType.NUM):
            childNodes.append(Node("NUM"))
            if match(TokenType.CLOSE_BRACKETS):
                childNodes.append(Node("]"))
                if match(TokenType.SEMICOLON):
                    childNodes.append(Node(";"))
                    return childNodes
    return None


def TypeSpecifier():
    """
        type_specifier : int | void
    """
    token = nextToken()
    if(token == TokenType.INT):#verificamos si es un int
        return(Node("int"))
    elif(token == TokenType.VOID):#verificamos si es un void
        return(Node("void"))
    return None


def funDeclaration():
    """
    fun-declaration -> type-specifier ID (params) compound-stmt 
    """
    childNodes = [Node("(")]#al haber identificado el type-specifier ID revisamos los parentesis 
    params = paramList()# vemos los paremtros que contiene 
    if(params):
        childNodes.append(params)
        childNodes.append(Node(")"))
        compoundStmt = CompoundStmt()# revisamos el compound-stmt 
        if(compoundStmt):
            childNodes.append(compoundStmt)
            return childNodes
    return None




def paramList():
    """
    param-list -> param param-list' 
    """
    childNodes = [Param()]
    if(childNodes[0] == None):#puede ser un vacio 
        return None
    while(True):
        if matchCurrent(TokenType.COMMA):
            childNodes.append(Node(","))
            param = Param()#mientras detecte los parametros 
            if(param):
                childNodes.append(param)
        if matchCurrent(TokenType.CLOSE_PARENTHESIS):
            return(Node("params", childNodes))



def Param():
    """
    param -> type-specifier ID | type-specifier ID [] 
    """
    childNodes = []
    typeSpecifier = TypeSpecifier()#esta gramatica empieza con tipo de especificador 
    if(typeSpecifier):
        if(typeSpecifier.type == "void"):#si es un coid 
            if match(TokenType.CLOSE_PARENTHESIS):
                return(Node("void"))
        childNodes.append(typeSpecifier)
        if match(TokenType.ID):#si es un ID 
            childNodes.append(Node("ID"))
            if match(TokenType.OPEN_BRACKETS):
                childNodes.append(Node("["))
                if match(TokenType.CLOSE_BRACKETS):
                    childNodes.append(Node("]"))
                    return(Node("param", childNodes))
            elif matchCurrent(TokenType.COMMA):
                return(Node("param", childNodes))
            elif matchCurrent( TokenType.CLOSE_PARENTHESIS):
                return(Node("param", childNodes))
    return None



def CompoundStmt():
    """
      compount-stmt -> { local-declarations statement-list } 
    """
    childNodes = []
    if match(TokenType.OPEN_KEYS):
        childNodes.append(Node("{"))#detectamos una llave 
        local = localDeclarations()
        if(local):
            childNodes.append(local)
            statement = statementList()#detectamos el local declaration
            if(statement):
                childNodes.append(statement)
                if match(TokenType.CLOSE_KEYS):
                    childNodes.append(Node("}"))#se cierra la llave cerrada
                    return(Node("compound-stmt", childNodes))
    return None

def localDeclarations():
    """
    local-declarations -> empty | var-declaration local-declarations 
    """
    global currentToken
    currentPos = currentToken
    childNodes = []
    while(True):
        tmp = localVarDeclaration()#detectamos el var declaration
        if(tmp):
            childNodes.append(tmp)
            currentPos = currentToken
        else:
            currentToken = currentPos
            break
    if(len(childNodes) > 0):
        return(Node("localDeclarations", childNodes))
    else:
        return(Node("empty"))

def localVarDeclaration():
    """
    var-declaration -> type-specifier ID ; | type-specifier ID [NUM] ; 
    """
    childNodes =[]
    type = TypeSpecifier()#se detecta el tipo 
    if(type):
        childNodes.append(type)
        if match(TokenType.ID):
            childNodes.append(Node("ID"))#detectamos el id
            tmp = varDeclaration()
            if(tmp):
                childNodes.append(tmp)
                return(Node("varDeclaration", childNodes))

def statementList():
    """
         statement-list -> empty | statement statement-list
    """
    global currentToken
    stmt = []
    tmp = statement()
    while(tmp):
        stmt.append(tmp)
        tmp = statement()#revisamos el stament
    if(len(stmt) > 0):
        return(Node("statement-list", stmt))
    else:
        return(Node("empty"))#detectamos el vacio 



def statement():
    """statement -> expression-stmnt | compound-stmt | selection-stmt | iteration-stmt |return stmt 
    """
    global currentToken
    currentPos = currentToken
    exp = expressionStmt()#expression-stmnt
    if(exp):
        return (Node("statement", exp))
    currentToken = currentPos
    exp = CompoundStmt()# compound-stmt
    if(exp):
        return(Node("statement", exp))
    currentToken = currentPos
    exp = selectionStmt()#selection-stmt
    if(exp):
        return(Node("statement", exp))
    currentToken = currentPos
    exp = iterationStmt()#iteration-stmt
    if(exp):
        return(Node("statement", exp))
    currentToken = currentPos
    exp = returnStmt()#return stmt 
    if(exp):#Vacio 
        return(Node("statement", exp))
    currentToken = currentPos

    return None
    
def expressionStmt():
    """
    expression-stmnt -> expression ; | ; 
    """
    global currentToken
    childNodes = []
    if match(TokenType.SEMICOLON):
        return(Node(";"))
    else:
        currentToken -= 1
        exp = Expression()
        if(exp):
            childNodes.append([exp, Node(";")])
            return(Node("expression-stmt", childNodes))
    return None

def selectionStmt():
    """
     selection-stmt -> if ( expression ) statement | if ( expression ) statement else statement 
    """
    global currentToken
    childNodes = []
    if match(TokenType.IF):
        childNodes.append(Node("if"))#detectamos el if 
        if match(TokenType.OPEN_PARENTHESIS):
            childNodes.append(Node("("))#detectamos (expresion )
            exp = Expression()
            if(exp):
                childNodes.append(exp)
                if match(TokenType.CLOSE_PARENTHESIS):
                    childNodes.append(Node(")"))
                    stmt = statement()#si contiene un stament 
                    if(stmt):
                        childNodes.append(stmt)
                        if match(TokenType.ELSE):
                            childNodes.append(Node("else"))#detectamos el else
                            stmt = statement()
                            if(stmt):
                                childNodes.append(stmt)
                                return(Node("selection-stmt", childNodes))
                        else:

                            currentToken -= 1
                            return(Node("selection-stmt", childNodes))
    return None


def iterationStmt():
    """
    iteration-stmt -> while ( expression ) statement 
    """
    childNodes = []
    if match(TokenType.WHILE):
        childNodes.append(Node("while"))#detectamos el while 
        if match(TokenType.OPEN_PARENTHESIS):
            childNodes.append(Node("("))#abrimos los parentesis 
            exp = Expression()#detetamos la expresion 
            if(exp):
                childNodes.append(exp)
                if match(TokenType.CLOSE_PARENTHESIS):
                    childNodes.append(Node(")"))#cerramos los parentesis 
                    stmt = statement()#detectamos los statement
                    if(stmt):
                        childNodes.append(stmt)
                        return(Node("iteration-stmt", childNodes))
    return None

def returnStmt():
    """
     return-stmt -> return ; | return expression ; 
    """
    global currentToken
    childNodes = []
    if match(TokenType.RETURN):
        childNodes.append(Node("return"))#detectamos el retunr 
        if match(TokenType.SEMICOLON):
            childNodes.append(Node(";"))#con su semicolumn
            return(Node("return-stmt", childNodes))
        else:

            currentToken -= 1
            exp = Expression()#si contiene una expresion 

            if(exp):
                if match(TokenType.SEMICOLON):
                    childNodes.append([exp, Node(";")])#con su semicolumn
                    return(Node("return-stmt", childNodes))
    return None

def Expression():
    """
     expression -> var = expression | simple-expression 
    """
    childNodes = []
    global currentToken
    currentPos = currentToken
    var = Var()#detectamos las varibles 
    if(var):
        childNodes.append(var)
        if match(TokenType.ASSIGNMENT):
            childNodes.append(Node("="))#si se tiene una variableb detectamos la asignacion 
            exp = Expression()#y la expresion 
            if(exp):
                childNodes.append(exp)
                return(Node("expression", childNodes))

    currentToken = currentPos
    exp = simpleExpression()#si solo detecta la expresion simple
    if(exp):
        childNodes.append(exp)
        return(Node("expression", childNodes))
    return None

def Var():
    """
    var -> ID | ID [expression] 
    """
    global currentToken
    childNodes = []
    if match(TokenType.ID):
        childNodes.append(Node("ID"))#se detecta el ID 
        if match(TokenType.OPEN_BRACKETS):
            childNodes.append(Node("["))#este pude contener una expresion 
            exp = Expression()
            if(exp):
                childNodes.append(exp)
                if match(TokenType.CLOSE_BRACKETS):
                    childNodes.append(Node("]"))
                    return(Node("var", childNodes))
        else:
            currentToken -= 1
            return(Node("var", childNodes))
    return None

def simpleExpression():
    """
    simple-expression -> additive expression relop additive-expression | additive expression 
    """
    childNodes = []
    global currentToken
    currentPos = currentToken
    add = additiveExp()#detectamos el additive expression
    if(add):
        childNodes.append(add)
        currentPos = currentToken
        relop = Relop()# detectamos el Relop
        if(relop):
            childNodes.append(relop)
            add = additiveExp()#detectamos el additive expression
            if(add):
                childNodes.append(add)
                return(Node("simple-expression", childNodes))
        else:# si solo contiene el additive expression lo detectamos
            currentToken = currentPos
            return(Node("simple-expression", childNodes))

    return None


def Relop():
    """
    relop -> <= | < | > | >= | == | != 
    """
    global currentToken
    if match(TokenType.LESS_THAN_EQUAL_TO):#detectamos el <=
        return(Node("<="))
    elif match(TokenType.LESS_THAN):#detectamos el <
        return(Node("<"))
    elif(getCurrenToken() == TokenType.GREATER_THAN):#detectamos el >
        return(Node(">"))
    elif(getCurrenToken() == TokenType.GREATER_THAN_EQUAL_TO):#detectamos el >=
        return(Node(">="))
    elif(getCurrenToken() == TokenType.EQUAL):#detectamos el ==
        return(Node("=="))
    elif(getCurrenToken() == TokenType.DIFFERENT):#detectamos el !=
        return(Node("!="))
    currentToken -= 1
    return None

def additiveExp():
    """
    additive-expression -> term additive-expression’ 
    """
    global currentToken
    currentPos = currentToken
    childNodes = []
    term = Term()#detectamos el term
    if(term):
        currentPos = currentToken
        childNodes.append(term)
        add = additiveExpP()#additive-expression’
        if(add):
            childNodes.append(add)
            return(Node("additive-expression", childNodes))
        else:
            currentToken = currentPos
            return(Node("additive-expression", childNodes))
    return None


def additiveExpP():
    """
    additive-expression’ -> addop term additive-expression’ | empty 
    """
    childNodes = []
    addop = addOp()# detectamos el addop
    if(addop):
        childNodes.append(addop)
        term = Term()#detectamos el term
        if(term):
            childNodes.append(term)
            add = additiveExpP()#detectamos el additive-expression
            if(add):
                childNodes.append(add)
                return(Node("additive-expression",childNodes))
    else:
        return None


def addOp():
    """
    addop -> + | - 
    """
    if match(TokenType.PLUS):#detectamos el +
        return(Node("+"))
    elif(getCurrenToken() == TokenType.MINUS):#detectamos el -
        return(Node("-"))
    return None

def Term():
    """term -> factor | term’ """
    global currentToken
    currentPos = currentToken
    childNodes = []
    factor = Factor()#detectamos el factor 
    if(factor):
        childNodes.append(factor)
        return(Node("term", childNodes))
    currentToken = currentPos
    term = TermP()# o detectamos  el term 
    if(term):
        childNodes.append(term)
        return(Node("term", childNodes))
    return None

def TermP():
    """term’ -> empty | mulop factor term’ """
    childNodes = []
    mulop = Mulop()#detectamos el Mulop 
    if(mulop):
        childNodes.append(mulop)#detectamos el Mulop 
        factor = Factor()
        if(factor):
            childNodes.append(factor)#detectamos el factor 
            term =  TermP()
            if(term):
                childNodes.append(term)
                return(Node("term-p", childNodes))
    return None#detectamos el vacio 


def Mulop():
    """mulop *| / """
    if match(TokenType.ASTERISK):
        return(Node("*"))#detectamos el *
    elif(ListOfTokens[currentToken].SLASH):
        return(Node("/"))#detectamos el /
    return None

def Factor():
    """
    factor -> (expression ) | var | call | NUM 
    """
    global currentToken
    childNodes = []
    currentPos = currentToken
    if match(TokenType.OPEN_PARENTHESIS):#detecta el (expresion )
        childNodes.append(Node("("))
        exp = Expression()
        if(exp):
            childNodes.append(exp)
            if match(TokenType.CLOSE_PARENTHESIS):
                childNodes.append(Node(")"))
                return(Node("factor", childNodes))
    elif(getCurrenToken() == TokenType.NUM):#detecta el NUM
        childNodes.append(Node("num"))
        return(Node("factor", childNodes))

    currentToken = currentPos
    call = Call()#detecta el call
    if(call):
        childNodes.append(call)
        return(Node("factor", childNodes))

    currentToken = currentPos
    var = Var()#detecta el var 
    if(var):
        childNodes.append(var)
        return(Node("factor", childNodes))

    return None

def Call():
    """
    call -> ID (args) 
    """
    childNodes = []
    if match(TokenType.ID):
        childNodes.append(Node("ID"))#detecta el ID
        if match(TokenType.OPEN_PARENTHESIS):
            childNodes.append(Node("("))#detecta el (args) 
            args = Args()
            childNodes.append(args)
            if(args):
                childNodes.append(Node(")"))
                return(Node("call", childNodes))
    return None

def Args():
    """
    args -> arg-list | empty 
    """
    global currentToken
    if match(TokenType.CLOSE_PARENTHESIS):#detecta el vacio 
        return(Node("empty"))
    currentToken -= 1
    arglist = ArgList()#detecta el (args) 
    if(arglist):
        return(Node("args", arglist))

def ArgList():
    """arg-list -> expression arg-list' """
    childNodes = [Expression()]
    while(True):
        if match(TokenType.COMMA):
            childNodes.append(Node(","))
            childNodes.append(Expression())
        elif(getCurrenToken() == TokenType.CLOSE_PARENTHESIS):
            return childNodes