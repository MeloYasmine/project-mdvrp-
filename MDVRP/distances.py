'''
Arquivo responsável por computar distâncias entres clientes e distâncias entre clientes e depósitos
@author Fabiana Barreto Pereira
'''

import math
from operator import itemgetter, attrgetter
from collections import OrderedDict


class Distances:

    '''
    Método calcula distância euclidiana entre dois pontos cartezianos (x1,y1) e (x2,y2)
    @return distância
    '''
    def euclidianDistance(x1, y1, x2, y2):
        return math.sqrt(math.pow((x1-x2), 2)+math.pow((y1-y2), 2))

    '''
    Método calcula distância de um cliente para todos os clientes
    @return dicionário com as distâncias do cliente informado para cada cliente
    '''
    def euclidianDistanceNeighbors(customer, customers):
        distances = []
        for cst in customers.values():
            if cst.get_id() != customer.get_id():
                dist = Distances.euclidianDistance(customer.get_x_coord(
                ), customer.get_y_coord(), cst.get_x_coord(), cst.get_y_coord())
                distances.append([cst.get_id(), dist])

        distancesOrd = sorted(distances, key=lambda x: x[1])
        return distancesOrd

    '''
    Método calcula distância de um cliente para todos os depósitos
    @return dicionário com as distâncias do cliente informado para cada depósito
    '''
    def euclidianDistanceDepots(customer, depots):
        distances = []
        for dpt in depots.values():
            dist = Distances.euclidianDistance(customer.get_x_coord(
            ), customer.get_y_coord(), dpt.get_x_coord(), dpt.get_y_coord())
            distances.append((dpt.get_id(), dist))

        distancesOrd = sorted(distances, key=lambda x: x[1])
        return distancesOrd

    '''
    Método calcula distância de todos para todos
    '''
    def euclidianDistanceAll(customers, depots):
        for cst in customers.values():
            cst.set_neighborsDistances(
                Distances.euclidianDistanceNeighbors(cst, customers))
            cst.set_depotsDistances(
                Distances.euclidianDistanceDepots(cst, depots))
