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


class LocalSearch:

    def __init__(self):
        self._M = mov()

    def LS(self, solution, prob=config.PROB_LS_BEST, nMovimentations='all', where=None, timeIni=0, timeMax=math.inf):
        '''
        Cada iteração varre todos os pares possíveis de nós distintos (u,v). Esses nós podem pertencer à mesma viagem ou a viagens diferentes
        e um deles pode ser o depósito. x e y são os sucessores de u e v em suas respectivas viagens.
        @param Where opcional, para indicar onde o método é chamado, opções: None default ou 'ls'
        @param nMovimentations, para indicar se serão utilizados todos os movimentos ou apenas alguns. Opções: 'all' default ou 'random'
        '''

        movimentation = [self.M2, self.M4,self.M5, self.M6, self.M7, self.M8, self.M9, self.M10]
        # print("timeIni: {}".format(timeIni))

        # movimentation = [self.M1a, self.M1b, self.M2a, self.M2b, self.M3a, self.M3b, self.M4a,
        #                  self.M4b, self.M5a, self.M5b, self.M6a, self.M6b, self.M7, self.M8, self.M9, self.M10]
        lenght = len(movimentation)
        prob = 0  # config.PROB_LS
        # pMov = [0.1, 0.1, 0.05, 0.05, 0.05, 0.02, 0.05, 0.2, 0.3, 0.08]
        # embaralhar os movimentos
        if nMovimentations == 'random':
            n = max(2, round(0.8*lenght))
            p = np.random.randint(1, n+1)
            movimentation = np.random.choice(
                movimentation, p, replace=False)
        else:
            # p = np.random.randint(1,lenght)
            # prob = config.PROB_LS_BEST
            movimentation = np.random.choice(
                movimentation, lenght, replace=False)

        bestSolution = None
        bestSolution = copy.deepcopy(solution)
        cont = 0

        if (where == 'ls' and np.random.random_sample() < prob) or where == None:
            # print("vai mudar")
            # print(movimentation)
            # print(bestSolution)
            # print(bestSolution.get_routes())
            for i, m in enumerate(movimentation):
                # print(m)
                # print(solution)
                # print(solution.get_routes())
                # print("vai passar .................")
                solution1 = None
                solution1 = m(copy.deepcopy(bestSolution), timeIni, timeMax)
                # tour = solution1.get_giantTour()
                # for i, c1 in enumerate(tour):
                #     for j, c2 in enumerate(tour):
                #         if i != j and c1 == c2:
                #             print("Elementos iguais na LS first")
                #             exit(1)
                # print(m)
                # print(solution1)
                # print(solution1.get_routes())
                # for r in solution1.get_routes():
                #     demand = 0
                #     for c in r.get_tour():
                #         demand += c.get_demand()
                #     if demand != r.get_totalDemand():
                #         print("demandas diferentes")
                #         print(r)
                #         print(c)
                #         print("demand: "+ str(demand))
                #         print("totalDemand: "+str(r.get_totalDemand()))
                #         exit(1)

                if solution1.get_cost() < bestSolution.get_cost():
                    cont = 0
                    bestSolution = copy.deepcopy(solution1)
                else:
                    cont += 1
                    # print(
                    #     "achou melhor first {}  -  {}***************************************************\n\n".format(i, m))
                if cont > 10:
                    # print(
                    #     "não  achou melhor first  {}  - {}***************************************************\n\n".format(i, m))
                    # excluir rotas vazias
                    bestSolution.removeRoutesEmpty()
                    # print("bestSolution")
                    # print(bestSolution)
                    return bestSolution

                if timeMax < (time.time()-timeIni):
                    # print("entrou aqui????")
                    break

            # excluir rotas vazias
            bestSolution.removeRoutesEmpty()
            # print("não achou melhor")
        return bestSolution

    def movimentRoutes(self, solution, moviment, timeIni=0, timeMax=math.inf):
        cost = solution.get_cost()
        for idRouteU, routeU in enumerate(solution.get_routes()):
            lenghtRouteU = len(routeU.get_tour())
            for idU in range(lenghtRouteU):
                for idRouteV, routeV in enumerate(solution.get_routes()):
                    lenghtRouteV = len(routeV.get_tour())
                    for idV in range(lenghtRouteV):
                        # print("Inicio")
                        # print("cost: {}".format(cost))
                        # print("timeIni: {}".format(timeIni))
                        # print(solution.get_routes())
                        # print("len Route U: {}".format(lenghtRouteU))
                        # print("len Route V: {}".format(lenghtRouteV))
                        # print("idRouteU: {}, idRouteV:{}  idU: {}  idV: {}".format(
                        #     idRouteU, idRouteV, idU, idV))
                        # print("routeU")
                        # print(routeU)
                        # print("routeV")
                        # print(routeV)
                        # print("routeU.get_tour()")
                        # print(routeU.get_tour())
                        # print("routeV.get_tour()")
                        # print(routeV.get_tour())
                        solution1 = moviment(solution, idRouteU, idRouteV,
                                             idU, idV, cost=cost)[0]
                        # print("cost1: {}".format(solution1.get_cost()))

                        if solution1.get_cost() < cost:
                            # print("cost: {}".format(cost))
                            # print("cost1: {}".format(solution1.get_cost()))
                            return solution1
                        if timeMax < (time.time()-timeIni):
                            # print("entrou aqui")
                            # print("timeIni: {}  timeNow: {}  timeDif: {}".format(
                            #     timeIni, time.time(), time.time()-timeIni))
                            break
                    if timeMax < (time.time()-timeIni):
                        # print("entrou aqui")
                        # print("timeIni: {}  timeNow: {}  timeDif: {}".format(
                        #     timeIni, time.time(), time.time()-timeIni))
                        break
                if timeMax < (time.time()-timeIni):
                    # print("entrou aqui")
                    # print("timeIni: {}  timeNow: {}  timeDif: {}".format(
                    #     timeIni, time.time(), time.time()-timeIni))
                    break
            if timeMax < (time.time()-timeIni):
                # print("entrou aqui")
                # print("timeIni: {}  timeNow: {}  timeDif: {}".format(
                #     timeIni, time.time(), time.time()-timeIni))
                break

        return solution

    def movimentIntraRoutes(self, solution, moviment, timeIni=0, timeMax=math.inf):
        cost = solution.get_cost()
        for idRouteU, routeU in enumerate(solution.get_routes()):
            lenghtRouteU = len(routeU.get_tour())
            for idU in range(lenghtRouteU-1):
                for idV in range(lenghtRouteU-1):
                    if idU != idV:
                        solution1 = moviment(solution, idRouteU, idRouteU,
                                             idU, idV, cost=cost)[0]
                        if solution1.get_cost() < cost:
                            # print("cost: {}".format(cost))
                            # print("cost1: {}".format(solution1.get_cost()))
                            return solution1
                    if timeMax < (time.time()-timeIni):
                        break
                if timeMax < (time.time()-timeIni):
                    break
            if timeMax < (time.time()-timeIni):
                break

        return solution

    def movimentInterRoutes(self, solution, moviment, timeIni=0, timeMax=math.inf):
        cost = solution.get_cost()
        for idRouteU, routeU in enumerate(solution.get_routes()):
            lenghtRouteU = len(routeU.get_tour())
            for idU in range(lenghtRouteU):
                for idRouteV, routeV in enumerate(solution.get_routes()):
                    lenghtRouteV = len(routeV.get_tour())
                    for idV in range(lenghtRouteV):
                        if idRouteU != idRouteV and idU != idV:
                            solution1 = moviment(solution, idRouteU, idRouteV,
                                                 idU, idV, cost=cost)[0]
                            if solution1.get_cost() < cost:
                                # print("cost: {}".format(cost))
                                # print("cost1: {}".format(solution1.get_cost()))
                                return solution1
                        if timeMax < (time.time()-timeIni):
                            break
                    if timeMax < (time.time()-timeIni):
                        break
                if timeMax < (time.time()-timeIni):
                    break
            if timeMax < (time.time()-timeIni):
                break

        return solution

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
        cost = solution.get_cost()
        for idRouteU, routeU in enumerate(solution.get_routes()):
            lenghtU = len(routeU.get_tour())
            for idU in range(lenghtU-1):
                for idRouteV, routeV in enumerate(solution.get_routes()):
                    for idV in range(len(routeV.get_tour())):
                        # se u e x são diferentes de v
                        if idU != idV and idU+1 != idV:
                            solution1 = self._M.removeUXinsertAfterV(solution, idRouteU, idRouteV,
                                                                     idU, idV, cost=cost)[0]
                            if solution1.get_cost() < cost:
                                # print("cost: {}".format(cost))
                                # print("cost1: {}".format(solution1.get_cost()))
                                return solution1
                        if timeMax < (time.time()-timeIni):
                            break
                    if timeMax < (time.time()-timeIni):
                        break
                if timeMax < (time.time()-timeIni):
                    break
            if timeMax < (time.time()-timeIni):
                break

        return solution

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
        cost = solution.get_cost()
        for idRouteU, routeU in enumerate(solution.get_routes()):
            lenghtU = len(routeU.get_tour())
            for idU in range(lenghtU-1):
                for idRouteV, routeV in enumerate(solution.get_routes()):
                    for idV in range(len(routeV.get_tour())):
                        # se u e x são diferentes de v
                        if idU != idV and idU+1 != idV:
                            solution1 = self._M.removeUXinsertXUAfterV(solution, idRouteU, idRouteV,
                                                                       idU, idV, cost=cost)[0]
                            if solution1.get_cost() < cost:
                                # print("cost: {}".format(cost))
                                # print("cost1: {}".format(solution1.get_cost()))
                                return solution1

                        if timeMax < (time.time()-timeIni):
                            break
                    if timeMax < (time.time()-timeIni):
                        break
                if timeMax < (time.time()-timeIni):
                    break
            if timeMax < (time.time()-timeIni):
                break

        return solution

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
        cost = solution.get_cost()
        size = len(solution.get_routes())
        for idRouteU in range(size-1):
            routeU = solution.get_routes()[idRouteU]
            for idU in range(len(routeU.get_tour())):
                for idRouteV in range(idRouteU, size):
                    routeV = solution.get_routes()[idRouteV]
                    for idV in range(len(routeV.get_tour())):
                        if idU != idV:
                            solution1 = self._M.swap(solution, idRouteU, idRouteV,
                                                     idU, idV, cost=cost)[0]
                            if solution1.get_cost() < cost:
                                # print("cost: {}".format(cost))
                                # print("cost1: {}".format(solution1.get_cost()))
                                return solution1
                        if timeMax < (time.time()-timeIni):
                            break
                    if timeMax < (time.time()-timeIni):
                        break
                if timeMax < (time.time()-timeIni):
                    break
            if timeMax < (time.time()-timeIni):
                break

        return solution

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
        cost = solution.get_cost()
        for idRouteU, routeU in enumerate(solution.get_routes()):
            lenghtRouteU = len(routeU.get_tour())
            for idU in range(lenghtRouteU-1):
                for idRouteV, routeV in enumerate(solution.get_routes()):
                    lenghtRouteV = len(routeV.get_tour())
                    for idV in range(lenghtRouteV):
                        solution1 = self._M.shiftUXwithV(solution, idRouteU, idRouteV,
                                                         idU, idV, cost=cost)[0]
                        if solution1.get_cost() < cost:
                            # print("cost: {}".format(cost))
                            # print("cost1: {}".format(solution1.get_cost()))
                            return solution1

                        if timeMax < (time.time()-timeIni):
                            break
                    if timeMax < (time.time()-timeIni):
                        break
                if timeMax < (time.time()-timeIni):
                    break
            if timeMax < (time.time()-timeIni):
                break

        return solution

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
        cost = solution.get_cost()
        for idRouteU, routeU in enumerate(solution.get_routes()):
            lenghtRouteU = len(routeU.get_tour())
            for idU in range(lenghtRouteU-1):
                for idRouteV, routeV in enumerate(solution.get_routes()):
                    lenghtRouteV = len(routeV.get_tour())
                    for idV in range(lenghtRouteV-1):
                        solution1 = self._M.shiftUXwithVY(solution, idRouteU, idRouteV,
                                                          idU, idV, cost=cost)[0]
                        if solution1.get_cost() < cost:
                            # print("cost: {}".format(cost))
                            # print("cost1: {}".format(solution1.get_cost()))
                            return solution1

                        if timeMax < (time.time()-timeIni):
                            break
                    if timeMax < (time.time()-timeIni):
                        break
                if timeMax < (time.time()-timeIni):
                    break
            if timeMax < (time.time()-timeIni):
                break

        return solution

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
        cost = solution.get_cost()
        for idRouteU, routeU in enumerate(solution.get_routes()):
            lenghtRouteU = len(routeU.get_tour())
            for idU in range(lenghtRouteU-1):
                for idRouteV, routeV in enumerate(solution.get_routes()):
                    lenghtRouteV = len(routeV.get_tour())
                    for idV in range(lenghtRouteV-1):
                        if idRouteU != idRouteV and idU != idV:
                            solution1 = self._M.shiftUXVYwithUVXY(solution, idRouteU, idRouteV,
                                                                  idU, idV, cost=cost)[0]
                            if solution1.get_cost() < cost:
                                # print("cost: {}".format(cost))
                                # print("cost1: {}".format(solution1.get_cost()))
                                return solution1
                        if timeMax < (time.time()-timeIni):
                            break
                    if timeMax < (time.time()-timeIni):
                        break
                if timeMax < (time.time()-timeIni):
                    break
            if timeMax < (time.time()-timeIni):
                break

        return solution

    def M9(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Método aplica a regra: Se T(u) != T(v), substitua (u,x) e (v,y) por (u,y) e (x,v)
        '''
        cost = solution.get_cost()
        for idRouteU, routeU in enumerate(solution.get_routes()):
            lenghtRouteU = len(routeU.get_tour())
            for idU in range(lenghtRouteU-1):
                for idRouteV, routeV in enumerate(solution.get_routes()):
                    lenghtRouteV = len(routeV.get_tour())
                    for idV in range(lenghtRouteV-1):
                        if idRouteU != idRouteV and idU != idV:
                            solution1 = self._M.shiftUXVYwithUYXV(solution, idRouteU, idRouteV,
                                                                  idU, idV, cost=cost)[0]
                            if solution1.get_cost() < cost:
                                # print("cost: {}".format(cost))
                                # print("cost1: {}".format(solution1.get_cost()))
                                return solution1
                        if timeMax < (time.time()-timeIni):
                            break
                    if timeMax < (time.time()-timeIni):
                        break
                if timeMax < (time.time()-timeIni):
                    break
            if timeMax < (time.time()-timeIni):
                break

        return solution

    def M10(self, solution, timeIni=0, timeMax=math.inf):
        '''
        Rotation
        Bolaños 2018
        '''
        solution1 = copy.deepcopy(solution)
        depots = dpts.get_depotsList()
        # escolha da rota
        routes = solution1.get_routes()
        idRoute = np.random.randint(len(routes))
        route = copy.deepcopy(routes[idRoute])
        length = len(route.get_tour())  # comprimento da rota
        oldDepot = route.get_depot()
        costWithoutRoute = solution1.get_cost() - route.get_totalCost()
        penalty = route.get_totalCost() - route.get_costWithoutPenalty()
        extraPenalty = 0
        # print(penalty)
        cont = 0

        bestRoute = copy.deepcopy(route)
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
                if bestRoute.get_totalCost() > route1.get_totalCost():
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
                            if solution1.get_nRoutesByDepot(str(dpt.get_id())) < dpt.get_numberVehicles():
                                if (costWithoutRoute + newCost) < solution1.get_cost():  # é melhor
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
