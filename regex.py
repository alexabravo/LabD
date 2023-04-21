class expresionRegular:
    def __init__(self, expresion_regular):
        self.expresion_regular =  expresion_regular

def alfabeto(expresionRegular):
    alfabeto = []
    for i in expresionRegular:
        if i != '(' and i != ')' and i != '*' and i != '+' and i != '?' and i != '|' and i != 'ε' and i != '.':
            alfabeto.append(i)
            alfabeto = list(dict.fromkeys(alfabeto))
    
    return alfabeto


get_precedence = lambda c: {'|':1,'.':2,'*':3,'+':3,'?':3,'(':-1,')':-1}.get(c, 6)

def convertir(expresionRegular):
    res = ''
    Operador = set(['|', '?', '+', '*', '^'])
    OperadoresB = set(['^', '|'])

    for i in range(len(expresionRegular)):
        c1 = expresionRegular[i]

        if i + 1 < len(expresionRegular):
            c2 = expresionRegular[i + 1]

            res += c1

            if c1 != '(' and c2 != ')' and c2 not in Operador and c1 not in OperadoresB:
                res += '.'

    res += expresionRegular[-1]

    if "+" in res:
        res = res.replace("+", "")
        res = res + "." + res + "*"
        print("Res: ", res)
    return res


def regex_to_postfix(expresionRegular):
    pila = []
    postfix = ''
    expresionLista = convertir(expresionRegular)
    for c in expresionLista:
        if c == '(':
            pila.append(c)
        elif c == ')':
            while pila[-1] != '(':
                postfix += pila.pop()
            pila.pop()
        else:
            while len(pila) > 0:
                charTomado = pila[-1]

                charTomadoPrecedencia = get_precedence(charTomado)
                precedenciaActualChar = get_precedence(c)

                if charTomadoPrecedencia >= precedenciaActualChar:
                    postfix += pila.pop()
                else:
                    break

            pila.append(c)

    while len(pila) > 0:
        postfix += pila.pop()
    return postfix