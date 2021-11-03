from depots import Depots as dpts
from customers import Customers as csts
from solution import Solution
from distances import Distances as dist
import numpy as np
import math
import copy
import config


class SplitDepots:
    _availableDepots = []
    _individual = None

    '''
    Método divide os clientes por depósito
    '''
    def splitByDepot(listCustomers):
        customers = list(copy.deepcopy(listCustomers))
        depots = dpts.get_depotsList()  # dicionário
        split = []  # cada indice da lista uma subrota
        SplitDepots._individual = Solution()
        nDepots = len(depots)
        base = len(customers)/float(nDepots)
        maxCustomers = round(config.FRAC_MAX_DISTRIBUTION * base)
        # print(maxCustomers)
        # dividir em n grupos de clientes
        aux = nDepots
        for n in depots.values():
            load = 0  # carregamento
            tour = []
            # se existir cliente não alocado
            while load < n.get_loadTotal() or aux == 1:
                if len(customers) == 0 or (aux > 1 and len(tour) >= maxCustomers):
                    break
                load = load + customers[0].get_demand()
                if load <= n.get_loadTotal() or aux == 1:
                    tour.append(customers[0])
                    del customers[0]  # atualizar lista
                else:
                    load = load - customers[0].get_demand()
                    break
            split.append(tour)
            aux -= 1
        # associar o primeiro cliente da subrota ao depósito mais próximo
        depotsAvailable = list(copy.deepcopy(depots).keys())

        for s in split:
            if s:
                i = 0
                depot = s[0].get_depotsDistances()[i]
                while str(depot[0]) not in depotsAvailable:
                    i += 1
                    depot = s[0].get_depotsDistances()[i]
                for cst in s:
                    SplitDepots._individual.addGiantTour(
                        cst, depots[str(depot[0])])
                depotsAvailable.remove(str(depot[0]))

        return SplitDepots._individual

    '''
    Método para distribuir clientes de forma aleatória aos depósitos.
    '''
    def randomDistribution():
        #print('Entrou aqui')
        # np.random.seed(idum)
        SplitDepots._individual = Solution()
        customersList = copy.deepcopy(csts.get_customersList())  # dicionário
        # lista com as chaves dos clientes
        keysCst = list(customersList.keys())
        depots = dpts.get_depotsList()  # dicionário
        nDepots = len(depots)
        base = len(customersList)/float(nDepots)
        maxCustomers = round(config.FRAC_MAX_DISTRIBUTION * base)

        nCustomers = len(keysCst)

        # (depósito, [total de demanda, número de clientes alocados]
        control = {}

        for depot in depots:
            control[depot] = [0, 0]
        while nCustomers > 0:  # enquanto tiver cliente não alocado
            # cliente aleatório
            idCst = np.random.randint(0, len(keysCst))
            customer = customersList[keysCst[idCst]]
            # depósito mais próximo
            i = 0
            dpt = customer.get_depotsDistances()[i]
            cont = len(customer.get_depotsDistances())
            aux = 0
            while (control[str(dpt[0])][0] >= depots[str(dpt[0])].get_loadTotal() + 0.0001 or (cont > 1 and control[str(dpt[0])][1] > maxCustomers)) and cont > 0:
                if cont == 1:
                    aux = 1  # indica que todos os depósitos anteriores estão lotados
                i += 1
                dpt = customer.get_depotsDistances()[i]
                cont -= 1

            depot = depots[str(dpt[0])]
            control[str(dpt[0])][0] = control[str(
                dpt[0])][0] + customer.get_demand()
            control[str(dpt[0])][1] = control[str(dpt[0])][1] + 1

            # adicionar cliente ao depósito
            SplitDepots._individual.addGiantTour(customer, depot)
            del keysCst[idCst]  # atualizar lista
            nCustomers -= 1
            # escolher três clientes aleatórios
            if len(keysCst) > 0:
                idcst1 = np.random.randint(0, len(keysCst))
                neighbor1 = customersList[keysCst[idcst1]]
                dist1 = dist.euclidianDistance(customer.get_x_coord(
                ), customer.get_y_coord(), neighbor1.get_x_coord(), neighbor1.get_y_coord())
                idcst2 = np.random.randint(0, len(keysCst))
                neighbor2 = customersList[keysCst[idcst2]]
                dist2 = dist.euclidianDistance(customer.get_x_coord(
                ), customer.get_y_coord(), neighbor2.get_x_coord(), neighbor2.get_y_coord())
                idcst3 = np.random.randint(0, len(keysCst))
                neighbor3 = customersList[keysCst[idcst3]]
                dist3 = dist1 = dist.euclidianDistance(customer.get_x_coord(
                ), customer.get_y_coord(), neighbor3.get_x_coord(), neighbor3.get_y_coord())
                # ver o mais próximo ao cliente
                if dist1 <= dist2 and dist1 <= dist3:
                    close = neighbor1
                    id = idcst1
                elif dist2 <= dist1 and dist2 <= dist3:
                    close = neighbor2
                    id = idcst2
                else:
                    close = neighbor3
                    id = idcst3

                control[str(dpt[0])][0] = control[str(
                    dpt[0])][0] + close.get_demand()
                control[str(dpt[0])][1] = control[str(dpt[0])][1] + 1

                if (control[str(dpt[0])][0] <= depot.get_loadTotal() + 0.0001 and control[str(dpt[0])][1] <= maxCustomers) or aux == 1:
                    # adicionar vizinho mais próximo a solução
                    SplitDepots._individual.addGiantTour(close, depot)
                    del keysCst[id]  # atualizar lista
                    nCustomers -= 1
                else:
                    control[str(dpt[0])][0] = control[str(
                        dpt[0])][0] - close.get_demand()
                    control[str(dpt[0])][1] = control[str(dpt[0])][1] - 1

        # print(self._individual.get_giantTour())
        # print(SplitDepots._individual.get_depots())
        return SplitDepots._individual

    '''
    Implementação do algoritmo de Gillet e Johnson (1976)
    https://www.marinha.mil.br/spolm/sites/www.marinha.mil.br.spolm/files/102830.pdf
    A  ideia  básica  do  referido  algoritmo  é  selecionar  os  pontos  que  apresentam
    a maior razão entre as distâncias às duas medianas mais próximas para serem designados com  prioridade
    '''
    def GilletJohnson():
        SplitDepots._individual = Solution()
        SplitDepots._availableDepots = []
        customersList = copy.deepcopy(csts.get_customersList())  # dicionário

        for dpt in dpts.get_depotsList():
            SplitDepots._availableDepots.append([dpt, dpts.get_depotsList()[dpt].get_loadTotal(
            ), 0.0, 0])  # depósito, carga totaL,demanda total atendida,clientes alocados

        SplitDepots.GilletJohnsonProcedure(
            customersList, len(SplitDepots._availableDepots))
        # print("verificando")
        # print(SplitDepots._individual)
        return SplitDepots._individual

    def GilletJohnsonProcedure(customersList, nDepotsAvailable):
        unallocatedCustomers = customersList
        numberDepotsAvailable = nDepotsAvailable
        depots = dpts.get_depotsList()
        auxiliar = []
        base = len(csts.get_customersList())/float(len(depots))
        maxCustomers = round(config.FRAC_MAX_DISTRIBUTION * base)
        # print("maxCustomers:")
        # print(maxCustomers)
        # print(unallocatedCustomers)
        for cst in unallocatedCustomers:
            depotsDistances = unallocatedCustomers[cst].get_depotsDistances()
            depotsAvailable = []
            # recuperar apenas depósitos com vagas

            for dptDist in depotsDistances:
                for adpts in SplitDepots._availableDepots:
                    if str(dptDist[0]) == adpts[0]:
                        depotsAvailable.append(dptDist)
                        break

            # print("saiu do for")
            # print(depotsAvailable)

            if len(depotsAvailable) > 1:
                fstDepot = depotsAvailable[0]  # primeiro depósito mais próximo
                sndDepot = depotsAvailable[1]  # segundo depósito mais próximo
                fstDistance = fstDepot[1]  # distância do primeiro depósito
                sndDistance = sndDepot[1]  # distância do segundo depósito
                ratio = fstDistance/float(sndDistance)
                auxiliar.append(
                    [unallocatedCustomers[cst], ratio, str(fstDepot[0])])
            elif len(depotsAvailable) == 1:
                fstDepot = depotsAvailable[0]  # primeiro depósito mais próximo
                ratio = 1.0
                auxiliar.append(
                    [unallocatedCustomers[cst], ratio, str(fstDepot[0])])
        # print("check")
        # print(unallocatedCustomers[cst])
        # ordenar lista auxiliar em ordem decrescente
        pts = sorted(auxiliar, key=lambda x: x[1], reverse=False)
        # print("pts:")
        # print(pts)
        # print(SplitDepots._individual)
        for dpt in SplitDepots._availableDepots:
            control = 0
            for pt in pts:
                # print(pt)
                if dpt[0] == pt[2]:
                    dpt[2] = dpt[2] + pt[0].get_demand()
                    dpt[3] = dpt[3] + 1
                    # demanda total > carga total (considera cheio)
                    if (dpt[2] > dpt[1] or dpt[3] > maxCustomers):
                        if numberDepotsAvailable > 1:
                            dpt[2] = dpt[2] - pt[0].get_demand()
                            dpt[3] = dpt[3] - 1

                            dpt[0] = "-1"
                            numberDepotsAvailable -= 1
                            #print("é menor")
                        else:  # se ainda faltarem clientes para serem alocados e restar apenas 1 depósito, a carga total será desrespeitada
                            #print("último depósito disponível")
                            # print(SplitDepots._availableDepots)
                            # adiciona o cliente no depósito mais próximo
                            SplitDepots._individual.addGiantTour(
                                pt[0], depots[dpt[0]])
                            # remove da lista de unallocatedCustomers
                            unallocatedCustomers.pop(str(pt[0].get_id()), -1)
                            control += 1
                    else:
                        # adiciona o cliente no depósito mais próximo
                        SplitDepots._individual.addGiantTour(
                            pt[0], depots[dpt[0]])
                        # remove da lista de unallocatedCustomers
                        unallocatedCustomers.pop(str(pt[0].get_id()), -1)
                        control += 1

        # print(":")
        # print(SplitDepots._availableDepots)
        # print(unallocatedCustomers)
        # print(SplitDepots._availableDepots)
        if len(unallocatedCustomers) > 0:
            SplitDepots.GilletJohnsonProcedure(
                unallocatedCustomers, numberDepotsAvailable)
