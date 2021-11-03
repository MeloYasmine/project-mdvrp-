from collections import Counter
from distances import Distances as dist
from depots import Depots as dpts
from movimentsLocalSearch import MovimentsLocalSearch as mov
import copy
import config
import numpy as np
import random
import math
import time

'''
Pesquisa local de Prins2004
'''


class LocalSearchBest:

    def LS(self, solution, prob=config.PROB_LS_BEST, nMovimentations='all', where=None, timeIni=0, timeMax=math.inf):
        '''
        Cada iteração varre todos os pares possíveis de nós distintos (u,v). Esses nós podem pertencer à mesma viagem ou a viagens diferentes
        e um deles pode ser o depósito. x e y são os sucessores de u e v em suas respectivas viagens.
        @param Where opcional, para indicar onde o método é chamado, opções: None default ou 'ls'
        @param nMovimentations, para indicar se serão utilizados todos os movimentos ou apenas alguns. Opções: 'all' default ou 'random'
        '''
        self._M = mov()
        movimentation = [self.M1, self.M2, self.M3, self.M4,
                         self.M5, self.M6, self.M7, self.M8, self.M9, self.M10]
        # movimentation = [self.M1a, self.M1b, self.M2a, self.M2b, self.M3a, self.M3b, self.M4a,
        #                  self.M4b, self.M5a, self.M5b, self.M6a, self.M6b, self.M7, self.M8, self.M9, self.M10]
        lenght = len(movimentation)
        prob = config.PROB_LS
        # embaralhar os movimentos
        if nMovimentations == 'random':
            n = max(2, round(0.8*lenght))
            p = np.random.randint(1, n+1)
            movimentation = np.random.choice(movimentation, p, replace=True)
        else:
            # p = np.random.randint(1,lenght)
            # prob = config.PROB_LS_BEST
            movimentation = np.random.choice(
                movimentation, lenght, replace=True)

        bestSolution = None
        bestSolution = copy.deepcopy(solution)

        if (where == 'ls' and np.random.random_sample() < prob) or where == None:
            # print("vai mudar")
            # print(bestSolution)
            # print(bestSolution.get_routes())
            cont = 0
            for i, m in enumerate(movimentation):
                # print(m)
                # print(solution)
                # print(solution.get_routes())
                # print("vai passar .................")
                solution1 = None
                solution1 = m(copy.deepcopy(bestSolution), timeIni, timeMax)
                tour = solution1.get_giantTour()
                for i, c1 in enumerate(tour):
                    for j, c2 in enumerate(tour):
                        if i != j and c1 == c2:
                            print("Elementos iguais na LS")
                            print(solution1)
                            print(solution1.get_routes())
                            exit(1)

                if solution1.get_cost() < bestSolution.get_cost():
                    bestSolution = copy.deepcopy(solution1)
                    cont = 0
                else:
                    cont += 1
                    # print("achou melhor ------------------------- best\n\n\n")
                if cont > 4:
                    # excluir rotas vazias
                    bestSolution.removeRoutesEmpty()
                    # print("bestSolution")
                    # print(bestSolution)
                    return bestSolution

                if timeMax < (time.time()-timeIni):
                    break

            # excluir rotas vazias
            bestSolution.removeRoutesEmpty()
            # print("não achou melhor")
        return bestSolution

    def movimentRoutes(self, solution, moviment, timeIni=0, timeMax=math.inf):
        bestCost = math.inf
        bestIdRouteU = -1
        bestIdRouteV = -1
        bestIdU = -1
        bestIdV = -1
        for idRouteU, routeU in enumerate(solution.get_routes()):
            lenghtRouteU = len(routeU.get_tour())
            for idU in range(lenghtRouteU):
                for idRouteV, routeV in enumerate(solution.get_routes()):
                    lenghtRouteV = len(routeV.get_tour())
                    for idV in range(lenghtRouteV):
                        cost1 = moviment(solution, idRouteU, idRouteV,
                                         idU, idV, onlyCost=True)[1]
                        # print("cost1: {}".format(cost1))
                        if cost1 < bestCost:
                            bestCost = cost1
                            bestIdRouteU = idRouteU
                            bestIdRouteV = idRouteV
                            bestIdU = idU
                            bestIdV = idV
                        if timeMax < (time.time()-timeIni):
                            break
                    if timeMax < (time.time()-timeIni):
                        break
                if timeMax < (time.time()-timeIni):
                    break
            if timeMax < (time.time()-timeIni):
                break
        bestSolution = moviment(solution, bestIdRouteU, bestIdRouteV,
                                bestIdU, bestIdV)[0]
        return bestSolution

    def movimentIntraRoutes(self, solution, moviment, timeIni=0, timeMax=math.inf):
        bestCost = math.inf
        bestIdRouteU = -1
        bestIdU = -1
        bestIdV = -1
        for idRouteU, routeU in enumerate(solution.get_routes()):
            lenghtRouteU = len(routeU.get_tour())
            for idU in range(lenghtRouteU-1):
                for idV in range(lenghtRouteU-1):
                    if idU != idV:
                        cost1 = moviment(solution, idRouteU, idRouteU,
                                         idU, idV, onlyCost=True)[1]
                        # print("cost1: {}".format(cost1))
                        if cost1 < bestCost:
                            bestCost = cost1
                            bestIdRouteU = idRouteU
                            bestIdU = idU
                            bestIdV = idV
                if timeMax < (time.time()-timeIni):
                    break
            if timeMax < (time.time()-timeIni):
                break

        bestSolution = moviment(solution, bestIdRouteU, bestIdRouteU,
                                bestIdU, bestIdV)[0]
        return bestSolution

    def movimentInterRoutes(self, solution, moviment, timeIni=0, timeMax=math.inf):
        bestCost = math.inf
        bestIdRouteU = -1
        bestIdRouteV = -1
        bestIdU = -1
        bestIdV = -1
        for idRouteU, routeU in enumerate(solution.get_routes()):
            lenghtRouteU = len(routeU.get_tour())
            for idU in range(lenghtRouteU):
                for idRouteV, routeV in enumerate(solution.get_routes()):
                    lenghtRouteV = len(routeV.get_tour())
                    for idV in range(lenghtRouteV):
                        if idRouteU != idRouteV and idU != idV:
                            cost1 = moviment(solution, idRouteU, idRouteV,
                                             idU, idV, onlyCost=True)[1]
                            # print("cost1: {}".format(cost1))
                            if cost1 < bestCost:
                                bestCost = cost1
                                bestIdRouteU = idRouteU
                                bestIdRouteV = idRouteV
                                bestIdU = idU
                                bestIdV = idV
                        if timeMax < (time.time()-timeIni):
                            break
                    if timeMax < (time.time()-timeIni):
                        break
                if timeMax < (time.time()-timeIni):
                    break
            if timeMax < (time.time()-timeIni):
                break

        bestSolution = moviment(solution, bestIdRouteU, bestIdRouteV,
                                bestIdU, bestIdV)[0]
        return bestSolution

    def M1(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se u e v for um nó cliente, remova u e insira-o após v.
        '''
        return self.movimentRoutes(solution, self._M.removeUinsertAfterV, timeIni, timeMax)

    def M1a(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se T(u) == T(v) e Se u e v for um nó cliente, remova u e insira-o após v.
        '''
        return self.movimentIntraRoutes(solution, self._M.removeUinsertAfterV, timeIni, timeMax)

    def M1b(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se T(u) != T(v) e Se u e v for um nó cliente, remova u e insira-o após v.
        '''
        return self.movimentInterRoutes(solution, self._M.removeUinsertAfterV, timeIni, timeMax)

    def M2(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se u e x forem clientes, remova-os e insira (u,x) após v
        '''
        bestCost = math.inf
        bestIdRouteU = -1
        bestIdRouteV = -1
        bestIdU = -1
        bestIdV = -1
        for idRouteU, routeU in enumerate(solution.get_routes()):
            lenghtRouteU = len(routeU.get_tour())
            for idU in range(lenghtRouteU-1):
                for idRouteV, routeV in enumerate(solution.get_routes()):
                    lenghtRouteV = len(routeV.get_tour())
                    for idV in range(lenghtRouteV):
                        # se u e x são diferentes de v
                        if idU != idV and idU+1 != idV:
                            cost1 = self._M.removeUXinsertAfterV(solution, idRouteU, idRouteV,
                                                                 idU, idV, onlyCost=True)[1]
                            # print("cost1: {}".format(cost1))
                            if cost1 < bestCost:
                                bestCost = cost1
                                bestIdRouteU = idRouteU
                                bestIdRouteV = idRouteV
                                bestIdU = idU
                                bestIdV = idV
                        if timeMax < (time.time()-timeIni):
                            break
                    if timeMax < (time.time()-timeIni):
                        break
                if timeMax < (time.time()-timeIni):
                    break
            if timeMax < (time.time()-timeIni):
                break

        bestSolution = self._M.removeUXinsertAfterV(solution, bestIdRouteU, bestIdRouteV,
                                                    bestIdU, bestIdV)[0]
        return bestSolution

    def M2a(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se T(u) == T(v) e Se u e x forem clientes, remova-os e insira (u,x) após v
        '''
        return self.movimentIntraRoutes(solution, self._M.removeUXinsertAfterV, timeIni, timeMax)

    def M2b(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se T(u) != T(v) e Se u e x forem clientes, remova-os e insira (u,x) após v
        '''
        return self.movimentInterRoutes(solution, self._M.removeUXinsertAfterV, timeIni, timeMax)

    def M3(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se u e x forem clientes, remova-os e insira (x,u) após v
        '''
        bestCost = math.inf
        bestIdRouteU = -1
        bestIdRouteV = -1
        bestIdU = -1
        bestIdV = -1
        for idRouteU, routeU in enumerate(solution.get_routes()):
            lenghtRouteU = len(routeU.get_tour())
            for idU in range(lenghtRouteU-1):
                for idRouteV, routeV in enumerate(solution.get_routes()):
                    lenghtRouteV = len(routeV.get_tour())
                    for idV in range(lenghtRouteV):
                        # se u e x são diferentes de v
                        if idU != idV and idU+1 != idV:
                            cost1 = self._M.removeUXinsertXUAfterV(solution, idRouteU, idRouteV,
                                                                   idU, idV, onlyCost=True)[1]
                            # print("cost1: {}".format(cost1))
                            if cost1 < bestCost:
                                bestCost = cost1
                                bestIdRouteU = idRouteU
                                bestIdRouteV = idRouteV
                                bestIdU = idU
                                bestIdV = idV
                        if timeMax < (time.time()-timeIni):
                            break
                    if timeMax < (time.time()-timeIni):
                        break
                if timeMax < (time.time()-timeIni):
                    break
            if timeMax < (time.time()-timeIni):
                break

        bestSolution = self._M.removeUXinsertXUAfterV(solution, bestIdRouteU, bestIdRouteV,
                                                      bestIdU, bestIdV)[0]
        return bestSolution

    def M3a(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se T(u) == T(v) e Se u e x forem clientes, remova-os e insira (x,u) após v
        '''
        return self.movimentIntraRoutes(solution, self._M.removeUXinsertXUAfterV, timeIni, timeMax)

    def M3b(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se T(u) != T(v) e Se u e x forem clientes, remova-os e insira (x,u) após v
        '''
        return self.movimentInterRoutes(solution, self._M.removeUXinsertXUAfterV, timeIni, timeMax)

    def M4(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se u e v forem clientes, troque u e v
        '''
        bestCost = math.inf
        bestIdRouteU = -1
        bestIdRouteV = -1
        bestIdU = -1
        bestIdV = -1
        size = len(solution.get_routes())
        for idRouteU in range(size-1):
            routeU = solution.get_routes()[idRouteU]
            lenghtRouteU = len(routeU.get_tour())
            for idU in range(lenghtRouteU):
                for idRouteV in range(idRouteU, size):
                    routeV = solution.get_routes()[idRouteV]
                    lenghtRouteV = len(routeV.get_tour())
                    for idV in range(lenghtRouteV):
                        cost1 = self._M.swap(solution, idRouteU, idRouteV,
                                             idU, idV, onlyCost=True)[1]
                        # print("cost1: {}".format(cost1))
                        if cost1 < bestCost:
                            bestCost = cost1
                            bestIdRouteU = idRouteU
                            bestIdRouteV = idRouteV
                            bestIdU = idU
                            bestIdV = idV
                        if timeMax < (time.time()-timeIni):
                            break
                    if timeMax < (time.time()-timeIni):
                        break
                if timeMax < (time.time()-timeIni):
                    break
            if timeMax < (time.time()-timeIni):
                break

        bestSolution = self._M.swap(solution, bestIdRouteU, bestIdRouteV,
                                    bestIdU, bestIdV)[0]
        return bestSolution

    def M4a(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se T(u) == T(v) e Se u e v forem clientes, troque u e v
        '''
        return self.movimentIntraRoutes(solution, self._M.swap, timeIni, timeMax)

    def M4b(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se T(u) != T(v) e Se u e v forem clientes, troque u e v
        '''
        return self.movimentInterRoutes(solution, self._M.swap, timeIni, timeMax)

    def M5(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se u, x e v são clientes, troque (u,x) e v
        '''
        bestCost = math.inf
        bestIdRouteU = -1
        bestIdRouteV = -1
        bestIdU = -1
        bestIdV = -1
        for idRouteU, routeU in enumerate(solution.get_routes()):
            lenghtRouteU = len(routeU.get_tour())
            for idU in range(lenghtRouteU-1):
                for idRouteV, routeV in enumerate(solution.get_routes()):
                    lenghtRouteV = len(routeV.get_tour())
                    for idV in range(lenghtRouteV):
                        cost1 = self._M.shiftUXwithV(solution, idRouteU, idRouteV,
                                                     idU, idV, onlyCost=True)[1]
                        # print("cost1: {}".format(cost1))
                        if cost1 < bestCost:
                            bestCost = cost1
                            bestIdRouteU = idRouteU
                            bestIdRouteV = idRouteV
                            bestIdU = idU
                            bestIdV = idV
                        if timeMax < (time.time()-timeIni):
                            break
                    if timeMax < (time.time()-timeIni):
                        break
                if timeMax < (time.time()-timeIni):
                    break
            if timeMax < (time.time()-timeIni):
                break

        bestSolution = self._M.shiftUXwithV(solution, bestIdRouteU, bestIdRouteV,
                                            bestIdU, bestIdV)[0]
        return bestSolution

    def M5a(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se T(u) == T(v) e Se u, x e v são clientes, troque (u,x) e v
        '''
        return self.movimentIntraRoutes(solution, self._M.shiftUXwithV, timeIni, timeMax)

    def M5b(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se T(u) != T(v) e Se u, x e v são clientes, troque (u,x) e v
        '''
        return self.movimentInterRoutes(solution, self._M.shiftUXwithV, timeIni, timeMax)

    def M6(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se u, x, v e y são clientes, troque (u,x) e (v,y)
        '''
        bestCost = math.inf
        bestIdRouteU = -1
        bestIdRouteV = -1
        bestIdU = -1
        bestIdV = -1
        for idRouteU, routeU in enumerate(solution.get_routes()):
            lenghtRouteU = len(routeU.get_tour())
            for idU in range(lenghtRouteU-1):
                for idRouteV, routeV in enumerate(solution.get_routes()):
                    lenghtRouteV = len(routeV.get_tour())
                    for idV in range(lenghtRouteV-1):
                        cost1 = self._M.shiftUXwithVY(solution, idRouteU, idRouteV,
                                                      idU, idV, onlyCost=True)[1]
                        # print("cost1: {}".format(cost1))
                        if cost1 < bestCost:
                            bestCost = cost1
                            bestIdRouteU = idRouteU
                            bestIdRouteV = idRouteV
                            bestIdU = idU
                            bestIdV = idV
                        if timeMax < (time.time()-timeIni):
                            break
                    if timeMax < (time.time()-timeIni):
                        break
                if timeMax < (time.time()-timeIni):
                    break
            if timeMax < (time.time()-timeIni):
                break

        bestSolution = self._M.shiftUXwithVY(solution, bestIdRouteU, bestIdRouteV,
                                             bestIdU, bestIdV)[0]
        return bestSolution

    def M6a(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se T(u) == T(v) e Se u, x, v e y são clientes, troque (u,x) e (v,y)
        '''
        return self.movimentIntraRoutes(solution, self._M.shiftUXwithVY, timeIni, timeMax)

    def M6b(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se T(u) != T(v) e Se u, x, v e y são clientes, troque (u,x) e (v,y)
        '''
        return self.movimentInterRoutes(solution, self._M.shiftUXwithVY, timeIni, timeMax)

    def M7(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se T(u) == T(v), substitua (u,x) e (v,y) por (u,v) e (x,y)
        '''
        return self.movimentIntraRoutes(solution, self._M.shiftUXVYwithUVXY, timeIni, timeMax)

    def M8(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se T(u) != T(v), substitua (u,x) e (v,y) por (u,v) e (x,y)
        '''
        bestCost = math.inf
        bestIdRouteU = -1
        bestIdRouteV = -1
        bestIdU = -1
        bestIdV = -1
        for idRouteU, routeU in enumerate(solution.get_routes()):
            lenghtRouteU = len(routeU.get_tour())
            for idU in range(lenghtRouteU-1):
                for idRouteV, routeV in enumerate(solution.get_routes()):
                    lenghtRouteV = len(routeV.get_tour())
                    for idV in range(lenghtRouteV-1):
                        if idRouteU != idRouteV and idU != idV:
                            cost1 = self._M.shiftUXVYwithUVXY(solution, idRouteU, idRouteV,
                                                              idU, idV, onlyCost=True)[1]
                            # print("cost1: {}".format(cost1))
                            if cost1 < bestCost:
                                bestCost = cost1
                                bestIdRouteU = idRouteU
                                bestIdRouteV = idRouteV
                                bestIdU = idU
                                bestIdV = idV
                        if timeMax < (time.time()-timeIni):
                            break
                    if timeMax < (time.time()-timeIni):
                        break
                if timeMax < (time.time()-timeIni):
                    break

        bestSolution = self._M.shiftUXVYwithUVXY(solution, bestIdRouteU, bestIdRouteV,
                                                 bestIdU, bestIdV)[0]
        return bestSolution

    def M9(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se T(u) != T(v), substitua (u,x) e (v,y) por (u,y) e (x,v)
        '''
        return self.movimentInterRoutes(solution, self._M.shiftUXVYwithUYXV, timeIni, timeMax)

    def M10(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Rotation 
        Bolaños 2018
        '''
        solution1 = copy.deepcopy(solution)
        depots = dpts.get_depotsList()
        bestRoute = None
        extraPenalty = 0

        # verifica todas as rotas
        for idRoute, route in enumerate(solution.get_routes()):
            length = len(route.get_tour())  # comprimento da rota
            oldDepot = route.get_depot()
            costWithoutRoute = solution.get_cost() - route.get_totalCost()
            penalty = route.get_totalCost() - route.get_costWithoutPenalty()
            extraPenalty = 0
            # print(penalty)
            cont = 0

            # print("tamanho de rotas")
            # print(len(routes))
            # print("route")
            # print(route)
            if length > 0:
                route1 = copy.deepcopy(route)
                # rotação da rota
                for i in range(length):
                    # rotacionar
                    # print(route1)
                    aux = route1.get_tour()[0]
                    # print(aux)
                    cost = route1.costWithoutNode(0)
                    route1.removeCustomer(aux)
                    route1.set_cost(cost[1], cost[2], cost[3])
                    cost = route1.costWithNode(aux, length-1)
                    route1.addCustomer(aux)
                    route1.set_cost(cost[1], cost[2], cost[3])
                    # print(route1)
                    # print("-----")
                    # verificar se rota gerada é melhor (considerando mesmo depósito)
                    if bestRoute == None or bestRoute.get_totalCost() > route1.get_totalCost():
                        extraPenalty = 0
                        bestRoute = copy.deepcopy(route1)
                        cont = 1
                    # verificar transferência da rota em outro depósito
                    for dpt in depots.values():
                        if str(dpt) != str(oldDepot):
                            # verificar rota para o novo depósito
                            tour = route1.get_tour()
                            # tirar o custo associado ao depósito
                            cost1 = route1.get_totalCost() - dist.euclidianDistance(tour[0].get_x_coord(),
                                                                                    tour[0].get_y_coord(), oldDepot.get_x_coord(), oldDepot.get_y_coord()) - \
                                dist.euclidianDistance(tour[length-1].get_x_coord(),
                                                       tour[length-1].get_y_coord(), oldDepot.get_x_coord(), oldDepot.get_y_coord())

                            # computar custo com o novo depósito
                            newCost = cost1 + dist.euclidianDistance(tour[0].get_x_coord(),
                                                                     tour[0].get_y_coord(), dpt.get_x_coord(), dpt.get_y_coord()) + \
                                dist.euclidianDistance(tour[length-1].get_x_coord(),
                                                       tour[length-1].get_y_coord(), dpt.get_x_coord(), dpt.get_y_coord())

                            if bestRoute.get_totalCost() > newCost:
                                # verifica número de veículos utilizados pelo depósito
                                if solution.get_nRoutesByDepot(str(dpt.get_id())) < dpt.get_numberVehicles():
                                    if (costWithoutRoute + newCost) < solution.get_cost():  # é melhor
                                        extraPenalty = 0
                                        bestRoute = copy.deepcopy(route1)
                                        bestRoute.set_depot(dpt)
                                        newCost1 = newCost - penalty
                                        bestRoute.set_cost(newCost1, bestRoute.get_totalDemand(),
                                                           bestRoute.get_totalService())
                                        cont = 1
                                # else:
                                #     if (costWithoutRoute + newCost + 1000) < solution1.get_cost(): # ainda é melhor
                                #         extraPenalty = 1000 #penalização por rota a mais
                                #         bestRoute.set_depot(dpt)
                                #         newCost1 = newCost - penalty
                                #         bestRoute.set_cost(newCost1, bestRoute.get_totalDemand(),
                                #             bestRoute.get_totalService())
                                #         cont = 1

            if timeMax < (time.time()-timeIni):
                break

        if cont == 1:
            # print(penalty)
            # # print(bestRoute.get_totalCost())
            # print(route)
            # # print("best")
            # print(bestRoute)
            solution1.setRoute(bestRoute, idRoute)
            solution1.formGiantTour()
            solution1.calculateCost(extraPenalty)
            return solution1

        return solution
