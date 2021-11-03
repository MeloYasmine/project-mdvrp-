from localSearchFirst import LocalSearch as lsf
from localSearchBest import LocalSearchBest as lsb
from movimentsLocalSearch import MovimentsLocalSearch as mov
import copy
import numpy as np
import config
import math
import time


class IteratedLocalSearch:

    def ils(self, solution, nGenerations, ls='random', timeIni=0, timeMax=math.inf, probLs=config.PROB_LS):
        '''
        Modified Iterated Local Search
        __ls: string 'lsf' se for first improvement, 'lsb' se for best improvement
        '''
        if np.random.random_sample() < probLs:
            # print("entrou q****")
            level = 2
            if ls == 'lsf':
                LS = lsf()
            elif ls == 'lsb':
                LS = lsb()
            else:
                LS = self
            solution = LS.LS(solution, timeIni=timeIni, timeMax=timeMax)
            bestSolution = copy.deepcopy(solution)
            # print(solution.get_routes())
            # print(solution.get_cost())
            for i in range(nGenerations):
                solution1 = self.pertubation(copy.deepcopy(solution), level)
                # print(solution1.get_routes())
                # print(solution1.get_cost())
                # print("___________________________________")
                solution1 = LS.LS(
                    solution1, timeIni=timeIni, timeMax=timeMax)

                delta = solution1.get_cost() - solution.get_cost()
                if delta < 0 or level > 10:
                    solution = copy.deepcopy(solution1)
                    level = 2
                    if solution1.get_cost() < bestSolution.get_cost():
                        bestSolution = copy.deepcopy(solution1)
                else:
                    level += 1
                    if np.random.random_sample() < math.exp(-delta/nGenerations):
                        solution = copy.deepcopy(solution1)

                # if solution1.get_cost() < solution.get_cost() or level > 10:
                #     solution = copy.deepcopy(solution1)
                #     level = 2
                # else:
                #     level += 1

                if timeMax < (time.time()-timeIni):
                    break

            return bestSolution

        return solution

    def pertubation(self, solution, level):
        M = mov()
        # movs = [M.shiftUXVYwithUVXY]
        movs = [M.swap, M.shiftUXwithVY, M.shiftUXVYwithUVXY, M.shiftUXVYwithUYXV,
                M.shiftUXwithV, M.removeUXinsertAfterV, M.removeUXinsertXUAfterV, M.removeUinsertAfterV]
        for i in range(level):
            routes = solution.get_routes()
            # print(solution.get_routes())
            # print(solution.get_cost())
            mv = int(np.random.randint(len(movs)))
            # mv = 7
            idRoutes = np.random.choice(
                len(routes), 2, replace=True)
            # idRoutes = [1, 1]
            lengthU = len(routes[idRoutes[0]].get_tour())
            lengthV = len(routes[idRoutes[1]].get_tour())
            if lengthU > 0 and lengthV > 0:
                idU = np.random.randint(lengthU)
                # idU = 0
                # idV = 5
                idV = np.random.randint(lengthV)
                # print("idRouteU: {}  idRouteV: {}  idU: {}  idV: {}".format(
                #     idRoutes[0], idRoutes[1], idU, idV))
                solution = movs[mv](solution, idRoutes[0],
                                    idRoutes[1], idU, idV)[0]
                # print(solution.get_routes())
                # print(solution.get_cost())
        return solution

    def LS(self, solution, itMax=config.IT_ILSA, timeIni=0, timeMax=math.inf):
        M = mov()
        # movs = [M.shiftUXVYwithUVXY]
        movs = [M.swap, M.shiftUXwithVY, M.shiftUXVYwithUVXY, M.shiftUXVYwithUYXV,
                M.shiftUXwithV, M.removeUXinsertAfterV, M.removeUXinsertXUAfterV, M.removeUinsertAfterV]

        it = 0
        timeC = 0
        cont = 0
        while it < itMax and cont < 5 and timeC < timeMax:
            routes = solution.get_routes()
            it += 1
            mv = int(np.random.randint(len(movs)))
            idRoutes = np.random.choice(
                len(routes), 2, replace=True)
            lengthU = len(routes[idRoutes[0]].get_tour())
            lengthV = len(routes[idRoutes[1]].get_tour())
            if lengthU > 0 and lengthV > 0:
                idU = np.random.randint(lengthU)
                # idU = 0
                # idV = 5
                idV = np.random.randint(lengthV)
                # print("idRouteU: {}  idRouteV: {}  idU: {}  idV: {}".format(
                #     idRoutes[0], idRoutes[1], idU, idV))
                solution1 = movs[mv](copy.deepcopy(solution), idRoutes[0],
                                     idRoutes[1], idU, idV)[0]

                if solution1.get_cost() < solution.get_cost():
                    solution = copy.deepcopy(solution1)
                    it = 0
                    cont = 0
                else:
                    cont += 1

            timeC = time.time() - timeIni
        solution.removeRoutesEmpty()

        return solution
