'''
Arquivo responsável pela leitura das instâncias
@author Fabiana Barreto Pereira
'''
import math
class ReadingDatas:

    def __init__(self,name_file):
        self._f = name_file
        self._numberVehicles = 0
        self._numberCustomers = 0
        self._numberDepots = 0
        self._load = 0
        self._dataDepots = []
        self._dataCustomers = []
        self._durationRoute = 0

    '''
    Método faz leitura dos dados do arquivo e armazena nas variáveis correspondentes
    '''
    def readFile(self):
        f = open(self._f,'r')
        fstLine = f.readline()
        head = fstLine.split()
        self._numberVehicles = int(head[1])
        self._numberCustomers = int(head[2])
        self._numberDepots = int(head[3])
        #dados depósitos
        for i in range(self._numberDepots):
            line = f.readline().split()
            self._load = float(line[1])
            self._durationRoute = float(line[0])
            if self._durationRoute == 0.0:
                self._durationRoute = math.inf

        #dados clientes
        for i in range(self._numberCustomers):
            self._dataCustomers.append(f.readline())

        #dados clientes - últimas linhas - refere-se aos depósitos
        self._dataDepots = f.readlines()


    def get_numberVehicles(self):
        return self._numberVehicles

    def get_numberCustomers(self):
        return self._numberCustomers

    def get_numberDepots(self):
        return self._numberDepots

    def get_load(self):
        return self._load

    def get_dataCustomers(self):
        return self._dataCustomers

    def get_durationRoute(self):
        return self._durationRoute

    def get_dataDepots(self):
        return self._dataDepots
