'''
Arquivo responsável por carregar a aplicação
@author Fabiana Barreto Pereira
'''
from readingDatas import ReadingDatas
from customers import Customers
from depots import Depots
from distances import Distances
from geneticAlgorithm import GeneticAlgorithm as GA
from writingSolutions import WritingSolutions as Write
from route import Route
import numpy as np
import time
import math
import config
import sys


def main():
    print(80*"*")
    print("Algoritmo genético para o Problema de Roteamento de Veículos com Múltiplos Depósitos")
    print(80*"*")
    args = sys.argv
    if len(args) > 1:
        instance = args[1]  # primeiro parâmetro é o nome do sistema
        startGA(instance)
    while True:
        args = input(
            'Insira o caminho da instância ou q para sair da aplicação:\n')
        if args == 'q':
            exit(0)
        startGA(args)


def startGA(instance):
    seed = 7890
    inst = instance.split("/")
    nameInstance = inst[len(inst)-1]
    # print("*************************************")
    # print(nameInstance)
    # recebendo instâncias
    r = ReadingDatas(instance)
    r.readFile()
    # adicionando clientes
    Customers.addCustomers(r)
    # for cst in Customers.get_customersList().values():
    # print(cst)

    # adicionando depósitos
    Depots.addDepots(r)
    # print("\n\n\n\")
    # for dpt in Depots.get_depotsList().values():
    # print(dpt)

    # cálculo das distâncias
    Distances.euclidianDistanceAll(
        Customers.get_customersList(), Depots.get_depotsList())

    # test([44, 45, 15, 37, 17], 51)
    # test([40, 13, 18, 4], 51)
    # test([42, 19, 41], 51)
    # test([26, 43, 24, 25, 14], 52)
    # test([32, 1, 8, 7, 23], 52)
    # test([12, 47], 52)
    # test([46, 27, 48, 6], 52)
    # test([5, 38, 9], 53)
    # test([16, 50, 34], 53)
    # test([49, 10, 33, 39, 30], 53)
    # test([2, 11], 54)
    # test([3, 28, 31, 22], 54)
    # test([29, 21, 35, 36, 20], 54)
    # exit(1)

    # for cst in Customers.get_customersList():
    #     print(cst)
    #     print(Customers.get_customersList()[cst].get_depotsDistances())
    # print("\n\n\n")
    # for cst in Customers.get_customersList():
    #     print(cst)
    #     print(Customers.get_customersList()[cst].get_neighborsDistances())
    # exit(1)
    minor = math.inf
    worst = 0
    bestSolution = None
    mTime = 0
    mCost = 0

    for i in range(config.N_REPETITIONS):
        write = Write(config.DIRECTORY_RESULT + nameInstance)
        ini = time.time()
        ga = GA()
        best = ga.GA(seed)
        print(best)
        print(best.get_routes())
        cost = best.get_cost()
        if cost < minor:
            minor = best.get_cost()
            bestSolution = best
        if cost > worst:
            worst = best.get_cost()
        write.writeFile(best)
        end = (time.time() - ini)/60
        mTime += end
        mCost += cost
        print("tempo: "+str(end))
    mTime /= config.N_REPETITIONS
    mCost /= config.N_REPETITIONS

    # calcular gap
    print("gap médio: "+str(gap(nameInstance, mCost))+" \n gap melhor: "+str(gap(nameInstance, minor)) + " \n gap pior: " + str(gap(nameInstance, worst)) +
          " \n custo médio: "+str(mCost)+" \n melhor custo: "+str(minor) + " \n pior custo: "+str(worst)+" \n tempo médio: "+str(mTime)+"\n")


def gap(nameInstance, cost):
    if nameInstance in config.INSTANCES:
        return (100*((cost - config.INSTANCES[nameInstance])/config.INSTANCES[nameInstance]))
    else:
        print("Não foi possível calcular GAP")
        return "-1"


def test(route, depot):
    r = Route(Depots.get_depotsList()[str(depot)])
    r.startValues()
    for ct in route:
        r.addCustomer(Customers.get_customersList()[str(ct)])
    r.calculeCost()
    print(r.get_totalCost())


if __name__ == "__main__":
    main()
