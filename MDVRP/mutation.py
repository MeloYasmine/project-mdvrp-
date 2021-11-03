from distances import Distances as dist
import copy
import numpy as np
import config


class Mutation:

    def mutation1(individual, level=4):

        depots = copy.deepcopy(individual.get_depots())
        if np.random.random() < config.PROB_MUTATION:
            movimentation = [Mutation.M1, Mutation.M2, Mutation.M3]
            level = np.random.randint(len(movimentation * 2))
            for i in range(level):
                m = np.random.randint(len(movimentation))
                depots = movimentation[m](depots)

            individual.set_depots(depots)

        return individual

    def mutation(giantTour, level=2):
        tour = copy.deepcopy(giantTour)
        if np.random.random() < config.PROB_MUTATION:
            movimentation = [Mutation.M1, Mutation.M2, Mutation.M3]
            level = np.random.randint(len(movimentation * 2))
            for i in range(level):
                m = np.random.randint(len(movimentation))
                tour = movimentation[m](tour)

        return tour

    '''
    Método troca dois clientes de lugares
    '''
    def M1(giantTour):
        pos0 = np.random.randint(len(giantTour))
        pos1 = np.random.randint(len(giantTour))
        while pos1 == pos0:
            pos1 = np.random.randint(len(giantTour))

        cst1 = giantTour[pos0]
        cst2 = giantTour[pos1]
        giantTour[pos0] = cst2
        giantTour[pos1] = cst1

        return giantTour

    '''
    Método insere cliente x após cliente y
    '''
    def M2(giantTour):
        pos0 = np.random.randint(len(giantTour))
        pos1 = np.random.randint(len(giantTour))
        while pos1 == pos0:
            pos1 = np.random.randint(len(giantTour))

        cst1 = giantTour[pos0]
        del giantTour[pos0]
        i = pos0
        j = pos1
        if i < j:
            j -= 1
        giantTour.insert(j, cst1)

        return giantTour

    '''
    Método troca cliente x e x+1 com y e y+1
    '''
    def M3(giantTour):
        pos0 = np.random.randint(len(giantTour)-1)
        pos1 = np.random.randint(len(giantTour)-1)

        while pos1 == pos0 or pos1 == pos0 - 1 or pos1 == pos0 + 1:
            pos1 = np.random.randint(len(giantTour)-1)

        cst0 = giantTour[pos0]
        cst1 = giantTour[pos0 + 1]
        cst2 = giantTour[pos1]
        cst3 = giantTour[pos1 + 1]

        giantTour[pos0] = cst2
        giantTour[pos0+1] = cst3
        giantTour[pos1] = cst0
        giantTour[pos1+1] = cst1

        return giantTour
