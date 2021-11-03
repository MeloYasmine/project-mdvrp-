
from depots import Depots as dpts
from customers import Customers as csts
from distances import Distances as dist
from route import Route
from solution import Solution
import math
import copy


class SplitAlgorithms:
    _infinite = math.inf

    '''
    algoritmo adaptado de https://w1.cirrelt.ca/~vidalt/en/VRP-resources.html
    Linear Split algorithm
    '''

    def splitLinear(self, solution, limitRoutes=True):
        solution1 = copy.deepcopy(solution)
        depotsList = dpts.get_depotsList()
        customers = solution1.get_giantTour()
        depots = solution1.get_depots()
        penalty = 0.0
        for dpt in depotsList:
            verifyDpt = False
            listCst = []
            depot = depotsList[dpt]
            for j in range(len(customers)):
                if str(dpt) == str(depots[j].get_id()):
                    listCst.append(customers[j])
                    verifyDpt = True

            if verifyDpt:
                lenListCst = len(listCst)
                sumDistance = []
                sumLoad = []
                potential = []
                pred = []

                for x in range(lenListCst+1):
                    sumDistance.append(0.0)
                    sumLoad.append(0.0)
                    potential.append(1.e30)
                    pred.append(-1)

                sumDistance[0] = 0  # distancia do depósito
                # distância do depósito ao primeiro nó
                sumDistance[1] = dist.euclidianDistance(listCst[0].get_x_coord(
                ), listCst[0].get_y_coord(), depot.get_x_coord(), depot.get_y_coord()) + listCst[0].get_service()

                sumLoad[0] = 0
                sumLoad[1] = customers[0].get_demand()
                potential[0] = 0

                # inicializar com o somatório distancia de i-1 a i e a demanda de i-1 a i
                for i in range(2, lenListCst+1):
                    sumDistance[i] = sumDistance[i-1] + dist.euclidianDistance(listCst[i-2].get_x_coord(
                    ), listCst[i-2].get_y_coord(), listCst[i-1].get_x_coord(), listCst[i-1].get_y_coord()) + listCst[i-1].get_service()
                    sumLoad[i] = sumLoad[i-1] + listCst[i-1].get_demand()

                queue = [0]

                for i in range(1, lenListCst+1):
                    # da frente é o melhor predecessor de 1
                    potential[i] = self.propagate(
                        queue[0], i, listCst, sumDistance, potential, depot)
                    pred[i] = queue[0]

                    if i < lenListCst:
                        # se i não é dominado pelo último da pilha
                        if not self.dominates(queue[len(queue)-1], i, listCst, sumDistance, potential, sumLoad, depot):
                            # então i será inserido, precisando remover quem ele domina
                            while len(queue) > 0 and self.dominatesRight(queue[len(queue)-1], i, listCst, sumDistance, potential, depot):
                                del queue[len(queue)-1]
                            queue.append(i)
                        # Verifica se a frente consegue chegar ao próximo nó, caso contrário ele desaparecerá.
                        while len(queue) > 0 and (sumLoad[i+1] - sumLoad[queue[0]]) > (depot.get_loadVehicle() + 0.0001) and (sumDistance[i+1] - sumDistance[queue[0]]) > (2*depot.get_durationRoute() + 0.0001):
                            del queue[0]

                if potential[len(listCst)] > 1.e29:
                    print(
                        "ERRO: nenhuma solução de divisão foi propagada até o último nó")
                    exit(1)
                else:
                    # achando o número ótimo de rotas
                    nRoutes = 0
                    cour = lenListCst
                    while cour > 0:
                        cour = pred[cour]
                        nRoutes += 1

                    cour = len(listCst)
                    # print(listCst)
                    # print(pred)
                    # print(cour)
                    trip = []
                    for i in range(nRoutes-1, -1, -1):
                        t = []

                        j = pred[cour]
                        load = 0
                        for k in range(j+1, cour+1):
                            t.append(listCst[k-1])
                            load += listCst[k-1].get_demand()
                        cour = j
                        trip.append([t, load])

                    # se o número de rotas formadas for maior que o número de veículos, juntar as de menor demanda caso limitRoutes = True, senão aplica penalidade
                    numberVehicles = depot.get_numberVehicles()
                    if nRoutes > numberVehicles:
                        # ordenada em ordem crescente de demanda
                        trip = sorted(trip, key=lambda x: x[1])
                        # juntar rotas com menor demanda
                        aux = len(trip) - numberVehicles
                        aux1 = aux

                        if limitRoutes:
                            while aux > 0:
                                r0 = trip[0][0]
                                r1 = trip[1][0]
                                r0 = r0 + r1
                                demand = trip[0][1] + trip[1][1]
                                trip[0] = [r0, demand]
                                del trip[1]
                                # ordenada em ordem crescente de demanda
                                trip = sorted(trip, key=lambda x: x[1])
                                aux -= 1
                        else:
                            penalty += 1000 * aux1

                    # adicionar rotas a solucao
                    for r in trip:
                        route = Route(depot)
                        # print("r")
                        # print(r)
                        for c in r[0]:
                            # print("c")
                            # print(c)
                            route.addCustomer(c)
                        # calcular custo da rota formada
                        route.startValues()
                        route.calculeCost()
                        solution1.addRoutes(route)

        solution1.formGiantTour()
        solution1.calculateCost(penalty)
        # print(solution1.get_routes())
        # exit(1)
        return solution1

    '''
    algoritmo adaptado de https://w1.cirrelt.ca/~vidalt/en/VRP-resources.html
    Linear Split algorithm with a fleet-size limit m
    '''

    def splitLinearBounded(self, solution):
        solution1 = copy.deepcopy(solution)
        solution2 = copy.deepcopy(solution)
        depotsList = dpts.get_depotsList()
        customers = solution1.get_giantTour()
        depots = solution1.get_depots()
        for dpt in depotsList:
            listCst = []
            depot = depotsList[dpt]
            for j in range(len(customers)):
                if dpt == str(depots[j].get_id()):
                    listCst.append(customers[j])

            sumDistance = [0.0 for x in range(len(listCst)+1)]
            sumLoad = [0.0 for x in range(len(listCst)+1)]
            sumDistance[0] = 0  # distancia do depósito
            # distância do depósito ao primeiro nó
            sumDistance[1] = dist.euclidianDistance(listCst[0].get_x_coord(
            ), listCst[0].get_y_coord(), depot.get_x_coord(), depot.get_y_coord())

            sumLoad[0] = 0
            sumLoad[1] = customers[0].get_demand()
            # inicializar com o somatório distancia de i-1 a i e a demanda de i-1 a i
            for i in range(2, len(listCst)+1):
                sumDistance[i] = sumDistance[i-1] + dist.euclidianDistance(listCst[i-2].get_x_coord(
                ), listCst[i-2].get_y_coord(), listCst[i-1].get_x_coord(), listCst[i-1].get_y_coord())
                sumLoad[i] = sumLoad[i-1] + listCst[i-1].get_demand()

            potential = []
            pred = []

            for k in range(depot.get_numberVehicles()+1):
                potential.append([1.e30 for x in range(len(listCst) + 1)])
                pred.append([-1 for x in range(len(listCst) + 1)])

            potential[0][0] = 0

            for k in range(depot.get_numberVehicles()):
                queue = [k]
                i = k+1
                while (i <= len(listCst)) and (len(queue) > 0):
                    # o primeiro da fila será o melhor predecessor de i
                    potential[k+1][i] = self.propagatek(
                        queue[0], i, k, listCst, sumDistance, potential, depot)  # calcula custo de i a j
                    pred[k+1][i] = queue[0]

                    # se i não é dominado pelo último da pilha
                    if i < len(listCst):
                        if not(self.dominatesk(queue[len(queue)-1], i, k, listCst, sumDistance, potential, sumLoad, depot)):
                            # então i será inserido, precisando remover quem ele domina
                            while len(queue) > 0 and self.dominatesRightk(queue[len(queue)-1], i, k, listCst, sumDistance, potential, depot):
                                del queue[len(queue)-1]
                            queue.append(i)

                        # Verifica se a frente consegue chegar ao próximo nó, caso contrário ele desaparecerá.
                        while len(queue) > 0 and (sumLoad[i+1] - sumLoad[queue[0]]) > (depot.get_loadVehicle() + 0.0001) and (sumDistance[i+1] - sumDistance[queue[0]]) > (2*depot.get_durationRoute() + 0.0001):
                            del queue[0]

                    i += 1

            if potential[depot.get_numberVehicles()][len(listCst)] > 1.e29:
                # print("ERRO: nenhuma solução de divisão foi propagada até o último nó")
                del solution1
                return self.mountRoutes(solution2)

            else:
               # achando o número ótimo de rotas
                minCost = 1.e30
                nRoutes = 0
                for k in range(1, depot.get_numberVehicles()+1):
                    if potential[k][len(listCst)] < minCost:
                        minCost = potential[k][len(listCst)]
                        # print("minCost "+str(minCost))
                        nRoutes = k

                cour = len(listCst)
                for i in range(nRoutes-1, -1, -1):
                    route = Route(depot)
                    j = pred[i+1][cour]
                    for k in range(j+1, cour+1):
                        route.addCustomer(listCst[k-1])
                    cour = j
                    # calcular custo da rota formada
                    route.startValues()
                    route.calculeCost()
                    solution1.addRoutes(route)

        solution1.formGiantTour()
        solution1.calculateCost()
        # print(solution)
        return solution1

    '''
    Método calcula o custo de propagação de i até j
    '''

    def propagate(self, i, j, listCst, sumDistance, potential, depot):
        distDeptNextI = dist.euclidianDistance(listCst[i].get_x_coord(), listCst[i].get_y_coord(
        ), depot.get_x_coord(), depot.get_y_coord()) + listCst[i].get_service()  # distancia de i+1 até o depósito

        distDeptJ = dist.euclidianDistance(listCst[j-1].get_x_coord(), listCst[j-1].get_y_coord(
        ), depot.get_x_coord(), depot.get_y_coord()) + listCst[j-1].get_service()  # distancia de j até o depósito

        return potential[i] + sumDistance[j] - sumDistance[i+1] + distDeptNextI + distDeptJ

    '''
    Método calcula o custo de propagação de i até j
    '''

    def propagatek(self, i, j, k, listCst, sumDistance, potential, depot):
        distDeptNextI = dist.euclidianDistance(listCst[i].get_x_coord(), listCst[i].get_y_coord(
        ), depot.get_x_coord(), depot.get_y_coord())  # distancia de i+1 até o depósito
        distDeptJ = dist.euclidianDistance(listCst[j-1].get_x_coord(), listCst[j-1].get_y_coord(
        ), depot.get_x_coord(), depot.get_y_coord())  # distancia de j até o depósito

        return potential[k][i] + sumDistance[j] - sumDistance[i+1] + distDeptNextI + distDeptJ

    '''
    Método testa se i domina j como predecessor para todos os nós x> = j + 1
    '''

    def dominates(self, i, j, listCst, sumDistance, potential, sumLoad, depot):
        distDeptNextJ = dist.euclidianDistance(listCst[j].get_x_coord(
        ), listCst[j].get_y_coord(), depot.get_x_coord(), depot.get_y_coord()) + listCst[j].get_service()
        distDeptNextI = dist.euclidianDistance(listCst[i].get_x_coord(
        ), listCst[i].get_y_coord(), depot.get_x_coord(), depot.get_y_coord()) + listCst[i].get_service()

        return sumLoad[i] == sumLoad[j] and (potential[j] + distDeptNextJ) > (potential[i] + distDeptNextI + sumDistance[j+1] - sumDistance[i+1] - 0.0001)

    '''
    Método testa se i domina j como predecessor para todos os nós x> = j + 1
    '''

    def dominatesk(self, i, j, k, listCst, sumDistance, potential, sumLoad, depot):
        distDeptNextJ = dist.euclidianDistance(listCst[j].get_x_coord(
        ), listCst[j].get_y_coord(), depot.get_x_coord(), depot.get_y_coord())
        distDeptNextI = dist.euclidianDistance(listCst[i].get_x_coord(
        ), listCst[i].get_y_coord(), depot.get_x_coord(), depot.get_y_coord())

        return sumLoad[i] == sumLoad[j] and (potential[k][j] + distDeptNextJ) > (potential[k][i] + distDeptNextI + sumDistance[j+1] - sumDistance[i+1] - 0.0001)

    '''
    Método testa se j domina i como predecessor para todos os nós x> = j + 1
    '''

    def dominatesRight(self, i, j, listCst, sumDistance, potential, depot):
        distDeptNextJ = dist.euclidianDistance(listCst[j].get_x_coord(
        ), listCst[j].get_y_coord(), depot.get_x_coord(), depot.get_y_coord()) + listCst[j].get_service()
        distDeptNextI = dist.euclidianDistance(listCst[i].get_x_coord(
        ), listCst[i].get_y_coord(), depot.get_x_coord(), depot.get_y_coord()) + listCst[i].get_service()

        return (potential[j] + distDeptNextJ) < (potential[i] + distDeptNextI + sumDistance[j+1] - sumDistance[i+1] + 0.0001)

    '''
    Método testa se j domina i como predecessor para todos os nós x> = j + 1
    '''

    def dominatesRightk(self, i, j, k, listCst, sumDistance, potential, depot):
        distDeptNextJ = dist.euclidianDistance(listCst[j].get_x_coord(
        ), listCst[j].get_y_coord(), depot.get_x_coord(), depot.get_y_coord())
        distDeptNextI = dist.euclidianDistance(listCst[i].get_x_coord(
        ), listCst[i].get_y_coord(), depot.get_x_coord(), depot.get_y_coord())

        return (potential[k][j] + distDeptNextJ) < (potential[k][i] + distDeptNextI + sumDistance[j+1] - sumDistance[i+1] + 0.0001)

    '''
    Método monta as rotas de cada depósito usando algoritmo proposto por Prins2004
    '''

    def mountRoutes(self, solution):
        solution1 = copy.deepcopy(solution)
        allDepots = dpts.get_depotsList()
        customers = solution1.get_giantTour()
        depots = solution1.get_depots()
        numberVehicles = depots[0].get_numberVehicles()
        # print("customers: "+str(customers))
        # print("deposts: "+str(depots))

        # depósitos já vem separados, utilizar heurística de Prins2004 para separar as rotas

        # separar conjuntos
        for i in allDepots:
            depot = allDepots[i]
            path = []
            for j in range(len(customers)):
                if str(depot.get_id()) == str(depots[j].get_id()):
                    path.append(customers[j])
            # print(len(allDepots))
            # print(len(customers))
            # print(len(path))
            # print(path)
            # print("nVeiculos"+str(depot.get_numberVehicles()))
            # print("path: "+str(path))
            # gerar rotas para cada caminho
            # método retorna lista de predecessores
            pred = self.splitRoute(path, depot)
            # print(pred)
            # método retorna lista de lista com rotas para um depósito (número máximo de veículos não delimitado)
            allroutes = self.extractVRP(pred, path)
            # verificar número de rotas formadas

            routes = []
            for l in allroutes:
                if len(l) > 0:  # há rota
                    routes.append(l)
            # print("routes: "+ str(routes))
            # caso tenha mais rotas que veículos
            if len(routes) > numberVehicles:
                # ordenada em ordem crescente de demanda
                routes = sorted(routes, key=lambda x: x[1])
                # juntar rotas com menor demanda
                aux = len(routes) - numberVehicles
                while aux > 0:
                    r0 = routes[0][0]
                    r1 = routes[1][0]
                    r0 = r0 + r1
                    demand = routes[0][1] + routes[1][1]
                    routes[0] = [r0, demand]
                    del routes[1]
                    # ordenada em ordem crescente de demanda
                    routes = sorted(routes, key=lambda x: x[1])
                    aux -= 1

            k = -1
            for l in routes:
                route = Route(depot)
                if len(l) > 0:
                    for m in l[0]:
                        route.addCustomer(m)
                        k += 1

                    # calcular custo da rota formada
                    route.startValues()
                    route.calculeCost()
                    solution1.addRoutes(route)
        solution1.formGiantTour()
        solution1.calculateCost()
        # print(solution1)
        return solution1

    '''
    Método implementa split definido em Prins2004
    recebe como parâmetro caminho de um depósito
    '''

    def splitRoute(self, path, depot):
        n = len(path)
        # print("path")
        # print(path)
        # print(depot)
        vehicleCapacity = depot.get_loadVehicle()  # máximo carregamento
        durationRoute = depot.get_durationRoute()  # máxima duração
        v = []  # custo do menor caminho do depósito até o ponto.
        predecessor = []  # predecessores de cada idCsts neste caminho
        predecessor.append(-1)  # depósito não tem precedente
        v.append(0.0)
        # print("n = {}".format(len(path)))

        for i in range(n):
            v.append(SplitAlgorithms._infinite)
            # pior hipótese - número de rotas = número clientes
            predecessor.append(0)

        for i in range(1, n+1):
            load = 0.0
            cost = 0.0
            j = i
            while (j <= n) and (load < vehicleCapacity) and (cost < 2*durationRoute):
                customer = path[j-1]
                load += customer.get_demand()
                if i == j:
                    # custo de ida e volta
                    cost = 2 * dist.euclidianDistance(customer.get_x_coord(), customer.get_y_coord(
                    ), depot.get_x_coord(), depot.get_y_coord()) + customer.get_service()
                else:
                    previewCustomer = path[j-2]
                    cost = cost - dist.euclidianDistance(previewCustomer.get_x_coord(), previewCustomer.get_y_coord(), depot.get_x_coord(), depot.get_y_coord()) + dist.euclidianDistance(previewCustomer.get_x_coord(
                    ), previewCustomer.get_y_coord(), customer.get_x_coord(), customer.get_y_coord()) + customer.get_service() + dist.euclidianDistance(customer.get_x_coord(), customer.get_y_coord(), depot.get_x_coord(), depot.get_y_coord())

                if (load <= vehicleCapacity) and (cost <= 2*durationRoute):
                    if (v[i-1] + cost) < v[j]:
                        v[j] = v[i-1] + cost
                        predecessor[j] = i-1
                j += 1
                # print("cost: {} load: {}".format(cost, load))
                # print("pred: {}".format(predecessor))
                # print("v: {}".format(v))

        # print("\n")
        # print(predecessor)
        return predecessor

    '''
    Método para extrair a solução VRP do vetor P
    definido em Prins2004
    retorna uma lista de trips onde cada índice contém uma lista de visitação e a demanda total destes clientes
    '''

    def extractVRP(self, listPredecessors, listCustomers):
        # print(listPredecessors)
        trip = []
        totalDemand = []
        n = len(listPredecessors) - 1
        for i in range(n+1):
            trip.append([])
            totalDemand.append(0)
        t = 0
        j = n
        i = n
        while i > 0:
            t += 1
            i = listPredecessors[j]
            sumDemand = 0
            trp = []
            for k in range(i+1, j+1):
                # print(listCustomers)
                trp.append(listCustomers[k-1])

                sumDemand += listCustomers[k-1].get_demand()

            trip[t] = [trp, sumDemand]
            j = i

        return trip
