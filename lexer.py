class Lexer:

    def __init__(self, diccionarios, iniciales, finales, archivo, reservadas=[], operadores_reservados=[], tokens=[], tabla={}):
        self.diccionarios = diccionarios
        self.iniciales = iniciales
        self.finales = finales
        self.archivo = archivo
        self.reservadas = reservadas
        self.operadores_reservados = operadores_reservados
        self.tokens = tokens
        self.tabla = tabla
        
        self.diccionario_cadenas = {} 
        self.cadena_strings = [] 
        self.reservadas = ["IF", "FOR", "WHILE", "ELSE"]


        for palabra in self.reservadas:
            if palabra in self.tokens:
                self.tokens.remove(palabra)
        
        for i, token in enumerate(self.tokens):
            self.tokens[i] = token.replace('rule gettoken =\n', '').strip()

        print(self.tokens)

        new_m = "-"
        for key in self.tabla:
            if "~" in self.tabla[key]:
                value = self.tabla[key].replace("~", new_m)
                self.tabla[key] = value
        
        new_m = "+"
        for key in self.tabla:
            if "@" in self.tabla[key]:
                value = self.tabla[key].replace("@", new_m)
                self.tabla[key] = value
        
        new_m = " "
        for key in self.tabla:
            if "≡" in self.tabla[key]:
                value = self.tabla[key].replace("≡", new_m)
                self.tabla[key] = value
        
        new_m = "\t"
        for key in self.tabla:
            if "¥" in self.tabla[key]:
                value = self.tabla[key].replace("¥", new_m)
                self.tabla[key] = value

        new_m = "\n"
        for key in self.tabla:
            if "§" in self.tabla[key]:
                value = self.tabla[key].replace("§", new_m)
                self.tabla[key] = value

        print("Tabla: ", self.tabla)


        self.lista = []
        self.lista.extend(self.reservadas)
        self.lista.extend(self.operadores_reservados)
        self.lista.extend(self.tokens)

        res_copy = self.reservadas.copy()
        
        self.cad_s = [] 
        self.t = []
        self.cads = []


        with open(self.archivo, "r") as archivo:
            for linea in archivo:
                if linea[0] == '"' and linea[-1] == '"':
                    self.cad_s.append(linea.strip())
                    self.cads.append(linea.strip())
                else:
                    cadenas = linea.strip().split()
                    for cadena in cadenas:
                        if cadena[0] == '"' and cadena[-1] == '"':
                            self.cad_s.append(cadena.strip())
                            self.cads.append(linea.strip())
                        else:
                            self.cad_s.extend(cadena.split())
                            self.cads.append(linea.strip())
                    self.t.extend(cadenas)

                    self.cads.extend(linea.strip())

                    self.cad_s.extend(cadenas)

        resultados_txt = self.simular_cadenas(diccionarios, iniciales, finales, resultado=[])

        resultados_res = self.simular_res()
 
        self.archivopy = "scanner.py"

        print("Tokens: ", self.tokens)
        
        self.generar_py(self.archivopy, self.diccionarios, self.iniciales, self.finales, self.archivo, res_copy, self.operadores_reservados, self.tokens, self.tabla)

    def simular_cadenas(self, diccionarios, iniciales, finales, resultado=[]): 

        if not diccionarios:
            return resultado

        if len(self.cad_s) == 0:
            return resultado
        else:
            cadena_actual = self.cad_s.pop(0)

            self.cadena_copy = cadena_actual

            if cadena_actual[0] == '"' and cadena_actual[-1] == '"':

                cadena_actual = cadena_actual.replace('"', '')

            valores_cadena = []
            for i in range(len(diccionarios)):
                diccionario = diccionarios[i]
                estado_ini = iniciales[i]
                estados_acept = finales[i]
                estado_actual = estado_ini[0]
                
                if len(cadena_actual) == 1:
                    if cadena_actual in self.operadores_reservados:

                        if i == len(diccionarios) - 1:
                            valores_cadena.append(True)

                    else: 
        
                        if i == len(diccionarios) - 1:
                            valores_cadena.append(False)

                for j in range(len(cadena_actual) - 1):
                    caracter_actual = cadena_actual[j]
                    caracter_siguiente = cadena_actual[j+1]

                    v, estado_actual = self.simular_cadena(diccionario, estado_actual, caracter_actual, caracter_siguiente, estados_acept)

                    if estado_actual == {}:
                        estado_actual = estado_ini[0]
                        
                    if j == len(cadena_actual) - 2:
                        valores_cadena.append(v)

            if 'string' in self.tabla: 
            
                if self.cadena_copy[0] == '"' and self.cadena_copy[-1] == '"':
                    
                    self.cadena_strings.append(self.cadena_copy)

                    valores_cadena[-1] = True
                else:
                    valores_cadena[-1] = False
            
            if 'endline' in self.tabla:
                endline = self.tabla['endline']

                endline = endline.replace('(', '')
                endline = endline.replace(')', '')

                if valores_cadena[7] == True and valores_cadena[8] == True:
                    pass
                elif valores_cadena[7] == False and valores_cadena[8] == False:
                    pass
                elif valores_cadena[7] == False and valores_cadena[8] == True:

                    if cadena_actual in self.reservadas: 
                        pass
                    
                    else:
                        for i in range(len(valores_cadena)):
                            valores_cadena[i] == False
            
            self.diccionario_cadenas[cadena_actual] = valores_cadena

            resultado.append(valores_cadena)

            if True in valores_cadena:
                pass
            else:
                with open(self.archivo, "r") as archivos:
                    for i, linea in enumerate(archivos):
                        if cadena_actual in linea:
                            print("Sintax error: " + cadena_actual + " line: ", i+1)

            return self.simular_cadenas(diccionarios, iniciales, finales, resultado)
    
    def simular_res(self):
        ultima_vez_operador = False
        ultima_vez_reservada = False
        ultima_vez_token = {}

        diccionario = {}

        for clave in self.tokens:
            ultima_vez_token[clave] = False
        
        print(self.tokens)

        for clave in self.diccionario_cadenas:
            lista = self.diccionario_cadenas[clave]

            if len(lista) == 1:
                if lista[0] == True:
                    print("Operador detectado")
                
                elif lista[0] == False:
                    with open(self.archivo, "r") as ar:
                        for a, linea in enumerate(ar):
                            if clave in linea:
                                print("Sintax error: " + clave + " line: ", a+1)
            
            for i, valor in enumerate(lista):

                for s, (key, value) in enumerate(self.tabla.items()):

                    if valor == True:

                        if i == s:
                            if key in self.tokens:
                                if clave in self.reservadas:
                                    print("Palabra reservada: ", clave)
                                    ultima_vez_reservada = True
                                    ultima_vez_token[key] = False
                                    ultima_vez_operador = False
                                
                                elif key in self.operadores_reservados:

                                    if not ultima_vez_operador:
                                        print("Operador reservado: ", clave)
                                        ultima_vez_operador = True
                                        ultima_vez_reservada = False
                                        ultima_vez_token[key] = False
                                else: 

                                    ultima_vez_operador = False
                                    ultima_vez_reservada = False
                                    ultima_vez_token[key] = True

                                    diccionario[clave] = key

        new_dict =  {}

        for k, v in diccionario.items():
            if not isinstance(v, bool):
                new_dict[k] = v
        
        for keys, value in new_dict.items():


            if value == "string":

                string2 = self.cadena_strings.pop()

                comillas = 0
                palabra = ''
                for c in string2:
                    if c == '"':
                        comillas += 1
                        if comillas == 2:
                            print('"' + palabra.strip() + '"' + " type: " + value)
                            palabra = ''
                            comillas = 0
                    else:
                        palabra += c
                if palabra:
                    print('"' + palabra.strip() + '"')

            else: 
                print("Token: " + keys + " type: " + value)
        
    
    def simular_cadena(self, diccionario, estado_actual, caracter_actual, caracter_siguiente, estados_acept):

        transiciones = diccionario[estado_actual]
    
        if caracter_actual in transiciones:
            estado_siguiente = transiciones[caracter_actual]

            if estado_siguiente in estados_acept:
                return True, estado_actual

            if estado_siguiente == {}:

                return False, estado_actual
            
            elif estado_siguiente in estados_acept:
                return True, estado_actual
        
            else:

                return True, estado_siguiente
            
        elif caracter_siguiente in transiciones:

            estado_siguiente = transiciones[caracter_siguiente]

            if estado_siguiente in estados_acept:
                return True, estado_siguiente

            if estado_siguiente == {}:
                
                return False, estado_siguiente
            
            elif estado_siguiente in estados_acept:
                return True, estado_siguiente
        
            else:
                return True, estado_siguiente
        
        elif caracter_actual not in transiciones:

            return False, estado_actual
            
        else:

            if transiciones != {}:
                return True, estado_actual
            
            else: 
                return False, estado_actual

    def generar_py(self, nombre, diccionarios, iniciales, finales, archivo, reservadas, operadores_reservados, tokens, tabla):

        vacio = {}
        diccionario_cadenas = {}
        vacio2 = {}
        cadena_strings = []
    

        datas = f"""
diccionarios = {'{}'}
iniciales = {'{}'}
finales = {'{}'}
archiv = {'{}'}
reservadas = {'{}'}
vacio = {'{}'}
operadores_reservados = {'{}'}
tokens = {'{}'}
tabla = {'{}'}
diccionario_cadenas = {'{}'}
vacio2 = {'{}'}
cadena_strings = {'{}'}
    
def main():

    lista = []
    lista.extend(reservadas)
    lista.extend(operadores_reservados)
    lista.extend(tokens)

    res_copy = reservadas.copy()
    
    cad_s = [] 
    t = []
    cads = []


    with open(archiv, "r") as archivo:
        for linea in archivo:
            if linea[0] == '"' and linea[-1] == '"':
                cad_s.append(linea.strip())
                cads.append(linea.strip())
            else:
                cadenas = linea.strip().split()
                for cadena in cadenas:
                    if cadena[0] == '"' and cadena[-1] == '"':
                        cad_s.append(cadena.strip())
                        cads.append(linea.strip())
                    else:
                        cad_s.extend(cadena.split())
                        cads.append(linea.strip())
                t.extend(cadenas)

                cads.extend(linea.strip())

                cad_s.extend(cadenas)
    
    simular_cadenas(diccionarios, cad_s, iniciales, finales) 

    simular_res() 
    
def simular_cadenas(diccionarios, cad_s, iniciales, finales, resultado=[]):
    
    if not diccionarios:
        return resultado
    
    if len(cad_s) == 0:
        return resultado
    else: 

        cadena_actual = cad_s.pop(0)

        cadena_copy = cadena_actual
        
        if cadena_actual[0] == '"' and cadena_actual[-1] == '"':
            cadena_actual = cadena_actual.replace('"', '')

        valores_cadena = []
        for i in range(len(diccionarios)):
            diccionario = diccionarios[i]
            estado_ini = iniciales[i]
            estados_acept = finales[i]
            estado_actual = estado_ini[0]

            if len(cadena_actual) == 1:

                if cadena_actual in operadores_reservados:
                    
                    if i == len(diccionarios) - 1:
                        valores_cadena.append(True)
                
                else:
                    if i == len(diccionarios) - 1:
                        valores_cadena.append(False)
            
            for j in range(len(cadena_actual) - 1):
                caracter_actual = cadena_actual[j]
                caracter_siguiente = cadena_actual[j+1]

                v, estado_actual = simular_cadena(diccionario, estado_actual, caracter_actual, caracter_siguiente, estados_acept)

                if estado_actual == vacio:
                    estado_actual = estado_ini[0]
                
                if j == len(cadena_actual) - 2:
                    valores_cadena.append(v)
        
        if 'string' in tabla: 
            
            if cadena_copy[0] == '"' and cadena_copy[-1] == '"':
                
                cadena_strings.append(cadena_copy)

                valores_cadena[-1] = True
            else:
                valores_cadena[-1] = False

        if 'endline' in tabla:
            endline = tabla['endline']

            endline = endline.replace('(', '')
            endline = endline.replace(')', '')

            if valores_cadena[7] == True and valores_cadena[8] == True:
                pass
            elif valores_cadena[7] == False and valores_cadena[8] == False:
                pass
            elif valores_cadena[7] == False and valores_cadena[8] == True:

                if cadena_actual in reservadas: 
                    pass
                
                else:
                    for i in range(len(valores_cadena)):
                        valores_cadena[i] == False
        
        diccionario_cadenas[cadena_actual] = valores_cadena

        resultado.append(valores_cadena)

        if True in valores_cadena:
            pass
        else: 
            with open(archiv, "r") as ar:
                for a, linea in enumerate(ar):
                    if cadena_actual in linea:
                        print("Sintax error: " + cadena_actual + " line: ", a+1)

    return simular_cadenas(diccionarios, cad_s, iniciales, finales, resultado) 


def simular_cadena(diccionario, estado_actual, caracter_actual, caracter_siguiente, estados_acept):

    transiciones = diccionario[estado_actual]

    if caracter_actual in transiciones:
        estado_siguiente = transiciones[caracter_actual]


        if estado_siguiente in estados_acept:
            return True, estado_actual

        if estado_siguiente == vacio:
            return False, estado_actual
        
        elif estado_siguiente in estados_acept:
            return True, estado_actual
    
        else:
            return True, estado_siguiente
        
    elif caracter_siguiente in transiciones:

        estado_siguiente = transiciones[caracter_siguiente]

        if estado_siguiente in estados_acept:
            return True, estado_siguiente

        if estado_siguiente == vacio:
            
            return False, estado_siguiente
        
        elif estado_siguiente in estados_acept:
            return True, estado_siguiente
    
        else:
            return True, estado_siguiente
    
    elif caracter_actual not in transiciones:

        return False, estado_actual
        
    else:
        if transiciones != vacio:
            return True, estado_actual
        
        else: 
            return False, estado_actual

def simular_res(): 
    ultima_vez_operador = False
    ultima_vez_reservada = False
    ultima_vez_token = vacio

    diccionario = vacio

    for clave in tokens:
        ultima_vez_token[clave] = False
    
    print(diccionario_cadenas)

    for clave in diccionario_cadenas:
        lista = diccionario_cadenas[clave]

        if len(lista) == 1:
            if lista[0] == True:
                print("Operador detectado")
            
            elif lista[0] == False:
                with open(archiv, "r") as ar:
                    for a, linea in enumerate(ar):
                        if clave in linea:
                            print("Sintax error: " + clave + " line: ", a+1)
        
        for i, valor in enumerate(lista):

            for s, (key, value) in enumerate(tabla.items()):

                if valor == True:

                    if i == s:
                        if key in tokens:
                            if clave in reservadas:
                                print("Palabra reservada: ", clave)
                                ultima_vez_reservada = True
                                ultima_vez_token[key] = False
                                ultima_vez_operador = False
                            
                            elif key in operadores_reservados:

                                if not ultima_vez_operador:
                                    print("Operador reservado: ", clave)
                                    ultima_vez_operador = True
                                    ultima_vez_reservada = False
                                    ultima_vez_token[key] = False
                            else: 

                                ultima_vez_operador = False
                                ultima_vez_reservada = False
                                ultima_vez_token[key] = True

                                diccionario[clave] = key

    print("Diccionario: ", diccionario)    
    
    new_dict =  vacio2

    for k, v in diccionario.items():
        if not isinstance(v, bool):
            new_dict[k] = v
    
    print("Diccionario: ", new_dict)
    
    for keys, value in new_dict.items():


        if value == "string":

            string2 = cadena_strings.pop()

            comillas = 0
            palabra = ''
            for c in string2:
                if c == '"':
                    comillas += 1
                    if comillas == 2:
                        print('"' + palabra.strip() + '"' + " type: " + value)
                        palabra = ''
                        comillas = 0
                else:
                    palabra += c
            if palabra:
                print('"' + palabra.strip() + '"')

        else: 
            print("Token: " + keys + " type: " + value)
                

if __name__ == "__main__":
    main()

""".format(diccionarios, iniciales, finales, str('"{}"'.format(archivo)), reservadas, vacio, operadores_reservados, tokens, tabla, diccionario_cadenas, vacio2, cadena_strings)
        
        with open(nombre, 'w', encoding='utf-8') as f:
            f.write(datas)