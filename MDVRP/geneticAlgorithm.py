from population import Population
from crossover import Crossover as cross
from splitDepots import SplitDepots
from splitAlgorithms import SplitAlgorithms as splitAl
from mutation import Mutation
from localSearchFirst import LocalSearch as ls
from localSearchBest import LocalSearchBest as lsb
from iteratedLocalSearch import IteratedLocalSearch as ils
import numpy as np
import config
import concurrent.futures
import copy
import time
import traceback
import threading as th
import logging

mutex = th.Semaphore(1)
newIndividuals = []  # indivíduos obtidos na busca local best improvement


class GeneticAlgorithm:
    '''
    Método responsável pelo algoritmo genético
    '''

    def GA(self, seed):
        global mutex
        global newIndividuals
        split = splitAl()
        np.random.seed(seed)
        # define população inicial
        pop = Population()
        population = pop.definePopulation(config.SIZE_POP)
        def minor(x, y): return x if x.get_cost() < y.get_cost() else y
        best = 0
        bestPrev = 0
        cont = 0
        timeControl = 0
        threads = []
        level = 2
        # avalie a população

        # critério de parada
        i = 0
        timeIni = time.time()
        while i < config.GEN and cont <= 2*config.GEN_NO_EVOL and timeControl < config.TIME_TOTAL:
            tAllIni = time.time()
            bestPrev = best
            tLS = 0

            # sizePopulation = len(population)
            descendant = []
            for j in range(round(config.SIZE_DESC/2)):
                tGenIni = time.time()
                selProbalities = pop.get_selProbabilities()  # probabilidade de seleção
                # print("prob: "+str(len(selProbalities)))

                # selecione os pais

                aux = np.random.choice(
                    population, 2, replace=False, p=selProbalities)

                P1 = minor(aux[0], aux[1])

                aux = np.random.choice(
                    population, 2, replace=False, p=selProbalities)

                P2 = minor(aux[0], aux[1])

                # Crossover

                rand = np.random.random_sample()
                # print(rand)
                # print(P1)
                # print(P2)
                children = []

                if rand > 0.5:
                    children = cross.OBX1(copy.deepcopy(P1), copy.deepcopy(P2))
                else:
                    children = cross.PMX1(copy.deepcopy(P1), copy.deepcopy(P2))
                # print("children: \n")
                # print(children)
                # for a in range(2):
                #     for e1, c1 in enumerate(children[a].get_giantTour()):
                #         for e2, c2 in enumerate(children[a].get_giantTour()):
                #             if e1 != e2 and c1 == c2:
                #                 print("Elementos iguais")
                #                 exit(1)

                # Mutação

                # duas threads
                modChildren = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                    future_to_child = {executor.submit(
                        Mutation.mutation1, child, level): child for child in children}
                    for future in concurrent.futures.as_completed(future_to_child):
                        child = future_to_child[future]
                        try:
                            indiv = future.result()
                            modChildren.append(indiv)
                        except Exception as exc:
                            print('%s gerou uma exceção na busca local: %s' %
                                  (str(child), exc))

                # split
                # cluster = SplitDepots.splitByDepot(modChildren[0])
                # print(cluster)
                individual1 = split.splitLinear(modChildren[0], True)
                # individual1 = split.mountRoutes(cluster)
                # cluster = SplitDepots.splitByDepot(modChildren[1])
                # print(cluster)
                individual2 = split.splitLinear(modChildren[1], True)
                # individual2 = split.mountRoutes(cluster)

                individuals = [individual1, individual2]

                # print("individual: ")
                # print(individual1)
                # print(individual2)
                for a in range(2):
                    for ii, c1 in enumerate(individuals[a].get_giantTour()):
                        for jj, c2 in enumerate(individuals[a].get_giantTour()):
                            if ii != jj and c1 == c2:
                                print("Elementos iguais na mutação")
                                exit(1)

                # Busca Local
                ILS = ils()
                # solutions = ILS.ils(individual1, 25)
                # for ii, c1 in enumerate(solutions.get_giantTour()):
                #     for jj, c2 in enumerate(solutions.get_giantTour()):
                #         if ii != jj and c1 == c2:
                #             print("Elementos iguais na ils")
                #             exit(1)

                # exit(1)
                # duas threads
                ini = time.time()
                modIndividuals = []
                LS = ls()
                individuals.append(P1)
                individuals.append(P2)
                # modIndividuals.append(LS.LS(individuals[0]))
                # modIndividuals.append(LS.LS(individuals[1]))
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                    # future_to_individual = {executor.submit(
                    #     LS.LS, ind, nMovimentations='random', where='ls', timeIni=tGenIni): ind for ind in individuals}
                    # future_to_individual = {executor.submit(
                    #     ILS.ils, ind, config.GEN_ILS, timeIni=tGenIni, timeMax=config.TIME_GEN): ind for ind in individuals}
                    future_to_individual = {executor.submit(
                        self.localSearch, ind, prob=config.PROB_LS, nMovimentations='random', timeIni=tGenIni): ind for ind in individuals}
                    for future in concurrent.futures.as_completed(future_to_individual):
                        ind = future_to_individual[future]
                        try:
                            indiv = future.result()
                            modIndividuals.append(indiv)
                        except Exception as exc:
                            print('%s gerou uma exceção na busca local: %s' %
                                  (str(ind), exc))
                            traceback.print_exc()
                # print(future_to_individual)
                # print(individuals[0])
                # print(modIndividuals)
                tTotal = time.time() - ini
                tLS += tTotal
                for a in range(2):
                    for e1, c1 in enumerate(modIndividuals[a].get_giantTour()):
                        for e2, c2 in enumerate(modIndividuals[a].get_giantTour()):
                            if e1 != e2 and c1 == c2:
                                print("Elementos iguais na busca local")
                                exit(1)

                # avalie a população

                for a in range(2):
                    # indivíduo diferente do resto da população
                    if self.is_different(modIndividuals[a], descendant):
                        descendant.append(modIndividuals[a])

            # inserir descendentes à população

            for desc in descendant:
                if pop.is_different(desc):
                    pop.addIndividual(desc)

            # inserir indivíduos da lista newIndividuals (se existir) à população

            # início seção crítica
            mutex.acquire()
            # print("verificar lista")
            # print(newIndividuals)
            if newIndividuals:
                # print("novo: "+ str(len(newIndividuals)))
                for ni in newIndividuals:
                    if pop.is_different(ni):
                        pop.addIndividual(ni)
                newIndividuals = []
            mutex.release()
            # fim seção crítica

            pop.sortPopulation()
            population = pop.get_population()

            # promoção - busca local first improvement de 10% da população
            ini = time.time()
            p = max(round(config.SIZE_POP * 0.1), 1)  # 10% da população
            LSBetter = lsb()

            modIndividuals = []
            individuals = []
            selProbalities = pop.get_selProbabilities()  # probabilidade de seleção
            individuals = np.random.choice(
                population, p, replace=False, p=selProbalities)
            individuals = np.append(individuals, pop.showBestSolution())

            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                # future_to_individual = {executor.submit(
                #     LSBetter.LS, ind, where='ls', timeIni=tGenIni): ind for ind in individuals}
                future_to_individual = {executor.submit(
                    self.localSearch, ind, prob=config.PROB_LS_BEST, nMovimentations='all', timeIni=tGenIni): ind for ind in individuals}
                # future_to_individual = {executor.submit(
                #     ILS.ils, ind, config.N_REPETITIONS, timeIni=tGenIni, timeMax=config.TIME_GEN): ind for ind in individuals}
                for future in concurrent.futures.as_completed(future_to_individual):
                    ind = future_to_individual[future]
                    try:
                        indiv = future.result()
                        modIndividuals.append(indiv)
                    except Exception as exc:
                        print(
                            '%s gerou uma exceção na busca local - promoção: %s' % (str(ind), exc))
                        traceback.print_exc()

            # avalie a população

            for a in modIndividuals:

                # for e1, c1 in enumerate(a.get_giantTour()):
                #     for e2, c2 in enumerate(a.get_giantTour()):
                #         if e1 != e2 and c1 == c2:
                #             print("Elementos iguais na busca local - promoção")
                #             exit(1)

                # indivíduo diferente do resto da população
                if pop.is_different(a):
                    pop.addIndividual(a)

            tTotalP = time.time() - ini

            pop.sortPopulation()

            # defina a população sobrevivente

            best = pop.defineSurvivors(config.SIZE_POP)
            population = pop.get_population()

            # busca local exaustiva assícrona - best improvemment dos dois melhores indivíduos

            individuals = []
            selProbalities = pop.get_selProbabilities()  # probabilidade de seleção
            individuals = np.random.choice(population, 1, p=selProbalities)
            individuals = np.append(individuals, pop.showBestSolution())
            individuals = np.append(individuals, pop.showSecondBestSolution())

            # cria threads
            for individual in individuals:
                if np.random.random_sample() < config.PROB_LS_BEST_P:
                    if th.active_count() < 4:  # máximo 3 threads agindo de forma assíncrona
                        a = MyThread(individual, timeIni)  # inicializa thread
                        a.start()
                        threads.append(a)

            # verifica número de gerações sem melhoras

            if round(bestPrev, 9) == round(best, 9):
                cont += 1
                level += 1

                # config.SOFT_VEHICLES = True
            else:
                cont = 0
                level = 2
                # config.SOFT_VEHICLES = False

            if cont > config.GEN_NO_EVOL:
                mt = ils()
                individualM = mt.pertubation(
                    copy.deepcopy(pop.showBestSolution()), level)
                pop.addIndividual(individualM)
                pop.sortPopulation()
                aux = 0

                # verifica se há solutions na lista newIndividuos

                # início seção crítica
                mutex.acquire()
                if newIndividuals:
                    aux = 1
                    for ni in newIndividuals:
                        if pop.is_different(ni):
                            pop.addIndividual(ni)
                    pop.sortPopulation()
                newIndividuals = []
                mutex.release()
                # fim seção crítica

                if aux >= 0:
                    best = pop.defineSurvivors(config.SIZE_POP)
                    if round(bestPrev, 9) != round(best, 9):
                        cont = 0

                # print("ALERTA POPULAÇÃO PAROU DE EVOLUIR")
                # print(pop.get_population())
                # logging.debug("ALERTA POPULAÇÃO PAROU DE EVOLUIR")

            pop.sortPopulation()
            population = pop.get_population()
            tAll = time.time() - tAllIni  # tempo da geração
            timeControl = time.time() - timeIni  # tempo total

            # print("GERAÇÃO: {} - Custo: {} - Tempo LS: {} - Tempo LS Promotion: {} - Tempo Total: {}".format(i,
                                                                                                            #  pop.showBestSolution().get_cost(), tLS/60, tTotalP/60, tAll/60))
            # logging.debug("GERAÇÃO: {} - Custo: {} - Tempo LS: {} - Tempo LS Promotion: {} - Tempo Total: {}".format(i,
            #                                                                                                          pop.showBestSolution().get_cost(), tLS/60, tTotalP/60, tAll/60))
            i += 1

        # finalizar thread se ultrapassar o tempo limite.
        if (time.time() - timeIni) >= config.TIME_TOTAL:
            for t in threads:
                t.stop()
        else:
            for t in threads:
                t.join()

        # verificar se há indivíduos na lista newIndividuals
        if newIndividuals:
            for ni in newIndividuals:
                if pop.is_different(ni):
                    pop.addIndividual(ni)
        newIndividuals = []

        # ordena população
        pop.sortPopulation()
        # print(pop.showBestSolution().get_routes())
        # print(pop.showBestSolution().get_cost())
        # print(pop.showBestSolution().get_nRoutesByDepot())
        # self.test(pop.showBestSolution())

        # retorna melhor indivíduo
        return pop.showBestSolution()

    def is_different(self, solution, descendant):
        for d in descendant:
            if solution.get_cost() == d.get_cost():
                return False
        return True

    def localSearch(self, solution, prob=config.PROB_LS, nMovimentations='all', timeIni=0):
        heuristics = [ls, lsb]
        # heuristics = [ls, lsb, ils]
        probs = []
        idls = int(np.random.randint(len(heuristics)))
        LS = heuristics[idls]()
        if idls == 2:
            return LS.LS(solution, itMax=config.IT_ILS, timeIni=timeIni, timeMax=config.TIME_GEN)

        return LS.LS(solution, prob=prob, where='ls', timeIni=timeIni, timeMax=config.TIME_GEN, nMovimentations=nMovimentations)

    def test(self, solution):
        for r in solution.get_routes():
            r.startValues()
            r.calculeCost()
            print("route: " + str(r))
            print(r.get_costWithoutPenalty())


class MyThread(th.Thread):

    def __init__(self, solution, timeIni):
        th.Thread.__init__(self)
        self._solution = solution
        self.kill = th.Event()
        self._timeIni = timeIni

    def run(self):
        global mutex
        global newIndividuals
        LSB = lsb()
        ILS = ils()
        # print("executando thread")
        # print("solution: "+str(self._solution)+"\n")
        # individual = LSB.LS(self._solution)
        # individual = ILS.ils(self._solution, config.GEN_ILSA,
        #                      probLs=config.PROB_LS_BEST_P)
        individual = self.localSearch(self._solution, self._timeIni)
        # print("individual: "+ str(individual)+"\n")
        cont = 0

        # seção crítica
        mutex.acquire()
        for ind in newIndividuals:
            if ind.get_cost() == individual.get_cost():
                cont = 1
                break
        if cont == 0:
            newIndividuals.append(individual)
        mutex.release()
        # print("saiu da thread")

    def stop(self):
        # print("Thread parando")
        self.kill.set()

    def localSearch(self, solution, prob=config.PROB_LS_BEST_P, timeIni=0, timeMax=config.TIME_TOTAL):
        heuristics = [ils]
        probs = []
        idls = int(np.random.randint(len(heuristics)))
        LS = heuristics[idls]()
        if idls == 0:
            return LS.ils(solution, config.GEN_ILSA, ls='lsf',
                          probLs=config.PROB_LS_BEST_P, timeIni=timeIni, timeMax=timeMax)
        else:
            return LS.LS(solution)
