class TransicionesAFN: 
    def __init__(self, estadoInicial, simbolo, estadoFinal):
        self.estadoInicial = estadoInicial
        self.estadoFinal = estadoFinal
        self.simbolo = simbolo

    def getEstadoInicial(self):
        return self.estadoInicial
    
    def getEstadoFinal(self):
        return self.estadoFinal
    
    def getSimbolo(self):
        return self.simbolo
    
    def setEstadoInicial(self, estadoInicial):
        self.estadoInicial = estadoInicial

    def setEstadoFinal(self, estadoFinal):
        self.estadoFinal = estadoFinal
    
    def __str__(self):
        return str(self.estadoInicial) + " -- " + str(self.simbolo) + " --> " + str(self.estadoFinal)
    
class AutomataAFN:
    def __init__(self, inicio, fin):
        self.estadoInicial = inicio
        self.estadoFinal = fin
        self.estadoGeneral = None

    def getEstadoInicial(self):
        return self.estadoInicial
    
    def getEstadoFinal(self):
        return self.estadoFinal

    def __str__(self):
        return str(self.estadoInicial) + " -- " + str(self.estadoFinal)
    
class EstadoAFN:
    def __init__(self, num):
        self.numero = num

    def __repr__(self):
        return str(self.numero)