'''
Arquivo responsável por armazenar dados de todos os depósitos
@author Fabiana Barreto Pereira
'''

from depot import Depot


class Depots:
    _depotsList={} #dicionário de depósitos
    _numberDepots = 0
    #_loadVehicle = 0 #capacidade de cada veículo
    #_durationRoute = 0
    def addDepots(rd):
        ldepot=[]
        Depots._numberDepots = rd.get_numberDepots()
        #Depots._loadVehicle = rd.get_load()
        #Depots._durationRoute = rd.get_durationRoute()
        for i in range(Depots._numberDepots):
            dataDepot = rd.get_dataDepots()[i].split()
            dpt = Depot()
            dpt.set_id(int(dataDepot[0]))
            dpt.set_xy_coord(float(dataDepot[1]),float(dataDepot[2]))
            dpt.set_durationRoute(rd.get_durationRoute())
            dpt.set_numberVehicles(rd.get_numberVehicles())
            dpt.set_loadVehicle(rd.get_load())
            dpt.set_loadTotal(rd.get_load()*rd.get_numberVehicles())

            ldepot.append((dataDepot[0],dpt))

        Depots._depotsList=dict(ldepot)

    def get_depotsList():
        return Depots._depotsList

    def get_numberDepots():
        return Depots._numberDepots
'''
    def get_loadVehicle():
        return Depots._loadVehicle

    def get_durationRoute():
        return Depots._durationRoute
'''
