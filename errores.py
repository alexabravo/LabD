import re

def parentesisCheck(expresionRegular):
    pila = []
    for char in expresionRegular:
        if char == '(':
            pila.append(char)
        elif char == ')':
            if len(pila) == 0:
                return False
            pila.pop()

    return len(pila) == 0

def deteccion(expresionRegular):

    parent = parentesisCheck(expresionRegular)

    if not parent:
        print("Error: el archivo no tiene la misma cantidad de paréntesis")
        return False

    abc123 = re.match(r"[a-zA-Z0-9ε]*", expresionRegular)

    if not abc123:
        print("Error: El archivo no tiene letras y/o números.")
        return False

    inicio = re.match(r"^(?![*+]).*", expresionRegular)

    if not inicio:
        print("Error: El archivo no puede empezar con un * o un +.")
        return False

    inicio = re.match(r".*(?<!\|)$", expresionRegular)

    if not inicio:
        print("Error: El archivo no puede terminar con |.")
        return False

    if re.search("\-", expresionRegular):
        print("archivo Valido válida.")
        return True

    return True

def deteccion2(expresionRegular):

    if expresionRegular.count('[') != expresionRegular.count(']'):
        print("Error: el archivo no tiene la misma cantidad de corchetes.")
        return "Corchetes", expresionRegular

    if expresionRegular.count('(') != expresionRegular.count(')'):
        print("Error: el archivo no tiene la misma cantidad de paréntesis.")
        return "Parent", expresionRegular
    

    abc123 = re.match(r"[a-zA-Z0-9ε]*", expresionRegular)
    if not abc123: 
        print("Error: El archivo no tiene letras y/o números.")
        return False, expresionRegular

    inicio = re.match(r"^(?![*+]).*", expresionRegular)

    if not inicio:
        print("Error: El archivo no puede empezar con un * o un +.")
        return "BB", expresionRegular
    

    inicio = re.match(r".*(?<!\|)$", expresionRegular)

    if not inicio:
        print("Error: El archivo no puede terminar con |.")
        return "OF", expresionRegular
    
    return True, expresionRegular