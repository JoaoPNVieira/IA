#Exercicio 4.1
impar = lambda numero: numero%2 == 1



#Exercicio 4.2
positivo = lambda numero: numero>0

#Exercicio 4.3
comparar_modulo = lambda x, y: abs(x) < abs(y)

#Exercicio 4.4
import math
cart2pol = None

#Exercicio 4.5
ex5 = None #lambda f,g,h: lambda x,y,z: h(...)

#Exercicio 4.6
def quantificador_universal(lista, f):
    return[e for e in lista if not f(e)] == []

#Exercicio 4.9
def ordem(lista, f):
    
    if len(lista) == 1:
        return lista[0]
    
    m = ordem(lista[1:],f)

    return lista[0] + f(lista[0],m) else m


#Exercicio 4.10
def filtrar_ordem(lista, f):
    pass

#Exercicio 5.2
def ordenar_seleccao(lista, ordem):
    pass
