class EstadoAFD:
    def __init__(self, alfabeto, id_list, id, terminal_id):
        self.id = id
        self.id_set = set(id_list) 
        self.transitions = dict()
        self.final = terminal_id in self.id_set 

        for a in alfabeto:
            self.transitions[a] = {}
        
    def __repr__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)
    
class NodoAFD:
    def __init__(self, etiqueta=None, child=None, left=None, right=None):
        self.etiqueta = etiqueta
        self.child = child
        self.left = left
        self.right = right
        self.raiz = False
        self.id = None
        self.Null = None
        self.firstP = set()
        self.lastP = set()

    def __iter__(self):
        if self.etiqueta != None:
            yield self.etiqueta
        elif self.child != None:
            yield self.child
        elif self.left != None:
            yield self.left
        elif self.right != None:
            yield self.right

    def __repr__(self):
        if self.etiqueta != None:
            return str(self.etiqueta)
        elif self.child != None:
            return str(self.child)
        elif self.left != None:
            return str(self.left)
        elif self.right != None:
            return str(self.right)