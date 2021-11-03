from depots import Depots as dpts
from customers import Customers as csts
from splitDepots import SplitDepots
from splitAlgorithms import SplitAlgorithms as splitAlg
from solution import Solution
from auxiliary_heuristics import NearestNeighbor
from mutation import Mutation as mt
from localSearchFirst import LocalSearch as ls
from localSearchBest import LocalSearchBest as lsb
from iteratedLocalSearch import IteratedLocalSearch as ils
# from localSearchBest import LocalSearchBest as ls
import config
import numpy as np
import time


class Population:

    def __init__(self):
        self._population = []  # lista de Solution ordenada em ordem crescente de custo
        self._selProbabilities = []  # lista de probabilidade de seleção de cada indivíduo

    '''
    Método define população inicial
    '''

    def definePopulation(self, size):
        timeI = time.time()
        LS = ls()
        split = splitAlg()
        # Heurística do vizinho mais próximo
        customers = list(csts.get_customersList().values())
        cst0 = customers[np.random.randint(len(customers)-1)]
        # cst0 = customers[0]
        tour = NearestNeighbor.nearestNeighbor(cst0)
        cluster = SplitDepots.splitByDepot(tour)
        # criação de rotas por depósitos, individual é um Solution
        individual = split.splitLinear(cluster, True)
        # individual = split.mountRoutes(cluster)
        # print(individual)
        # print(individual.get_routes())
        # rand = np.random.random_sample()
        # if rand < config.PROB_LS_POP:
        # individual = LS.LS(individual)
        individual = self.localSearch(individual, timeI)
        self.addIndividual(individual)
        # print(individual)
        # exit(1)
        # print(individual.get_routes())
        # exit(1)

        # “cluster first and then route”
        cluster = SplitDepots.GilletJohnson()  # divisão por depósitos

        # criação de rotas por depósitos, individual é um Solution
        individual = split.splitLinear(cluster, True)
        # individual = split.mountRoutes(cluster)
        # print(individual)
        # print(individual.get_routes())
        # rand = np.random.random_sample()
        # if rand < config.PROB_LS_POP:
        # individual = LS.LS(individual)
        individual = self.localSearch(individual, timeI)
        # print(individual)
        # print(individual.get_routes())

        if individual is not None and self.is_different(individual):
            self.addIndividual(individual)
        # for i in self._population:
        #     print(i)
        #     self.verifyNodes(i)
        # exit(1)

        # formação de rotas aleatórias
        self.formRandomPopulation(size, timeI)

        # individual = np.random.choice(self._population, 1)[0]
        # individual = self.localSearch(individual, timeI)

        self.sortPopulation()
        # print(self.showBestSolution())

        # individual = self.localSearch(self.showBestSolution(), timeI)
        # self._population[len(self._population)-1] = individual
        # print(self.showBestSolution())
        # self.sortPopulation()
        # for i in self._population:
        #     print(i)
        # print(i.get_routes())
        # print(i.get_cost())
        # print(i.get_nRoutesByDepot())

        # print(self.showBestSolution().get_routes())
        # print(self.showBestSolution().get_cost())
        # print(self.showBestSolution().get_nRoutesByDepot())
        # self.test(self.showBestSolution())
        # exit(1)

        # print(len(self._population))
        print("Tempo população: {} minutos".format((time.time()-timeI)/60))
        return self._population

    def formRandomPopulation(self, size, timeIni=0):
        LS = ls()
        split = splitAlg()
        for i in range(2 * size):
            if len(self._population) >= size:
                break
            #seed = i + int(seed * np.random.random())
            cluster = SplitDepots.randomDistribution()
            # criação de rotas por depósitos, individual é um Solution
            individual = split.splitLinear(cluster, True)
            # individual = split.mountRoutes(cluster)
            # print(individual)
            # print(individual.get_routes())
            # rand = np.random.random_sample()
            # if rand < config.PROB_LS_POP:
            # individual = LS.LS(individual)
            individual = self.localSearch(individual, timeIni)
            if individual is not None and self.is_different(individual):
                self.addIndividual(individual)
            # print(individual)
            # print(individual.get_routes())
            # exit(1)

    def verifyNodes(self, solution):
        tour = solution.get_giantTour()
        for i, c1 in enumerate(tour):
            for j, c2 in enumerate(tour):
                if i != j and c1 == c2:
                    print("Elementos iguais")
                    exit(1)

    '''
    Método define as soluções sobreviventes (as de menor custo)
    @return melhor custo da população
    '''

    def defineSurvivors(self, size):
        # posicoes a deletar
        # print(self._population)
        fixIndividuals = max(2, round(0.1*config.SIZE_POP))
        individuals = np.random.choice(self._population[0:(
            len(self._population)-fixIndividuals)], size-fixIndividuals, replace=False)
        for i in range(1, (fixIndividuals+1)):
            individuals = np.append(
                individuals, self._population[(len(self._population)-i)])
        self._population = list(individuals)
        # del self._population[0:(len(self._population)-size)]
        self.sortPopulation()
        # print(self._population)
        # exit(1)
        return self.showBestSolution().get_cost()

    def changePopulation(self):
        print('mudou população')
        # print(self._population)
        lenght = len(self._population)
        sizeSurvivors = max(1, round(lenght*0.1))
        del self._population[0:(len(self._population)-sizeSurvivors)]
        self.definePopulation(config.SIZE_POP)
        # self.sortPopulation()
        # print('depois')
        # print(self._population)
        return self._population

    '''
    Método calcula o rank linear do indivíduo
    http://www.geatbx.com/docu/algindex-02.html#P244_16021
    '''

    def linearRanking(self, individual, pos):
        return 2 - config.SP + 2 * (config.SP - 1) * (pos/(len(self._population) - 1))

    '''
    Método adiciona indivíduo a população
    '''

    def addIndividual(self, solution):
        self._population.append(solution)

    '''
    Método remove o indivíduo de determinado índice da população
    @param índice do indivíduo a ser removido
    @return indivíduo removido ou -1
    '''

    def popIndividual(self, index):
        if index < len(self._population):
            individual = self._population.pop(index)
            return individual
        else:
            return -1

    def removeIndividual(self, individual):
        self._population.remove(individual)

    '''
    Método ordena a população em linear ranking
    '''

    def sortPopulation(self):
        self.sortPopulationDesc()
        self._selProbabilities = []
        for i, individual in enumerate(self._population):
            ranking = self.linearRanking(individual, i)
            individual.set_ranking(ranking)
            self._selProbabilities.append(ranking/len(self._population))

        self._population = sorted(self._population, key=Solution.get_ranking)

    '''
    Método ordena a população em ordem decrescente de custo
    '''

    def sortPopulationDesc(self):
        self._population = sorted(
            self._population, key=Solution.get_cost, reverse=True)

    def get_population(self):
        return self._population

    def get_selProbabilities(self):
        return self._selProbabilities

    def changeIndividual(self, individual, index):
        self._population[index] = individual
        self.sortPopulation()

    '''
    Método verifica se há outro indivíduo com mesmo custo
    '''

    def is_different(self, solution):
        for p in self._population:
            if solution.get_cost() == p.get_cost():
                return False
        return True

    def showBestSolution(self):
        return self._population[len(self._population)-1]

    def showSecondBestSolution(self):
        return self._population[len(self._population)-2]

    def localSearch(self, solution, timeIni=0):
        # heuristics = [ls, lsb]
        # print("Deveria fazer busca local")
        heuristics = [ils]
        probs = []
        idls = 0  # int(np.random.randint(len(heuristics)))
        LS = heuristics[idls]()
        if idls == 0:
            return LS.ils(solution, nGenerations=config.GEN_ILS, timeIni=timeIni, timeMax=config.TIME_POP, ls='lsf', probLs=config.PROB_LS_POP)

        return LS.LS(solution)

    def test(self, solution):
        for r in solution.get_routes():
            r.startValues()
            r.calculeCost()
            print("route: " + str(r))
            print(r.get_totalCost())
