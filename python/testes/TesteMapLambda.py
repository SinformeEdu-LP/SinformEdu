import math

SOMA1 = lambda x: x + 1

def printImpar(lista):
    return list(map(SOMA1,lista))

def printImpar2(lista):
    return list(map(lambda x: x + 1,lista))
       
# Driver program
if __name__ == "__main__":
    
    l1 = [1,3,5,7,9,11,13,15]
    l2 = []
    l3 = []
    print("Teste com For")
    for i in l1:
        i += 1
        l2.append(i)
    print(l2)
    
    print("")
    print("Teste com map1")
    lista1 = [1, 4, 9, 16, 25]
    lista2 = list(map(math.sqrt, lista1))
    print(lista2)
        
    print("")
    print("Teste com map e lambda")    

    l3 = printImpar(l1)
    print(l3)    
    
    l3 = printImpar2(l1)
    print(l3) 
    