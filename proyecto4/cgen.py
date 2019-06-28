#Enrique Lira Martinez A01023351

from globalTypes import *
from parser import *
from semantica import *
from cgen import *

Codigo = []
PalabrasReservadas = {'$zero': None, 
            '$v0': None, 
            '$v1': None, 
            '$a0':None, 
            '$a1': None, 
            '$a2': None, 
            '$a3': None, 
            '$t0': None, 
            '$t1': None, 
            '$t2':None,
            '$t3':None,
            '$t4':None,
            '$t5':None,
            '$t6':None,
            '$t7':None, 
            '$s0': None, 
            '$s1': None,
            '$s1': None,
            '$s3': None,
            '$s4': None,
            '$s5': None,
            '$s6': None,
            '$s7': None}
            
def codeGen(arbol, archivo, level = 0):
    global Codigo
    
    if arbol.type == 'program':#empezamos el programa 
        Codigo.append('.text')
        Codigo.append('.align 2')
        Codigo.append('.globl main')
        codeGen(arbol.childNodes[0], archivo, level +1)

    elif arbol.type == "fun-declaration":
        Codigo.append(arbol.childNodes[1].value + ":")
        Codigo.append('     move $fp $sp')
        Codigo.append('     sw $ra 0($sp)')
        Codigo.append('     addiu $sp $sp -4')
        codeGen(arbol.childNodes[2][1], archivo, level +1)
        Codigo.append('     lw $ra 4($sp)')
        Codigo.append('     addiu $sp $sp z')
        Codigo.append('     lw $fp 0($sp)')
        Codigo.append('     jr $ra')


    elif arbol.type == "call":
        if arbol.childNodes[0].value == 'input':
            input()
        elif arbol.childNodes[0].value == 'output':
            output()
        else:
            Codigo.append('     sw $fp 0($sp)')
            Codigo.append('     addiu $sp $sp -4')
            n = len(arbol.childNodes[1].childNodes)-1
            for i in range(n):
                codeGen(arbol.childNodes[1].childNodes[n-i], archivo, level+1)
                Codigo.append('     sw $fp 0($sp)')
                Codigo.append('     addiu $sp $sp -4')
            Codigo.append("     jal " + arbol.childNodes[0].value)

    elif arbol.type == 'additive-expression' and len(arbol.childNodes) == 2:
        if arbol.childNodes[1].childNodes[0].type == '-':
            codeGen(arbol.childNodes[0], archivo, level+1)
            Codigo.append('     sw $a0 0($sp)')
            Codigo.append('     addiu $sp $sp -4')
            codeGen(arbol.childNodes[1].childNodes[1], archivo, level +1)
            Codigo.append('     lw $t1 4($sp)')
            Codigo.append('     sub $a0 $t1 $a0')
            Codigo.append('     addiu $sp $sp 4')
        elif arbol.childNodes[1].childNodes[0].type == '+':
            codeGen(arbol.childNodes[0], archivo, level+1)
            Codigo.append('     sw $a0 0($sp)')
            Codigo.append('     addiu $sp $sp -4')
            codeGen(arbol.childNodes[1].childNodes[1], archivo, level +1)
            Codigo.append('     lw $t1 4($sp)')
            Codigo.append('     add $a0 $t1 $a0')
            Codigo.append('     addiu $sp $sp 4')

    elif arbol.type == 'term' and len(arbol.childNodes) > 1:
        if arbol.childNodes[1].type =='term-p':
            if arbol.childNodes[1].childNodes[0].type == '*':
                codeGen(arbol.childNodes[0], archivo, level +1)
                Codigo.append('     sw $a0 0($sp)')
                Codigo.append('     addiu $sp $sp -4')
                codeGen(arbol.childNodes[1].childNodes[1], archivo, level +1)
                Codigo.append('     lw $t1 4($sp)')
                Codigo.append('     mult $a0 $t1 $a0')
                Codigo.append('     addiu $sp $sp 4')
            elif arbol.childNodes[1].childNodes[0].type == '/':
                codeGen(arbol.childNodes[0], archivo)
                Codigo.append('      sw $a0 0($sp)')
                Codigo.append('      addiu $sp $sp -4')
                codeGen(arbol.childNodes[1].childNodes[1], archivo, level +1)
                Codigo.append('      lw $t1 4($sp)')
                Codigo.append('      div $a0 $t1 $a0')
                Codigo.append('      addiu $sp $sp 4')

    elif arbol.type == 'expression':
        if arbol.childNodes[1].type == '=':
            codeGen(arbol.childNodes[2], archivo, level)
            Codigo.append('     la ' + reservarVariableTemporal() + '($v1)')

    elif arbol.type == 'iteration-stmt':
            Codigo.append('     while:')
            codeGen(arbol.childNodes[1], archivo, level +1)
            Codigo.append('     exit')
            codeGen(arbol.childNodes[2], archivo, level +1)
            Codigo.append('     j while')
            Codigo.append('     exit:')

    elif(arbol.type == 'selection-stmt'):
        if arbol.childNodes[1].childNodes[1].childNodes[1].type  == '==':
            Codigo.append('     beq $t0, $t1, true_branch')
        elif arbol.childNodes[1].childNodes[1].childNodes[1].type  == '<':
            Codigo.append('     slt $t3,$t1,$t0') #s0 > s1
            Codigo.append('     beq $t3, 1 true_branch')
        elif arbol.childNodes[1].childNodes[1].childNodes[1].type == '>':
            Codigo.append('     slt $t3,$t1,$t0') #s0 < s1
            Codigo.append('     beq $t3, 0 true_branch')
        elif arbol.childNodes[1].childNodes[1].childNodes[1].type  == '=<':
            Codigo.append('     beq $t0, $t1, true_branch')
            Codigo.append('     slt $t3,$t1,$t0') #s0 > s1
            Codigo.append('     beq $t3, 1 true_branch')
        elif arbol.childNodes[1].childNodes[1].childNodes[1].type == '=>':
            Codigo.append('     beq $t0, $t1, true_branch')
            Codigo.append('     slt $t3,$t1,$t0') #s0 < s1
            Codigo.append('     beq $t3, 0 true_branch')
        elif arbol.childNodes[1].childNodes[1].childNodes[1].type == '!=':
            Codigo.append('     beq $t0, $t1, false_branch')

        if arbol.childNodes[3].type == 'else':
            Codigo.append('false_branch:')
            codeGen(arbol.childNodes[4], archivo, level+1)
            Codigo.append('     b end_if')
        Codigo.append("true_branch:")
        codeGen(arbol.childNodes[2], archivo, level +1)
        Codigo.append("end_if:")


    elif(arbol.type == 'return-stmt'):
        codeGen(arbol.childNodes[1][0].childNodes[1], archivo, level +1)
        Codigo.append('     la $v0, $t3')
        Codigo.append('     lw $fp 0($sp)')
        Codigo.append('     jr $ra')

    elif arbol.type == 'var-declaration':
        Codigo.append('     ori ' + reservarVariable(arbol.childNodes[1].value) + ', 0')


    elif type(arbol.childNodes) == list:
        for i in range(len(arbol.childNodes)):
            if(type(arbol.childNodes[i]) == list):
                for j in range(len(arbol.childNodes[i])):
                    codeGen(arbol.childNodes[i][j],archivo, level+1)
            else:
                codeGen(arbol.childNodes[i],archivo, level +1)
    if arbol.type == 'endfile':
        Codigo.append('     li $v0, 10')
        Codigo.append('     syscall')
        GenerarArchivo(archivo)

def input():
    Codigo.append('     li $v0, 5')
    Codigo.append('     syscall')
    Codigo.append('     move $t0, $v0')
    return

def output():
    Codigo.append('     li $v0, 1')
    Codigo.append('     move $a0, $t0')
    Codigo.append('     syscall')
    return

def reservarVariableTemporal():
    for i in range(7):
        index = '$t' + str(7 - i)
        if(PalabrasReservadas[index] == None):
            PalabrasReservadas[index] = "in use"
            return index

def reservarVariable(var):
    for i in range(7):
        index = '$s' + str(i)
        if(PalabrasReservadas[index] == None):
            PalabrasReservadas[index] = "in use"
            return index

def GenerarArchivo(archivo):
    open(archivo, 'w').close()
    f= open(archivo,"a")
    for i in range(len(Codigo)):
        temp = Codigo[i] + "\n"
        f.write(temp)
    f.close()

if __name__ == '__main__':
    f = open('sample.c-', 'r')
    programa = f.read()
    progLong = len(programa)
    programa = programa + '$'
    posicion  = 0
    globales(programa, posicion, progLong)
    AST =  parser(True)
    semantica(AST, True)
    codeGen(AST, 'file.s')
    f.close()
    
