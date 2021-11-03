from readingDatas import ReadingDatas
from customers import Customers
from depots import Depots
from distances import Distances
from geneticAlgorithm import GeneticAlgorithm as GA
from writingSolutions import WritingSolutions as Write
import numpy as np
import time
import math
import config
import logging
import argparse


def main(SEED, POP, DESC, PROB_MUT, PROB_LS_POP, PROB_LS, PROB_LSB, PROB_LSBP, GEN_ILS, GEN_ILSA, DATFILE, INSTANCE):

    # redefinindo variáveis conforme Package Irace
    # config.FRAC_MAX_DISTRIBUTION = FRAC
    config.SIZE_POP = POP
    config.SIZE_DESC = DESC
    config.PROB_MUTATION = PROB_MUT
    config.PROB_LS_POP = PROB_LS_POP
    config.PROB_LS = PROB_LS
    config.PROB_LS_BEST = PROB_LSB
    config.PROB_LS_BEST_P = PROB_LSBP
    config.GEN_ILS = GEN_ILS
    config.GEN_ILSA = GEN_ILSA

    seed = SEED

    timeIni = time.time()

    # exit(0)

    # recebendo instâncias
    r = ReadingDatas(INSTANCE)
    r.readFile()
    # adicionando clientes
    Customers.addCustomers(r)

    # adicionando depósitos
    Depots.addDepots(r)

    # cálculo das distâncias
    Distances.euclidianDistanceAll(
        Customers.get_customersList(), Depots.get_depotsList())

    ga = GA()
    best = ga.GA(seed)
    cost = best.get_cost()
    timeEnd = (time.time() - timeIni)/60.0

    logging.debug("Melhor indivíduo: %s" % best)
    logging.debug("tempo total: " + str(timeEnd) + " minutos.")
    logging.debug("------------fim algoritmo genético-----------")

    with open(DATFILE, 'w') as f:
        f.write(str(cost))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description='MDVRP com algoritmo genético')
    print(ap)
    ap.add_argument("-v", "--verbose",
                    help="aumentar verbosidade da saída", action="store_true")
    ap.add_argument('--seed', dest='seed', type=int,
                    required=True, help='Semente')
    ap.add_argument('--pop', dest='pop', type=int,
                    required=True, help='Tamanho da população')
    # ap.add_argument('--fracMaxD', dest='fracMaxD', type=float, required=True,
    #                 help='fração máxima de distribuição de clientes entre depósitos')
    ap.add_argument('--desc', dest='desc', type=int,
                    required=True, help='Número de descendentes')
    ap.add_argument('--probMut', dest='probMut', type=float,
                    required=True, help='Probabilidade de mutação')
    ap.add_argument('--probLsPop', dest='probLsPop', type=float, required=True,
                    help='Probabilidade de busca local na geração da população inicial')
    ap.add_argument('--probLs', dest='probLs', type=float,
                    required=True, help='Probabilidade de busca local 1')
    ap.add_argument('--probLsBest', dest='probLsBest', type=float,
                    required=True, help='Probabilidade de busca local na promoção')
    ap.add_argument('--probLsBestP', dest='probLsBestP', type=float,
                    required=True, help='Probabilidade de busca local assíncrona')
    ap.add_argument('--genIls', dest='genIls', type=int,
                    required=True, help='Número de gerações do ILS')
    ap.add_argument('--genIlsa', dest='genIlsa', type=int, required=True,
                    help='Número de gerações do ILS - busca assíncrona')
    ap.add_argument('--datfile', dest='datfile', type=str,
                    required=True, help='Arquivo onde será salvo os resultados')
    ap.add_argument('-i', dest='instance', type=str,
                    required=True, help='Instância')

    args = ap.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug("imprimindo args...........................")

    logging.debug(args)
    logging.debug("seed: "+str(args.seed))
    logging.debug("população: "+str(args.pop))
    # logging.debug("fracMaxD: "+str(args.fracMaxD))
    logging.debug("nDesc: "+str(args.desc))
    logging.debug("probMut: "+str(args.probMut))
    logging.debug("probLsPop: "+str(args.probLsPop))
    logging.debug("probLs: "+str(args.probLs))
    logging.debug("probLsBest: "+str(args.probLsBest))
    logging.debug("probLsBestP: " + str(args.probLsBestP))
    logging.debug("genIls: "+str(args.genIls))
    logging.debug("genIlsa: " + str(args.genIlsa))
    logging.debug("instância: " + str(args.instance))

    main(args.seed, args.pop, args.desc, args.probMut, args.probLsPop,
         args.probLs, args.probLsBest, args.probLsBestP, args.genIls, args.genIlsa, args.datfile, args.instance)
