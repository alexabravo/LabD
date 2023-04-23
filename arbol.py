from afd import *
import graphviz as gv

class Arbol:

    def __init__(self, expresionRegular, abc): 
        self.expresionRegular = expresionRegular
        self.abc = abc
        self.contador = 1 
        self.followpos = [] 
        self.followposT = []
        self.hojas = dict()
        self.estadosAFD = []
        self.EstadosAceptAFD = [] 
        self.EstadoInicial = None 
        self.transiciones = [] 
        self.terminal = None
        self.dict = {} 

        self.aumento() 
        self.tarbol = self.arbol() 
        self.tree = self.analisis(self.tarbol) 
        self.construir() 
        self.grafica() 


    def aumento(self): 
        self.expresionRegular = self.expresionRegular + "#."

    def anular(self, expresionRegular):
        if expresionRegular.etiqueta == "ε":
            return True
        
        elif expresionRegular.etiqueta == ".":
            return self.anular(expresionRegular.left) and self.anular(expresionRegular.right)
        elif expresionRegular.etiqueta == "|":

            return self.anular(expresionRegular.left) or self.anular(expresionRegular.right)
        elif expresionRegular.etiqueta == "*":
            return True
        
        elif expresionRegular.etiqueta not in ["|", ".", "*"]:
            return False
            
        
    def arbol(self): 
        pila = []
        resultado = []
        operaciones = ["|", ".", "*"]

        for c in self.expresionRegular:

            if c not in operaciones: 
                nodo1 = NodoAFD(etiqueta=c)
                pila.append(nodo1)

                resultado.append(nodo1)

            elif c == ".": 
                derecha1 = pila.pop()
                izquierda1 = pila.pop()

                nodo2 = NodoAFD(etiqueta=c, left=izquierda1, right=derecha1)

                pila.append(nodo2)

                resultado.append(nodo2)
            
            elif c == "@": 

                print("Suma")
                nodoo = NodoAFD(etiqueta="+")
                pila.append(nodoo)
                resultado.append(nodoo)
            
            elif c == "~": 

                nodoo = NodoAFD(etiqueta="-")
                pila.append(nodoo)
                resultado.append(nodoo)
            
            elif c == "≡": 
                nods = NodoAFD(etiqueta="≡")

                pila.append(nods)
                resultado.append(nods)

            elif c == "¥": 

                nod = NodoAFD(etiqueta="¥")
                pila.append(nod)
                resultado.append(nod)
            
            elif c == "§": 

                no = NodoAFD(etiqueta="§")

            elif c == "|":

                derecha2 = pila.pop()
                izquierda2 = pila.pop()

                nodo3 = NodoAFD(etiqueta=c, left=izquierda2, right=derecha2)

                pila.append(nodo3)

                resultado.append(nodo3)
            
            elif c == "*":

                hijo = pila.pop()

                nodo4 = NodoAFD(etiqueta=c, child=hijo)

                pila.append(nodo4)

                resultado.append(nodo4)


        return resultado

    def siguientePosicion(self, n):
    
        if n.etiqueta == ".":
            for i in n.left.lastP:
                self.followpos[i] = self.followpos[i].union(n.right.firstP)
        
        if n.etiqueta == "*": 
            for i in n.child.lastP:
                self.followpos[i] = self.followpos[i].union(n.child.firstP)
    
    def primeraPosicion(self, b):
        if b.etiqueta == "ε":
            pass
        elif b.etiqueta == ".":
            
            if b.left.Null:
                b.firstP = b.left.firstP.union(b.right.firstP)
            else:
                b.firstP = b.left.firstP
        
        
        elif b.etiqueta == "|":

            b.firstP = b.child.firstP
        
        elif b.etiqueta == "*":
        
            b.firstP = b.child.firstP
        
        elif b.etiqueta not in ["|", ".", "*"]:
            
            b.firstP.add(b.id)
    
    def ultimaPosicion(self, b):
        if b.etiqueta == "ε":
            pass
        elif b.etiqueta == ".":
            
            if b.right.Null:
                    b.lastP = b.left.lastP.union(b.right.lastP)
            else:
                b.lastP = b.right.lastP

        elif b.etiqueta == "|":
            
            b.lastP = b.child.lastP

        elif b.etiqueta == "*":
            
            b.lastP = b.child.lastP

        elif b.etiqueta not in ["|", ".", "*"]:
            
            b.lastP.add(b.id)
    
    def analisis(self, arbol): 

        diccionario = {} 

        for i in range(len(arbol)-1, -1, -1):
            if arbol[i].etiqueta == ".":
                arbol[i].raiz = True
                break


        for c in arbol:
            if c.etiqueta == "|":
                diccionario[c] = [c.left, c.right]

            elif c.etiqueta == ".":
                diccionario[c] = [c.left, c.right]
            
            elif c.etiqueta == "*":
                diccionario[c] = [c.child]
            
        for c in arbol:
            if c.etiqueta not in ["|", ".", "*"]:
                c.id = self.contador
                self.contador += 1

        
        self.followpos = [set() for i in range(self.contador)]

        for a in arbol:
            a.Null = self.anular(a)


        for b in arbol:
            
            if b.etiqueta not in ["|", ".", "*"]:

                self.primeraPosicion(b)
                self.ultimaPosicion(b)

            elif b.etiqueta == "|": 
                b.firstP = b.left.firstP.union(b.right.firstP)
                b.lastP = b.left.lastP.union(b.right.lastP)

            elif b.etiqueta == "*": 
                b.firstP = b.child.firstP
                b.lastP = b.child.lastP
                
                self.siguientePosicion(b)
            
            elif b.etiqueta == ".": 
                if b.left.Null:
                    b.firstP = b.left.firstP.union(b.right.firstP)
                else:
                    b.firstP = b.left.firstP
                
                if b.right.Null:
                    b.lastP = b.left.lastP.union(b.right.lastP)
                else:
                    b.lastP = b.right.lastP
                

                self.siguientePosicion(b) 
            
            elif b.etiqueta == "ε":
                pass
        
        for c in arbol:
            if c.etiqueta not in ["|", ".", "*"]:
                self.hojas[c.id] = c.etiqueta

        return arbol
    
    
    def construir(self): 

        id_c = 0
        ter = [] 
        first_p = set()


        for i in range(len(self.tree)-1, -1, -1):
            if self.tree[i].etiqueta == "#":
                ter.append(self.tree[i].id)
                break
        
        self.terminal = ter.pop() 

        for i in range(len(self.tree)-1, -1, -1):
            if self.tree[i].etiqueta == ".":

                for p in self.tree[i].firstP:
                    first_p.add(p)
                break
   
        estado_inicial = EstadoAFD(alfabeto=self.abc, id_list=first_p, id=id_c, terminal_id=self.terminal)

        self.EstadoInicial = estado_inicial
        
        id_c += 1 

        self.estadosAFD.append(estado_inicial) 

        queue = [estado_inicial] 
        
        while len(queue) > 0: 
            st = queue.pop(0)
            nuevo_estado = self.DTran(st, self.terminal)

            for s in nuevo_estado:
                estadoo = EstadoAFD(self.abc, s, id_c, self.terminal)
                self.estadosAFD.append(estadoo)
                queue.append(estadoo)
                id_c += 1

        for e in self.estadosAFD:
            if self.terminal in e.id_set:
                self.EstadosAceptAFD.append(e)

        sin_estado = False
        for estado in self.estadosAFD:
            for a in self.abc:
                if estado.transitions[a] == {}:
                    sin_estado = True
                    estado.transitions[a] == id_c
                
                SET = estado.transitions[a]
                for estado2 in self.estadosAFD:
                    if estado2.id_set == SET:
                        estado.transitions[a] = estado2 

    def DTran(self, estado, terminal): 

        nuevo_estado = []
        for i in estado.id_set:
            if i == terminal:
                continue
            
            label = self.hojas[i] 

            if estado.transitions[label] == {}: 
                estado.transitions[label] = self.followpos[i]
            
            else: 
                estado.transitions[label] = estado.transitions[label].union(self.followpos[i])
            
        for a in self.abc: 
            if estado.transitions[a] != {}:
                nuevo = True
                for e in self.estadosAFD:
                    if (e.id_set == estado.transitions[a]) or (estado.transitions[a] in nuevo_estado):
                        nuevo = False
                
                if nuevo:
                    nuevo_estado.append(estado.transitions[a])
            
        return nuevo_estado
    
    def simularAFD(self): 
        print("Estados. ", self.estadosAFD)

        diccionario = {}

        trans = []

        for estado in self.estadosAFD:
            
            diccionario[estado] = estado.transitions

        
        print("Diccionario: ", diccionario)

        cadena = input("Ingrese la cadena: ")

        estado_actual = self.EstadoInicial 

        print("Tipo del estado inicial: ", type(estado_actual))

        for simbolo in cadena:
            if simbolo not in self.abc:
                print("La cadena no es aceptada en este lenguaje.")
                break
            

            estado_actual = diccionario[estado_actual][simbolo] 
            
            if estado_actual != {}:
                continue
            else: 
                print("Cadena no aceptada")
                break


        if estado_actual in self.EstadosAceptAFD:
            print("Cadena aceptada.")
            
        else: 
            print("Cadena rechazada.")
                    
    def grafica(self): 
        grafo = gv.Digraph(comment="AFD", format="png")
        grafo.node('title', 'AFD', shape='none')


        for estado in self.estadosAFD:
            for a in self.abc:
                
                trans = estado.transitions[a]

                if trans == {}:
                    continue
                else:

                    if a == "@": 
                        a = "+"
                    if a == '~': 
                        a = "-"
                    if a == "≡": 
                        a = "bb"
                    if a == "¥": 
                        a = "\yt"
                    if a == "§": 
                        a = "\yn"

                    grafo.edge(str(estado), str(trans), label=a)

        for esta in self.estadosAFD:
    
            if esta in self.EstadosAceptAFD:

                grafo.node(str(esta), str(esta), shape="doublecircle")
            
            elif esta == self.EstadoInicial: 

                grafo.node(str(esta), str(esta), shape="circle", color="green")

            else:
                grafo.node(str(esta), str(esta), shape="circle")
        

        grafo.render('AFDfinal', view=True) 

        for estado in self.estadosAFD:
            self.dict[estado] = estado.transitions
        
    def minimizar(self):
        
        diccionario_m = {}
        finales_m = []
        estados_m = []
        inicial_m = []
        
        diccionario = {}

        for estado in self.estadosAFD:

            diccionario[estado] = {}

            for a in self.abc:
                
                trans = estado.transitions[a]

                diccionario[estado][a] = trans
        
        particiones = [[s for s in self.estadosAFD if s in self.EstadosAceptAFD], 
                       [s for s in self.estadosAFD if s not in self.EstadosAceptAFD]]
        
        def buscar_particion(estado):

            for i, partition in enumerate(particiones):
                
                if estado in partition:
                    return i
        
        itera = True

        while itera:
            new_partitions = []

            for partition in particiones:

                equivalent_states = {}
                for state in partition:
                    transiciones = [diccionario[state][simbolo] for simbolo in self.abc]

                    transiciones = [t for t in transiciones if t != {}]

                    equivalent_states.setdefault(tuple(transiciones), []).append(state)
                
                subpartitions = list(equivalent_states.values())
                if len(subpartitions) > 0:
                    new_partitions.extend(subpartitions)
                else: 
                    new_partitions.append(partition)
                
                particione = []
                for particion in new_partitions:
                    particione.append([estado for estado in particion])
            
                if new_partitions == particione:
                    itera = False
                
                
                particiones = new_partitions 

                for i, partition in enumerate(particiones):
                    if self.EstadoInicial in partition:
                        inicial_m.append(self.EstadoInicial.id)

        new_states = [tuple(partition) for partition in particiones]
        
        new_transitions = {}

        for estad in self.estadosAFD:
            particion = buscar_particion(estad)

            for simbolo in self.abc:


                llegada = diccionario[estad][simbolo]

                new = tuple(sorted([buscar_particion(llegada)]))

                if new[0] is None: 
                    continue

                new_transitions[(new_states[particion], simbolo)] = new_states[new[0]]
                
        new_finals = []
        
        for estadoA in self.EstadosAceptAFD:
            final = buscar_particion(estadoA)

            new_finals.append(new_states[final])
        
        for tupla in new_states:
            if tupla in new_finals:
                indice = new_states.index(tupla)
                new_states.append(new_states.pop(indice))
    
        new_dict = {}

        for i, tupla in enumerate(new_states):

            new_dict[tupla] = i

        for tup, val in new_transitions.items(): 
            diccionario_m[(new_dict[tup[0]], tup[1])] = new_dict[val]
            
            if tup[0] in inicial_m or val in inicial_m:
                inicial_m.append(new_dict[val])
                inicial_m.append[new_dict[tup[0]]]

            estados_m.append(new_dict[val])
            estados_m.append(new_dict[tup[0]])
        
        for estado in new_states: 
            print("Estado en el Arbol: ", estado)
            if estado in new_finals:
                finales_m.append(new_dict[estado])

        inicial_m = list(set(inicial_m))
        finales_m = list(set(finales_m))
        estados_m = list(set(estados_m))

        for i, estado in enumerate(estados_m):
            estados_m[i] = int(estado)
        
        for i, estado in enumerate(finales_m):
            finales_m[i] = int(estado)
        
        for i, estado in enumerate(inicial_m):
            inicial_m[i] = int(estado)


        diccionario_temporal = {}

        for c, v in diccionario_m.items():
            if c[0] not in diccionario_temporal:
                diccionario_temporal[c[0]] = {}
            diccionario_temporal[c[0]][c[1]] = v

        diccionario_m = diccionario_temporal.copy()

        new_t = {} 
        for keys, values in diccionario_m.items():
            new_t[keys] = [(k, v) for k, v in values.items()]
        
        diccionario_m = new_t.copy()

        for estado in estados_m:
            if estado not in diccionario_m:
                estados_m.remove(estado)

            if estado in inicial_m: 
                inicial_m.remove(estado)


        inicial_m.append(estados_m[0])

        print("Inicial en Arbol: ", inicial_m)
        print("Final en el Arbol: ", finales_m)

        self.simular_AFD_min(diccionario_m, estados_m, inicial_m, finales_m)

        grafo = gv.Digraph(comment="AFD_Directo_Minimizado", format="png")
        grafo.node('title', 'AFD Minimizado', shape='none')

        for ke, va in diccionario_m.items():
            
            for ks, vs in va: 
                grafo.edge(str(ke), str(vs), label=str(ks))

        for estado in estados_m:
            
            if estado in finales_m:
                
                grafo.node(str(estado), str(estado), shape="doublecircle")
            
            elif estado in inicial_m:

                grafo.node(str(estado), str(estado), shape="circle", color="green")
            
            else:
            
                grafo.node(str(estado), str(estado), shape="circle")

        grafo.graph_attr['rankdir'] = 'LR'

        grafo.render('AFD_Directo_Minimizado', view=True) 

    def simular_AFD_min(self, diccionario_m, estados_m, inicial_m, finales_m):
        
        diccionario_simulacion = {}

        for c, v in diccionario_m.items():
            estado_actual = c
            trans = {}

            for simb, sig in v: 
                trans[simb] = sig
            
            diccionario_simulacion[estado_actual] = trans
        
        print("Diccionario simulación: ", diccionario_simulacion)

        cadena = input("Ingrese la cadena a simular: ")

        estado_actual = inicial_m.pop()


        for simbolo in cadena:
            if simbolo not in self.abc:
                print("El símbolo no pertenece al alfabeto.")
                return
            
            if simbolo in diccionario_simulacion[estado_actual]:
                estado_actual = diccionario_simulacion[estado_actual][simbolo]
            else:
                continue

        if estado_actual in finales_m:
            print("Cadena aceptada.")
        else:
            print("Cadena rechazada.")