# dados base
DIRECTORY_DATAS = "instances/"
DIRECTORY_RESULT = "result/"
INSTANCES = {"p01": 576.87, "p02": 473.53, "p03": 641.19, "p04": 1001.04, "p05": 750.03, "p06": 876.50, "p07": 881.97, "p08": 4387.38, "p09": 3873.64, "p10": 3650.04, "p11": 3546.06,
             "p12": 1318.95, "p13": 1318.95, "p14": 1360.12, "p15": 2505.42, "p16": 2572.23, "p17": 2708.99, "p18": 3702.85, "p19": 3827.06, "p20": 4058.07, "p21": 5474.74, "p22": 5702.16, "p23": 6078.75}


SOFT_VEHICLES = False
SOFT_DURATION = False

# parametros
# fração máxima de distribuição de clientes entre depósitos
FRAC_MAX_DISTRIBUTION = 100
SIZE_POP = 5  # população inicial
SIZE_DESC = 5  # número de descendentes
PROB_MUTATION = 0.1
PROB_LS_POP = 0.2  # probabilidade de busca local na formação da população
PROB_LS = 0.7  # probabilidade busca local
PROB_LS_BEST = 0.5  # probabilidade busca local promotion
PROB_LS_BEST_P = 0.9  # probabilidade busca local assíncrona
GEN = 200  # número de gerações
GEN_NO_EVOL = 30  # número permitido de gerações sem mudanças
SP = 2  # pressão seletiva para linear ranking
N_REPETITIONS = 10
TIME_TOTAL = 3600  # 3600 tempo em segundos
TIME_GEN = 360  # 360 tempo em segundos / tempo máximo em cada geracao
TIME_POP = 120 # 120 
IT_ILS = 10
GEN_ILS = 10
IT_ILSA = 10000
GEN_ILSA = 100000

# METRIC = 3.5 # métrica de diversidade
# CONT_METRIC = 5 # quantidade de vezes que a métrica de diversidade pode ser desrespeitada
