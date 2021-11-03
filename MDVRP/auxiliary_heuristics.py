from customers import Customers as cst
from distances import Distances as dist
import math
import copy

class NearestNeighbor:
    _infinite = math.inf
    _path = []
    _availableCsts = {}

    '''
    Heurística do vizinho mais próximo
    Método calcula o menor caminho partindo de um cliente pré-definido
    '''
    def nearestNeighbor(startCustomer):
        NearestNeighbor._path = []
        NearestNeighbor._availableCsts = {}
        NearestNeighbor._availableCsts = copy.deepcopy(cst.get_customersList())
        NearestNeighbor._path.append(startCustomer)
        del NearestNeighbor._availableCsts[str(startCustomer.get_id())] #remover da lista
        currentCst = startCustomer
        for i in range(len(NearestNeighbor._availableCsts)):
            nextCst = NearestNeighbor.findNeighbor(currentCst)
            if nextCst is not None:
                NearestNeighbor._path.append(nextCst)
                currentCst = nextCst

        return NearestNeighbor._path

    '''
    Método encontra vizinho mais próximo
    '''
    def findNeighbor(currentCst):
        for neighbor in currentCst.get_neighborsDistances():
            if str(neighbor[0]) in NearestNeighbor._availableCsts: #cliente ainda não visitado
                next = NearestNeighbor._availableCsts[str(neighbor[0])]
                del NearestNeighbor._availableCsts[str(neighbor[0])] #retirar da lista
                return next
        return None
