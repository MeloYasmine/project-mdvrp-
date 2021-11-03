'''
Arquivo responsável por computar e verificar restrições da rota
'''
from distances import Distances as dist
from customers import Customers as csts
from depots import Depots as dpts
from customer import Customer
import copy


class Route:
    _tour = None
    _depot = None
    _cost = float()
    _penaltyDuration = float()
    _penaltyDemand = float()
    _totalDemand = float()
    _totalService = float()

    def __init__(self, depot):
        self._tour = []  # lista de Customer
        self._depot = depot
        self._infeasible = False

    '''
    Método reinicia variáveis
    '''

    def startValues(self):
        self._cost = 0.0
        self._penaltyDuration = 0.0
        self._penaltyDemand = 0.0
        self._totalDemand = 0.0
        self._totalService = 0.0
        self._infeasible = False

    '''
    Método adiciona clientes a rota
    @param id dos clientes (string)
    '''

    def addCustomer(self, customer):
        self._tour.append(customer)

    '''
    Método insere cliente na rota no índice index
    @param cliente
    @param índice
    '''

    def insertCustomer(self, customer, index):
        self._tour.insert(index, customer)

    '''
    Método remove cliente da rota
    @param índice do cliente a ser removido
    @return cliente removido
    '''

    def popCustomer(self, index):
        return self._tour.pop(index)

    '''
    Método remove um elemento da lista (cliente)
    @param cliente a ser removido
    '''

    def removeCustomer(self, customer):
        try:
            self._tour.remove(customer)
        except:
            raise ""

    '''
    Método troca o customer do índice informado pelo customer recebido
    @param customer
    @param índice do cliente a ser substituído
    '''

    def changeCustomer(self, customer, index):
        self._tour[index] = customer

        '''
    Método calcula custo total da rota
    '''

    def calculeCost(self):
        cost = 0.0
        demand = 0.0
        service = 0.0
        length = len(self._tour)

        # custo do depósito ao primeiro cliente
        customer = self._tour[0]
        cost += dist.euclidianDistance(customer.get_x_coord(), customer.get_y_coord(
        ), self._depot.get_x_coord(), self._depot.get_y_coord())

        # custo do último cliente ao depósito
        customer = self._tour[length-1]
        cost += dist.euclidianDistance(customer.get_x_coord(), customer.get_y_coord(
        ), self._depot.get_x_coord(), self._depot.get_y_coord())

        # custo dos clientes intermediários
        for i in range(length):
            customer = self._tour[i]
            demand += customer.get_demand()
            service += customer.get_service()
            if i+1 < length:
                nextCustomer = self._tour[i+1]
                cost += dist.euclidianDistance(customer.get_x_coord(), customer.get_y_coord(
                ), nextCustomer.get_x_coord(), nextCustomer.get_y_coord())

        self._totalDemand = demand
        self._totalService = service
        self._cost = cost
        self.updatePenalty()

    '''
    Método atualiza penalizações caso restrições de duração total ou de capacidade sejam quebradas
    '''

    def updatePenalty(self):
        # se infrigir a restrição vai sofrer acréscimo de 1.000 x excedente
        capacity = float(self._depot.get_loadVehicle())
        self._infeasible = False
        if self._totalDemand > capacity:
            self._penaltyDemand = 1000 * (self._totalDemand - capacity)
            self._infeasible = True
        else:
            self._penaltyDemand = 0.0

        cost = self._cost + self._totalService
        duration = float(self._depot.get_durationRoute())
        # print(duration)
        if cost > duration:
            self._penaltyDuration = 1000 * abs(cost - duration)
            self._infeasible = True
        else:
            self._penaltyDuration = 0.0

    '''
    Método retorna o custo total calculado
    '''

    def get_totalCost(self):
        return self._cost + self._penaltyDuration + self._penaltyDemand

    def get_penaltyDuration(self):
        return self._penaltyDuration

    def get_penaltyDemand(self):
        return self._penaltyDemand

    def get_costWithoutPenalty(self):
        return self._cost

    def set_cost(self, cost, load, service):
        self._cost = cost
        self._totalDemand = load
        self._totalService = service
        self.updatePenalty()

    def get_tour(self):
        return self._tour

    def get_depot(self):
        return self._depot

    def set_depot(self, depot):
        self._depot = depot

    def is_infeasible(self):
        return self._infeasible

    def get_totalDemand(self):
        return self._totalDemand

    def get_totalService(self):
        return self._totalService

    '''
    Método imprime a rota com o depósito e o custo associado
    '''

    def printRoute(self):
        print("depósito: {} - custo: {:10.4f} - demanda: {:10.4f} - tempo de serviço: {:10.4f} - rota: {}".format(
            self._depot.get_id(), self.get_totalCost(), self._totalDemand, self._totalService, str(self._tour)))

    def __str__(self):
        return "depósito: {} - custo: {:10.4f} - demanda: {:10.4f} - tempo de serviço: {:10.4f} - rota: {}".format(self._depot.get_id(), self.get_totalCost(), self._totalDemand, self._totalService, str(self._tour))

    def __repr__(self):
        return "depósito: {} - custo: {:10.4f} - demanda: {:10.4f} - tempo de serviço: {:10.4f} - rota: {}\n".format(self._depot.get_id(), self.get_totalCost(), self._totalDemand, self._totalService, str(self._tour))
        # "depósito: {} - rota: {} - custo com penalização: {:10.4f}\n".format(self._depot.get_id(),str(self._tour),self.get_totalCost())

    def costSwapNodes(self, idU, idV, routeU, routeV):
        costU = routeU.get_costWithoutPenalty()
        tourU = routeU.get_tour()
        lengthU = len(tourU)
        costTotalU = 0
        costV = routeV.get_costWithoutPenalty()
        tourV = routeV.get_tour()
        lengthV = len(tourV)
        costTotalV = 0

        serviceU = routeU.get_totalService(
        ) - tourU[idU].get_service() + tourV[idV].get_service()
        loadU = routeU.get_totalDemand(
        ) - tourU[idU].get_demand() + tourV[idV].get_demand()

        serviceV = routeV.get_totalService(
        ) - tourV[idV].get_service() + tourU[idU].get_service()
        loadV = routeV.get_totalDemand(
        ) - tourV[idV].get_demand() + tourU[idU].get_demand()

        if idU != 0 and idU + 1 < lengthU:
            beforeU = tourU[idU-1]
            afterU = tourU[idU+1]
        elif idU == 0 and idU == lengthU - 1:
            beforeU = routeU.get_depot()
            afterU = routeU.get_depot()
        elif idU == lengthU - 1:
            beforeU = tourU[idU-1]
            afterU = routeU.get_depot()
        else:
            beforeU = routeU.get_depot()
            afterU = tourU[idU+1]

        costU = costU - dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) - \
            dist.euclidianDistance(tourU[idU].get_x_coord(), tourU[idU].get_y_coord(), afterU.get_x_coord(), afterU.get_y_coord()) + \
            dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourV[idV].get_x_coord(), tourV[idV].get_y_coord()) + \
            dist.euclidianDistance(tourV[idV].get_x_coord(
            ), tourV[idV].get_y_coord(), afterU.get_x_coord(), afterU.get_y_coord())

        costTotalU = costU

        if costU + serviceU > routeU.get_depot().get_durationRoute():
            costTotalU += 1000
        if loadU > routeU.get_depot().get_loadVehicle():
            costTotalU += 1000

        if idV != 0 and idV + 1 < lengthV:
            beforeV = tourV[idV-1]
            afterV = tourV[idV+1]
        elif idV == 0 and idV == lengthV - 1:
            beforeV = routeV.get_depot()
            afterV = routeV.get_depot()
        elif idV == lengthV - 1:
            beforeV = tourV[idV-1]
            afterV = routeV.get_depot()
        else:
            beforeV = routeV.get_depot()
            afterV = tourV[idV+1]

        costV = costV - dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourV[idV].get_x_coord(), tourV[idV].get_y_coord()) - \
            dist.euclidianDistance(tourV[idV].get_x_coord(), tourV[idV].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord()) + \
            dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) + \
            dist.euclidianDistance(tourU[idU].get_x_coord(
            ), tourU[idU].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord())

        costTotalV = costV

        if costV + serviceV > routeV.get_depot().get_durationRoute():
            costTotalV += 1000
        if loadV > routeV.get_depot().get_loadVehicle():
            costTotalV += 1000
        controlCostU = [costTotalU, costU, loadU, serviceU]
        controlCostV = [costTotalV, costV, loadV,
                        serviceV]  # [costTotal,cost,load,service]
        return controlCostU, controlCostV

    def costSwapSameRoute(self, idU, idV, routeU):
        costU = routeU.get_costWithoutPenalty()
        tourU = routeU.get_tour()
        lengthU = len(tourU)
        costTotalU = 0

        serviceU = routeU.get_totalService()
        loadU = routeU.get_totalDemand()

        if idU != 0 and idU + 1 < lengthU:
            beforeU = tourU[idU-1]
            afterU = tourU[idU+1]
        elif idU == 0 and idU == lengthU - 1:
            beforeU = routeU.get_depot()
            afterU = routeU.get_depot()
        elif idU == lengthU - 1:
            beforeU = tourU[idU-1]
            afterU = routeU.get_depot()
        else:
            beforeU = routeU.get_depot()
            afterU = tourU[idU+1]

        if idV != 0 and idV + 1 < lengthU:
            beforeV = tourU[idV-1]
            afterV = tourU[idV+1]
        elif idV == 0 and idV == lengthU - 1:
            beforeV = routeU.get_depot()
            afterV = routeU.get_depot()
        elif idV == lengthU - 1:
            beforeV = tourU[idV-1]
            afterV = routeU.get_depot()
        else:
            beforeV = routeU.get_depot()
            afterV = tourU[idV+1]

        if idV == idU + 1:
            costU = costU - dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) - \
                dist.euclidianDistance(tourU[idU].get_x_coord(), tourU[idU].get_y_coord(), afterU.get_x_coord(), afterU.get_y_coord()) -\
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord()) + \
                dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idV].get_x_coord(), tourU[idV].get_y_coord()) + \
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) + \
                dist.euclidianDistance(tourU[idU].get_x_coord(
                ), tourU[idU].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord())
        elif idU == idV + 1:
            costU = costU - dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourU[idV].get_x_coord(), tourU[idV].get_y_coord()) - \
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord()) -\
                dist.euclidianDistance(tourU[idU].get_x_coord(), tourU[idU].get_y_coord(), afterU.get_x_coord(), afterU.get_y_coord()) + \
                dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) + \
                dist.euclidianDistance(tourU[idU].get_x_coord(), tourU[idU].get_y_coord(), tourU[idV].get_x_coord(), tourU[idV].get_y_coord()) + \
                dist.euclidianDistance(tourU[idV].get_x_coord(
                ), tourU[idV].get_y_coord(), afterU.get_x_coord(), afterU.get_y_coord())
        else:
            costU = costU - dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) - \
                dist.euclidianDistance(tourU[idU].get_x_coord(), tourU[idU].get_y_coord(), afterU.get_x_coord(), afterU.get_y_coord()) -\
                dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourU[idV].get_x_coord(), tourU[idV].get_y_coord()) -\
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord()) + \
                dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idV].get_x_coord(), tourU[idV].get_y_coord()) + \
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), afterU.get_x_coord(), afterU.get_y_coord()) + \
                dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) + \
                dist.euclidianDistance(tourU[idU].get_x_coord(
                ), tourU[idU].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord())

        costTotalU = costU

        if costU + serviceU > routeU.get_depot().get_durationRoute():
            costTotalU += 1000
        if loadU > routeU.get_depot().get_loadVehicle():
            costTotalU += 1000
        controlCostU = [costTotalU, costU, loadU,
                        serviceU]  # [costTotal,cost,load,service]
        return controlCostU

    def costRemoveUinsertAfterV(self, idU, idV, routeU, routeV):
        '''
        Método calcula o custo de remover u e inseri-lo após v
        '''
        costU = routeU.get_costWithoutPenalty()
        tourU = routeU.get_tour()
        lengthU = len(tourU)
        costTotalU = costU

        costV = routeV.get_costWithoutPenalty()
        tourV = routeV.get_tour()
        lengthV = len(tourV)
        costTotalV = costV

        serviceU = routeU.get_totalService()
        loadU = routeU.get_totalDemand()

        serviceV = routeV.get_totalService()
        loadV = routeV.get_totalDemand()

        serviceU = serviceU - tourU[idU].get_service()
        loadU = loadU - tourU[idU].get_demand()

        serviceV = serviceV + tourU[idU].get_service()
        loadV = loadV + tourU[idU].get_demand()

        if idU != 0:
            beforeU = tourU[idU-1]
        else:
            beforeU = routeU.get_depot()

        if idU == lengthU - 1:
            afterU = routeU.get_depot()
        else:
            afterU = tourU[idU+1]

        if idV == lengthV - 1:
            afterV = routeV.get_depot()
        else:
            afterV = tourV[idV+1]

        costU = costU - dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) - \
            dist.euclidianDistance(tourU[idU].get_x_coord(), tourU[idU].get_y_coord(), afterU.get_x_coord(), afterU.get_y_coord()) + \
            dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(
            ), afterU.get_x_coord(), afterU.get_y_coord())

        costV = costV - dist.euclidianDistance(tourV[idV].get_x_coord(), tourV[idV].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord()) +\
            dist.euclidianDistance(tourV[idV].get_x_coord(), tourV[idV].get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) + \
            dist.euclidianDistance(tourU[idU].get_x_coord(
            ), tourU[idU].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord())

        if costU + serviceU > routeU.get_depot().get_durationRoute():
            costTotalU += 1000
        if loadU > routeU.get_depot().get_loadVehicle():
            costTotalU += 1000
        if costV + serviceV > routeV.get_depot().get_durationRoute():
            costTotalV += 1000
        if loadV > routeV.get_depot().get_loadVehicle():
            costTotalV += 1000

        controlCostU = [costTotalU, costU, loadU, serviceU]
        controlCostV = [costTotalV, costV, loadV,
                        serviceV]  # [costTotal,cost,load,service]
        return controlCostU, controlCostV

    def costRemoveUinsertAfterVSameRoute(self, idU, idV, routeU):
        '''
        Método calcula o custo de remover u e inseri-lo após v
        '''
        costU = routeU.get_costWithoutPenalty()
        tourU = routeU.get_tour()
        lengthU = len(tourU)
        costTotalU = costU
        # print("len U: {}  idU: {}  idV: {}".format(lengthU, idU, idV))

        serviceU = routeU.get_totalService()
        loadU = routeU.get_totalDemand()

        if idU != 0:
            beforeU = tourU[idU-1]
        else:
            beforeU = routeU.get_depot()

        if idU == lengthU - 1:
            afterU = routeU.get_depot()
        else:
            afterU = tourU[idU+1]

        if idV == lengthU - 1:
            afterV = routeU.get_depot()
        else:
            afterV = tourU[idV+1]
        if (idV + 1) != idU:
            costU = costU - dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) - \
                dist.euclidianDistance(tourU[idU].get_x_coord(), tourU[idU].get_y_coord(), afterU.get_x_coord(), afterU.get_y_coord()) - \
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord()) + \
                dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), afterU.get_x_coord(), afterU.get_y_coord()) + \
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) + \
                dist.euclidianDistance(tourU[idU].get_x_coord(
                ), tourU[idU].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord())

        if costU + serviceU > routeU.get_depot().get_durationRoute():
            costTotalU += 1000
        if loadU > routeU.get_depot().get_loadVehicle():
            costTotalU += 1000

        # [costTotal,cost,load,service]
        controlCostU = [costTotalU, costU, loadU, serviceU]
        return controlCostU

    def costRemoveUXinsertAfterV(self, idU, idV, routeU, routeV):
        '''
        Método calcula o custo de remover u e x e inseri-los após v
        '''
        costU = routeU.get_costWithoutPenalty()
        tourU = routeU.get_tour()
        lengthU = len(tourU)
        costTotalU = costU

        costV = routeV.get_costWithoutPenalty()
        tourV = routeV.get_tour()
        lengthV = len(tourV)
        costTotalV = costV

        serviceU = routeU.get_totalService()
        loadU = routeU.get_totalDemand()

        serviceV = routeV.get_totalService()
        loadV = routeV.get_totalDemand()

        idX = idU + 1

        serviceU = serviceU - \
            tourU[idU].get_service() - tourU[idX].get_service()
        loadU = loadU - tourU[idU].get_demand() - tourU[idX].get_demand()

        serviceV = serviceV + \
            tourU[idU].get_service() + tourU[idX].get_service()
        loadV = loadV + tourU[idU].get_demand() + tourU[idX].get_demand()

        afterU = tourU[idX]
        if idU != 0:
            beforeU = tourU[idU-1]
        else:
            beforeU = routeU.get_depot()
        if idX < lengthU - 1:
            afterX = tourU[idX+1]
        else:
            afterX = routeU.get_depot()

        if idV == lengthV - 1:
            afterV = routeV.get_depot()
        else:
            afterV = tourV[idV+1]

        costU = costU - dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) - \
            dist.euclidianDistance(tourU[idU].get_x_coord(), tourU[idU].get_y_coord(), afterU.get_x_coord(), afterU.get_y_coord()) - \
            dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) + \
            dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(
            ), afterX.get_x_coord(), afterX.get_y_coord())

        costV = costV - dist.euclidianDistance(tourV[idV].get_x_coord(), tourV[idV].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord()) +\
            dist.euclidianDistance(tourV[idV].get_x_coord(), tourV[idV].get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) + \
            dist.euclidianDistance(tourU[idU].get_x_coord(), tourU[idU].get_y_coord(), tourU[idX].get_x_coord(), tourU[idX].get_y_coord()) + \
            dist.euclidianDistance(tourU[idX].get_x_coord(
            ), tourU[idX].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord())

        if costU + serviceU > routeU.get_depot().get_durationRoute():
            costTotalU += 1000
        if loadU > routeU.get_depot().get_loadVehicle():
            costTotalU += 1000
        if costV + serviceV > routeV.get_depot().get_durationRoute():
            costTotalV += 1000
        if loadV > routeV.get_depot().get_loadVehicle():
            costTotalV += 1000

        controlCostU = [costTotalU, costU, loadU, serviceU]
        controlCostV = [costTotalV, costV, loadV,
                        serviceV]  # [costTotal,cost,load,service]
        return controlCostU, controlCostV

    def costRemoveUXinsertAfterVSameRoute(self, idU, idV, routeU):
        '''
        Método calcula o custo de remover u e x e inseri-los após v
        '''
        costU = routeU.get_costWithoutPenalty()
        tourU = routeU.get_tour()
        lengthU = len(tourU)
        costTotalU = costU

        serviceU = routeU.get_totalService()
        loadU = routeU.get_totalDemand()

        idX = idU + 1

        if idU != 0:
            beforeU = tourU[idU-1]
        else:
            beforeU = routeU.get_depot()
        if idX < lengthU - 1:
            afterX = tourU[idX+1]
        else:
            afterX = routeU.get_depot()

        if idV == lengthU - 1:
            afterV = routeU.get_depot()
        else:
            afterV = tourU[idV+1]

        if idV != (idU - 1):
            costU = costU - dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) - \
                dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) - \
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord()) + \
                dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) + \
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) + \
                dist.euclidianDistance(tourU[idX].get_x_coord(
                ), tourU[idX].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord())

        if costU + serviceU > routeU.get_depot().get_durationRoute():
            costTotalU += 1000
        if loadU > routeU.get_depot().get_loadVehicle():
            costTotalU += 1000

        # [costTotal,cost,load,service]
        controlCostU = [costTotalU, costU, loadU, serviceU]
        return controlCostU

    def costRemoveUXinsertXUAfterV(self, idU, idV, routeU, routeV):
        '''
        Método calcula o custo de remover u e x e inserir XU após v
        '''
        costU = routeU.get_costWithoutPenalty()
        tourU = routeU.get_tour()
        lengthU = len(tourU)
        costTotalU = costU

        costV = routeV.get_costWithoutPenalty()
        tourV = routeV.get_tour()
        lengthV = len(tourV)
        costTotalV = costV

        serviceU = routeU.get_totalService()
        loadU = routeU.get_totalDemand()

        serviceV = routeV.get_totalService()
        loadV = routeV.get_totalDemand()

        idX = idU + 1

        serviceU = serviceU - \
            tourU[idU].get_service() - tourU[idX].get_service()
        loadU = loadU - tourU[idU].get_demand() - tourU[idX].get_demand()

        serviceV = serviceV + \
            tourU[idU].get_service() + tourU[idX].get_service()
        loadV = loadV + tourU[idU].get_demand() + tourU[idX].get_demand()

        afterU = tourU[idX]
        if idU != 0:
            beforeU = tourU[idU-1]
        else:
            beforeU = routeU.get_depot()
        if idX < lengthU - 1:
            afterX = tourU[idX+1]
        else:
            afterX = routeU.get_depot()

        if idV == lengthV - 1:
            afterV = routeV.get_depot()
        else:
            afterV = tourV[idV+1]

        costU = costU - dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) - \
            dist.euclidianDistance(tourU[idU].get_x_coord(), tourU[idU].get_y_coord(), afterU.get_x_coord(), afterU.get_y_coord()) - \
            dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) + \
            dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(
            ), afterX.get_x_coord(), afterX.get_y_coord())

        costV = costV - dist.euclidianDistance(tourV[idV].get_x_coord(), tourV[idV].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord()) +\
            dist.euclidianDistance(tourV[idV].get_x_coord(), tourV[idV].get_y_coord(), tourU[idX].get_x_coord(), tourU[idX].get_y_coord()) + \
            dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) + \
            dist.euclidianDistance(tourU[idU].get_x_coord(
            ), tourU[idU].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord())

        if costU + serviceU > routeU.get_depot().get_durationRoute():
            costTotalU += 1000
        if loadU > routeU.get_depot().get_loadVehicle():
            costTotalU += 1000
        if costV + serviceV > routeV.get_depot().get_durationRoute():
            costTotalV += 1000
        if loadV > routeV.get_depot().get_loadVehicle():
            costTotalV += 1000

        controlCostU = [costTotalU, costU, loadU, serviceU]
        controlCostV = [costTotalV, costV, loadV,
                        serviceV]  # [costTotal,cost,load,service]
        return controlCostU, controlCostV

    def costRemoveUXinsertXUAfterVSameRoute(self, idU, idV, routeU):
        '''
        Método calcula o custo de remover u e x e inserir XU após v
        '''
        costU = routeU.get_costWithoutPenalty()
        tourU = routeU.get_tour()
        lengthU = len(tourU)
        costTotalU = costU

        serviceU = routeU.get_totalService()
        loadU = routeU.get_totalDemand()

        idX = idU + 1

        if idU != 0:
            beforeU = tourU[idU-1]
        else:
            beforeU = routeU.get_depot()
        if idX < lengthU - 1:
            afterX = tourU[idX+1]
        else:
            afterX = routeU.get_depot()

        if idV == lengthU - 1:
            afterV = routeU.get_depot()
        else:
            afterV = tourU[idV+1]

        if idV != (idU - 1):
            costU = costU - dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) - \
                dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) - \
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord()) + \
                dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) + \
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), tourU[idX].get_x_coord(), tourU[idX].get_y_coord()) + \
                dist.euclidianDistance(tourU[idU].get_x_coord(
                ), tourU[idU].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord())

        if costU + serviceU > routeU.get_depot().get_durationRoute():
            costTotalU += 1000
        if loadU > routeU.get_depot().get_loadVehicle():
            costTotalU += 1000

        # [costTotal,cost,load,service]
        controlCostU = [costTotalU, costU, loadU, serviceU]
        return controlCostU

    def costShiftUXwithVY(self, idU, idV, routeU, routeV):
        '''
        Método calcula o custo de trocar os elementos U e X com V e Y
        '''
        costU = routeU.get_costWithoutPenalty()
        tourU = routeU.get_tour()
        lengthU = len(tourU)
        costTotalU = costU

        costV = routeV.get_costWithoutPenalty()
        tourV = routeV.get_tour()
        lengthV = len(tourV)
        costTotalV = costV

        serviceU = routeU.get_totalService()
        loadU = routeU.get_totalDemand()

        serviceV = routeV.get_totalService()
        loadV = routeV.get_totalDemand()

        idX = idU + 1
        idY = idV + 1

        serviceU = serviceU - tourU[idU].get_service(
        ) - tourU[idX].get_service() + tourV[idV].get_service() + tourV[idY].get_service()
        loadU = loadU - tourU[idU].get_demand(
        ) - tourU[idX].get_demand() + tourV[idV].get_demand() + tourV[idY].get_demand()

        serviceV = serviceV - tourV[idV].get_service(
        ) - tourV[idY].get_service() + tourU[idU].get_service() + tourU[idX].get_service()
        loadV = loadV - tourV[idV].get_demand(
        ) - tourV[idY].get_demand() + tourU[idU].get_demand() + tourU[idX].get_demand()

        afterU = tourU[idX]
        if idU != 0 and idX < lengthU - 1:
            beforeU = tourU[idU-1]
            afterX = tourU[idX+1]
        elif idU == 0 and idX == lengthU - 1:
            beforeU = routeU.get_depot()
            afterX = routeU.get_depot()
        elif idU != 0 and idX == lengthU - 1:
            beforeU = tourU[idU-1]
            afterX = routeU.get_depot()
        elif idU == 0 and idX < lengthU - 1:
            beforeU = routeU.get_depot()
            afterX = tourU[idX+1]

        costU = costU - dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) - \
            dist.euclidianDistance(tourU[idU].get_x_coord(), tourU[idU].get_y_coord(), afterU.get_x_coord(), afterU.get_y_coord()) - \
            dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) + \
            dist.euclidianDistance(tourV[idV].get_x_coord(), tourV[idV].get_y_coord(), tourV[idY].get_x_coord(), tourV[idY].get_y_coord()) + \
            dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourV[idV].get_x_coord(), tourV[idV].get_y_coord()) + \
            dist.euclidianDistance(tourV[idY].get_x_coord(
            ), tourV[idY].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord())

        afterV = tourV[idY]
        if idV != 0 and idY < lengthV - 1:
            beforeV = tourV[idV-1]
            afterY = tourV[idY+1]
        elif idV == 0 and idY == lengthV - 1:
            beforeV = routeV.get_depot()
            afterY = routeV.get_depot()
        elif idV != 0 and idY == lengthV - 1:
            beforeV = tourV[idV-1]
            afterY = routeV.get_depot()
        elif idV == 0 and idY < lengthV - 1:
            beforeV = routeV.get_depot()
            afterY = tourV[idY+1]

        costV = costV - dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourV[idV].get_x_coord(), tourV[idV].get_y_coord()) - \
            dist.euclidianDistance(tourV[idV].get_x_coord(), tourV[idV].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord()) - \
            dist.euclidianDistance(tourV[idY].get_x_coord(), tourV[idY].get_y_coord(), afterY.get_x_coord(), afterY.get_y_coord()) + \
            dist.euclidianDistance(tourU[idU].get_x_coord(), tourU[idU].get_y_coord(), tourU[idX].get_x_coord(), tourU[idX].get_y_coord()) + \
            dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) + \
            dist.euclidianDistance(tourU[idX].get_x_coord(
            ), tourU[idX].get_y_coord(), afterY.get_x_coord(), afterY.get_y_coord())

        if costU + serviceU > routeU.get_depot().get_durationRoute():
            costTotalU += 1000
        if loadU > routeU.get_depot().get_loadVehicle():
            costTotalU += 1000
        if costV + serviceV > routeV.get_depot().get_durationRoute():
            costTotalV += 1000
        if loadV > routeV.get_depot().get_loadVehicle():
            costTotalV += 1000

        controlCostU = [costTotalU, costU, loadU, serviceU]
        controlCostV = [costTotalV, costV, loadV,
                        serviceV]  # [costTotal,cost,load,service]
        return controlCostU, controlCostV

    def costShiftUXwithVYsameRoute(self, idU, idV, routeU):
        '''
        Método calcula o custo de trocar os elementos U e X com V e Y
        '''
        costU = routeU.get_costWithoutPenalty()
        tourU = routeU.get_tour()
        lengthU = len(tourU)
        costTotalU = costU

        serviceU = routeU.get_totalService()
        loadU = routeU.get_totalDemand()

        idX = idU + 1
        idY = idV + 1

        if idU != 0:
            beforeU = tourU[idU-1]
        else:
            beforeU = routeU.get_depot()
        if idX < lengthU - 1:
            afterX = tourU[idX+1]
        else:
            afterX = routeU.get_depot()

        if idV != 0:
            beforeV = tourU[idV-1]
        else:
            beforeV = routeU.get_depot()
        if idY < lengthU - 1:
            afterY = tourU[idY+1]
        else:
            afterY = routeU.get_depot()

        if idX+1 == idV:
            costU = costU - dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) - \
                dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) - \
                dist.euclidianDistance(tourU[idY].get_x_coord(), tourU[idY].get_y_coord(), afterY.get_x_coord(), afterY.get_y_coord()) + \
                dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idV].get_x_coord(), tourU[idV].get_y_coord()) + \
                dist.euclidianDistance(tourU[idY].get_x_coord(), tourU[idY].get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) + \
                dist.euclidianDistance(tourU[idX].get_x_coord(
                ), tourU[idX].get_y_coord(), afterY.get_x_coord(), afterY.get_y_coord())

        elif idY+1 == idU:
            costU = costU - dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) - \
                dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) - \
                dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourU[idV].get_x_coord(), tourU[idV].get_y_coord()) + \
                dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) + \
                dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), tourU[idV].get_x_coord(), tourU[idV].get_y_coord()) + \
                dist.euclidianDistance(tourU[idY].get_x_coord(
                ), tourU[idY].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord())

        else:
            costU = costU - dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) - \
                dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) - \
                dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourU[idV].get_x_coord(), tourU[idV].get_y_coord()) - \
                dist.euclidianDistance(tourU[idY].get_x_coord(), tourU[idY].get_y_coord(), afterY.get_x_coord(), afterY.get_y_coord()) + \
                dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idV].get_x_coord(), tourU[idV].get_y_coord()) + \
                dist.euclidianDistance(tourU[idY].get_x_coord(), tourU[idY].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) + \
                dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) + \
                dist.euclidianDistance(tourU[idX].get_x_coord(
                ), tourU[idX].get_y_coord(), afterY.get_x_coord(), afterY.get_y_coord())

        if costU + serviceU > routeU.get_depot().get_durationRoute():
            costTotalU += 1000
        if loadU > routeU.get_depot().get_loadVehicle():
            costTotalU += 1000

        # [costTotal,cost,load,service]
        controlCostU = [costTotalU, costU, loadU, serviceU]
        return controlCostU

    def costShiftUXVYwithUVXY(self, idU, idV, routeU, routeV):
        '''
        Método calcula custo ao trocar x por v
        '''
        costU = routeU.get_costWithoutPenalty()
        tourU = routeU.get_tour()
        lengthU = len(tourU)
        costTotalU = costU

        costV = routeV.get_costWithoutPenalty()
        tourV = routeV.get_tour()
        costTotalV = costV

        serviceU = routeU.get_totalService()
        loadU = routeU.get_totalDemand()

        serviceV = routeV.get_totalService()
        loadV = routeV.get_totalDemand()

        idX = idU + 1
        idY = idV + 1

        serviceU = serviceU - tourU[idX].get_service(
        ) + tourV[idV].get_service()
        loadU = loadU - tourU[idX].get_demand() + tourV[idV].get_demand()

        serviceV = serviceV - tourV[idV].get_service(
        ) + tourU[idX].get_service()
        loadV = loadV - tourV[idV].get_demand(
        ) + tourU[idX].get_demand()

        beforeX = tourU[idU]
        if idX == lengthU-1:
            afterX = routeU.get_depot()
        else:
            afterX = tourU[idX+1]

        costU = costU - dist.euclidianDistance(beforeX.get_x_coord(), beforeX.get_y_coord(), tourU[idX].get_x_coord(), tourU[idX].get_y_coord()) - \
            dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) + \
            dist.euclidianDistance(beforeX.get_x_coord(), beforeX.get_y_coord(), tourV[idV].get_x_coord(), tourV[idV].get_y_coord()) + \
            dist.euclidianDistance(tourV[idV].get_x_coord(
            ), tourV[idV].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord())

        if costU + serviceU > routeU.get_depot().get_durationRoute():
            costTotalU += 1000
        if loadU > routeU.get_depot().get_loadVehicle():
            costTotalU += 1000

        if idV == 0:
            beforeV = routeV.get_depot()
        else:
            beforeV = tourV[idV-1]

        costV = costV - dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourV[idV].get_x_coord(), tourV[idV].get_y_coord()) - \
            dist.euclidianDistance(tourV[idV].get_x_coord(), tourV[idV].get_y_coord(), tourV[idY].get_x_coord(), tourV[idY].get_y_coord()) + \
            dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourU[idX].get_x_coord(), tourU[idX].get_y_coord()) + \
            dist.euclidianDistance(tourU[idX].get_x_coord(
            ), tourU[idX].get_y_coord(), tourV[idY].get_x_coord(), tourV[idY].get_y_coord())

        if costU + serviceU > routeU.get_depot().get_durationRoute():
            costTotalU += 1000
        if loadU > routeU.get_depot().get_loadVehicle():
            costTotalU += 1000
        if costV + serviceV > routeV.get_depot().get_durationRoute():
            costTotalV += 1000
        if loadV > routeV.get_depot().get_loadVehicle():
            costTotalV += 1000

        controlCostU = [costTotalU, costU, loadU, serviceU]
        controlCostV = [costTotalV, costV, loadV,
                        serviceV]  # [costTotal,cost,load,service]
        return controlCostU, controlCostV

    def costShiftUXVYwithUVXYSameRoute(self, idU, idV, routeU):
        '''
        Método calcula custo ao trocar x por v
        '''
        costU = routeU.get_costWithoutPenalty()
        tourU = routeU.get_tour()
        lengthU = len(tourU)
        costTotalU = tourU

        serviceU = routeU.get_totalService()
        loadU = routeU.get_totalDemand()

        idX = idU + 1

        beforeX = tourU[idU]
        if idX == lengthU - 1:
            afterX = routeU.get_depot()
        else:
            afterX = tourU[idX+1]

        afterV = tourU[idV+1]
        if idV == 0:
            beforeV = routeU.get_depot()
        else:
            beforeV = tourU[idV-1]

        if idX == idV - 1:
            costU = costU - dist.euclidianDistance(beforeX.get_x_coord(), beforeX.get_y_coord(), tourU[idX].get_x_coord(), tourU[idX].get_y_coord()) - \
                dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) -\
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord()) + \
                dist.euclidianDistance(beforeX.get_x_coord(), beforeX.get_y_coord(), tourU[idV].get_x_coord(), tourU[idV].get_y_coord()) + \
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), tourU[idX].get_x_coord(), tourU[idX].get_y_coord()) + \
                dist.euclidianDistance(tourU[idX].get_x_coord(
                ), tourU[idX].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord())

        else:
            costU = costU - dist.euclidianDistance(beforeX.get_x_coord(), beforeX.get_y_coord(), tourU[idX].get_x_coord(), tourU[idX].get_y_coord()) - \
                dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) -\
                dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourU[idV].get_x_coord(), tourU[idV].get_y_coord()) -\
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord()) + \
                dist.euclidianDistance(beforeX.get_x_coord(), beforeX.get_y_coord(), tourU[idV].get_x_coord(), tourU[idV].get_y_coord()) + \
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) + \
                dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourU[idX].get_x_coord(), tourU[idX].get_y_coord()) + \
                dist.euclidianDistance(tourU[idX].get_x_coord(
                ), tourU[idX].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord())

        costTotalU = costU

        if costU + serviceU > routeU.get_depot().get_durationRoute():
            costTotalU += 1000
        if loadU > routeU.get_depot().get_loadVehicle():
            costTotalU += 1000
        controlCostU = [costTotalU, costU, loadU,
                        serviceU]  # [costTotal,cost,load,service]
        return controlCostU

    def costShiftUXVYwithUYXV(self, idU, idV, routeU, routeV):
        '''
        Método troca x por y, v por x e y por v
        '''
        costU = routeU.get_costWithoutPenalty()
        tourU = routeU.get_tour()
        lengthU = len(tourU)
        costTotalU = costU

        costV = routeV.get_costWithoutPenalty()
        tourV = routeV.get_tour()
        lengthV = len(tourV)
        costTotalV = costV

        serviceU = routeU.get_totalService()
        loadU = routeU.get_totalDemand()

        serviceV = routeV.get_totalService()
        loadV = routeV.get_totalDemand()

        idX = idU + 1
        idY = idV + 1

        serviceU = serviceU - \
            tourU[idX].get_service() + tourV[idY].get_service()
        loadU = loadU - tourU[idX].get_demand() + tourV[idY].get_demand()

        serviceV = serviceV - \
            tourV[idY].get_service() + tourU[idX].get_service()
        loadV = loadV - tourV[idY].get_demand() + tourU[idX].get_demand()

        beforeX = tourU[idU]
        if idX == lengthU - 1:
            afterX = routeU.get_depot()
        else:
            afterX = tourU[idX+1]

        afterV = tourV[idY]
        if idV == 0:
            beforeV = routeV.get_depot()
        else:
            beforeV = tourV[idV-1]

        if idY == lengthV - 1:
            afterY = routeV.get_depot()
        else:
            afterY = tourV[idY+1]

        costU = costU - dist.euclidianDistance(beforeX.get_x_coord(), beforeX.get_y_coord(), tourU[idX].get_x_coord(), tourU[idX].get_y_coord()) - \
            dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) + \
            dist.euclidianDistance(beforeX.get_x_coord(), beforeX.get_y_coord(), tourV[idY].get_x_coord(), tourV[idY].get_y_coord()) + \
            dist.euclidianDistance(tourV[idY].get_x_coord(
            ), tourV[idY].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord())

        costV = costV - dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourV[idV].get_x_coord(), tourV[idV].get_y_coord()) - \
            dist.euclidianDistance(tourV[idV].get_x_coord(), tourV[idV].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord()) - \
            dist.euclidianDistance(tourV[idY].get_x_coord(), tourV[idY].get_y_coord(), afterY.get_x_coord(), afterY.get_y_coord()) + \
            dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourU[idX].get_x_coord(), tourU[idX].get_y_coord()) + \
            dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), tourV[idV].get_x_coord(), tourV[idV].get_y_coord()) + \
            dist.euclidianDistance(tourV[idV].get_x_coord(
            ), tourV[idV].get_y_coord(), afterY.get_x_coord(), afterY.get_y_coord())

        if costU + serviceU > routeU.get_depot().get_durationRoute():
            costTotalU += 1000
        if loadU > routeU.get_depot().get_loadVehicle():
            costTotalU += 1000
        if costV + serviceV > routeV.get_depot().get_durationRoute():
            costTotalV += 1000
        if loadV > routeV.get_depot().get_loadVehicle():
            costTotalV += 1000

        controlCostU = [costTotalU, costU, loadU, serviceU]
        controlCostV = [costTotalV, costV, loadV,
                        serviceV]  # [costTotal,cost,load,service]
        return controlCostU, controlCostV

    def costShiftUXVYwithUYXVSameRoute(self, idU, idV, routeU):
        '''
        Método troca x por y, v por x e y por v
        '''
        costU = routeU.get_costWithoutPenalty()
        tourU = routeU.get_tour()
        lengthU = len(tourU)
        costTotalU = costU

        serviceU = routeU.get_totalService()
        loadU = routeU.get_totalDemand()

        idX = idU + 1
        idY = idV + 1

        beforeX = tourU[idU]
        if idX == lengthU - 1:
            afterX = routeU.get_depot()
        else:
            afterX = tourU[idX+1]

        afterV = tourU[idY]
        if idV == 0:
            beforeV = routeU.get_depot()
        else:
            beforeV = tourU[idV-1]

        if idY == lengthU - 1:
            afterY = routeU.get_depot()
        else:
            afterY = tourU[idY+1]

        if idV == idX+1:
            costU = costU - dist.euclidianDistance(beforeX.get_x_coord(), beforeX.get_y_coord(), tourU[idX].get_x_coord(), tourU[idX].get_y_coord()) - \
                dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) - \
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord()) - \
                dist.euclidianDistance(tourU[idY].get_x_coord(), tourU[idY].get_y_coord(), afterY.get_x_coord(), afterY.get_y_coord()) + \
                dist.euclidianDistance(beforeX.get_x_coord(), beforeX.get_y_coord(), tourU[idY].get_x_coord(), tourU[idY].get_y_coord()) + \
                dist.euclidianDistance(tourU[idY].get_x_coord(), tourU[idY].get_y_coord(), tourU[idX].get_x_coord(), tourU[idX].get_y_coord()) + \
                dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), tourU[idV].get_x_coord(), tourU[idV].get_y_coord()) + \
                dist.euclidianDistance(tourU[idV].get_x_coord(
                ), tourU[idV].get_y_coord(), afterY.get_x_coord(), afterY.get_y_coord())
        else:
            costU = costU - dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourU[idV].get_x_coord(), tourU[idV].get_y_coord()) - \
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord()) - \
                dist.euclidianDistance(tourU[idY].get_x_coord(), tourU[idY].get_y_coord(), afterY.get_x_coord(), afterY.get_y_coord()) - \
                dist.euclidianDistance(beforeX.get_x_coord(), beforeX.get_y_coord(), tourU[idX].get_x_coord(), tourU[idX].get_y_coord()) - \
                dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) + \
                dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourU[idX].get_x_coord(), tourU[idX].get_y_coord()) + \
                dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), tourU[idV].get_x_coord(), tourU[idV].get_y_coord()) + \
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), afterY.get_x_coord(), afterY.get_y_coord()) + \
                dist.euclidianDistance(beforeX.get_x_coord(), beforeX.get_y_coord(), tourU[idY].get_x_coord(), tourU[idY].get_y_coord()) + \
                dist.euclidianDistance(tourU[idY].get_x_coord(
                ), tourU[idY].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord())

        if costU + serviceU > routeU.get_depot().get_durationRoute():
            costTotalU += 1000
        if loadU > routeU.get_depot().get_loadVehicle():
            costTotalU += 1000

        # [costTotal,cost,load,service]
        controlCostU = [costTotalU, costU, loadU, serviceU]
        return controlCostU

    def costShiftUXwithV(self, idU, idV, routeU, routeV):
        '''
        Método calcula custo ao trocar u por v e inserir x após v
        '''
        costU = routeU.get_costWithoutPenalty()
        tourU = routeU.get_tour()
        lengthU = len(tourU)
        costTotalU = costU

        costV = routeV.get_costWithoutPenalty()
        tourV = routeV.get_tour()
        lengthV = len(tourV)
        costTotalV = costV

        serviceU = routeU.get_totalService()
        loadU = routeU.get_totalDemand()

        serviceV = routeV.get_totalService()
        loadV = routeV.get_totalDemand()

        idX = idU + 1

        serviceU = serviceU - \
            tourU[idU].get_service() - tourU[idX].get_service() + \
            tourV[idV].get_service()
        loadU = loadU - tourU[idU].get_demand() - \
            tourU[idX].get_demand() + tourV[idV].get_demand()

        serviceV = serviceV - \
            tourV[idV].get_service() + tourU[idU].get_service() + \
            tourU[idX].get_service()
        loadV = loadV - tourV[idV].get_demand() + \
            tourU[idU].get_demand() + tourU[idX].get_demand()

        if idU == 0:
            beforeU = routeU.get_depot()
        else:
            beforeU = tourU[idU-1]

        if idX == lengthU - 1:
            afterX = routeU.get_depot()
        else:
            afterX = tourU[idX+1]

        if idV == 0:
            beforeV = routeV.get_depot()
        else:
            beforeV = tourV[idV-1]

        if idV == lengthV - 1:
            afterV = routeV.get_depot()
        else:
            afterV = tourV[idV+1]

        costU = costU - dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) - \
            dist.euclidianDistance(tourU[idU].get_x_coord(), tourU[idU].get_y_coord(), tourU[idX].get_x_coord(), tourU[idX].get_y_coord()) - \
            dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) + \
            dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourV[idV].get_x_coord(), tourV[idV].get_y_coord()) + \
            dist.euclidianDistance(tourV[idV].get_x_coord(
            ), tourV[idV].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord())

        costV = costV - dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourV[idV].get_x_coord(), tourV[idV].get_y_coord()) - \
            dist.euclidianDistance(tourV[idV].get_x_coord(), tourV[idV].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord()) + \
            dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) + \
            dist.euclidianDistance(tourU[idU].get_x_coord(), tourU[idU].get_y_coord(), tourU[idX].get_x_coord(), tourU[idX].get_y_coord()) + \
            dist.euclidianDistance(tourU[idX].get_x_coord(
            ), tourU[idX].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord())

        if costU + serviceU > routeU.get_depot().get_durationRoute():
            costTotalU += 1000
        if loadU > routeU.get_depot().get_loadVehicle():
            costTotalU += 1000
        if costV + serviceV > routeV.get_depot().get_durationRoute():
            costTotalV += 1000
        if loadV > routeV.get_depot().get_loadVehicle():
            costTotalV += 1000

        controlCostU = [costTotalU, costU, loadU, serviceU]
        controlCostV = [costTotalV, costV, loadV,
                        serviceV]  # [costTotal,cost,load,service]
        return controlCostU, controlCostV

    def costShiftUXwithVsameRoute(self, idU, idV, routeU):
        '''
        Método calcula custo ao trocar u por v e inserir x após v
        '''
        costU = routeU.get_costWithoutPenalty()
        tourU = routeU.get_tour()
        lengthU = len(tourU)
        costTotalU = costU

        serviceU = routeU.get_totalService()
        loadU = routeU.get_totalDemand()

        idX = idU + 1

        if idU == 0:
            beforeU = routeU.get_depot()
        else:
            beforeU = tourU[idU-1]

        if idX == lengthU - 1:
            afterX = routeU.get_depot()
        else:
            afterX = tourU[idX+1]

        if idV == 0:
            beforeV = routeU.get_depot()
        else:
            beforeV = tourU[idV-1]

        if idV == lengthU - 1:
            afterV = routeU.get_depot()
        else:
            afterV = tourU[idV+1]

        if idX + 1 == idV:
            costU = costU - dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) - \
                dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) - \
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord()) + \
                dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idV].get_x_coord(), tourU[idV].get_y_coord()) + \
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) + \
                dist.euclidianDistance(tourU[idX].get_x_coord(
                ), tourU[idX].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord())
        elif idV + 1 == idU:
            costU = costU - dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourU[idV].get_x_coord(), tourU[idV].get_y_coord()) - \
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) - \
                dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) + \
                dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) + \
                dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), tourU[idV].get_x_coord(), tourU[idV].get_y_coord()) + \
                dist.euclidianDistance(tourU[idV].get_x_coord(
                ), tourU[idV].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord())
        else:
            costU = costU - dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) - \
                dist.euclidianDistance(tourU[idX].get_x_coord(), tourU[idX].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) - \
                dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourU[idV].get_x_coord(), tourU[idV].get_y_coord()) - \
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord()) + \
                dist.euclidianDistance(beforeU.get_x_coord(), beforeU.get_y_coord(), tourU[idV].get_x_coord(), tourU[idV].get_y_coord()) + \
                dist.euclidianDistance(tourU[idV].get_x_coord(), tourU[idV].get_y_coord(), afterX.get_x_coord(), afterX.get_y_coord()) + \
                dist.euclidianDistance(beforeV.get_x_coord(), beforeV.get_y_coord(), tourU[idU].get_x_coord(), tourU[idU].get_y_coord()) + \
                dist.euclidianDistance(tourU[idX].get_x_coord(
                ), tourU[idX].get_y_coord(), afterV.get_x_coord(), afterV.get_y_coord())

        if costU + serviceU > routeU.get_depot().get_durationRoute():
            costTotalU += 1000
        if loadU > routeU.get_depot().get_loadVehicle():
            costTotalU += 1000

        # [costTotal,cost,load,service]
        controlCostU = [costTotalU, costU, loadU, serviceU]
        return controlCostU

    '''
    Método calcula custo ao trocar um ou mais nós da rota (será retirado elementos da listOld (consecutivos) e acrescentados elementos da listNew na mesma posição)
    @param lista de índices de clientes a serem substituídos
    @param lista de clientes substitutos
    @param rota
    @return [costTotal,cost,load,service]
    '''

    def costShiftNodes(self, listIdOld, listNew, route):
        # print(route)
        # print(listIdOld)
        # print(listNew)
        controlCost = []  # [costTotal,cost,load,service]
        auxiliarRoute = copy.deepcopy(route)
        # atualizar custo sem os individuos
        for i in range(len(listIdOld)):
            controlCost = auxiliarRoute.costWithoutNode(listIdOld[0])
            auxiliarRoute.popCustomer(listIdOld[0])
            auxiliarRoute.set_cost(
                controlCost[1], controlCost[2], controlCost[3])
            # print("auxiliarRoute")
            # print(auxiliarRoute)
        # calcular custo com os novos individuos
        i = listIdOld[0]
        for new in listNew:
            controlCost = auxiliarRoute.costWithNode(new, i)
            auxiliarRoute.insertCustomer(new, i)
            auxiliarRoute.set_cost(
                controlCost[1], controlCost[2], controlCost[3])
            i += 1
        del auxiliarRoute
        return controlCost

    '''
    Método calcula custo ao trocar um ou mais nós de uma mesma rota (será trocado elementos da listIdSwap1 (consecutivos) pelos da listIdSwap2)
    @param lista de índices de clientes 1
    @param lista de índices de clientes 2
    @param rota
    @return [custo total,rota]
    '''

    def costShiftNodesSameRoute(self, listIdSwap1, listIdSwap2, route):
        # print("listIdSwap1")
        # print(str(listIdSwap1))
        # print("listIdSwap2")
        # print(str(listIdSwap2))
        auxiliarRoute = copy.deepcopy(route)
        a = listIdSwap1
        b = listIdSwap2
        if listIdSwap1[0] > listIdSwap2[0]:
            a = listIdSwap2
            b = listIdSwap1

        aux = Customer()
        aux.set_id(-1)
        for i in a:
            auxiliarRoute.changeCustomer(aux, i)
        for i in b:
            auxiliarRoute.changeCustomer(aux, i)
        j = b[0]
        for i in a:
            auxiliarRoute.insertCustomer(route.get_tour()[i], j)
            j += 1
        j = a[0]
        for i in b:
            auxiliarRoute.insertCustomer(route.get_tour()[i], j)
            j += 1

        # remover -1
        while aux in auxiliarRoute.get_tour():
            auxiliarRoute.removeCustomer(aux)

        auxiliarRoute.startValues()
        auxiliarRoute.calculeCost()
        # print("auxiliar route")
        # print(auxiliarRoute)
        return [auxiliarRoute.get_totalCost(), auxiliarRoute]

    '''
    Método substitui dois pares por outros dois
    @param rota que sofrerá as mudanças
    @param lista1 de índices de clientes que serão substituídos (clientes consecutivos)
    @param replaceWith1 lista de clientes substitutos de lista1
    @param opcional lista2 de índices de clientes que serão substituídos (clientes consecutivos)
    @param opcional replaceWith2 lista de clientes substitutos de lista2
    @return [custo total,rota]
    '''

    def costReplaceNodes(self, route, old1, replaceWith1, old2=[], replaceWith2=[]):
        auxiliarRoute = copy.deepcopy(route)
        a = old1
        b = old2

        j = 0
        # trocando os pares
        for i in a:
            repl = replaceWith1[j]
            auxiliarRoute.changeCustomer(repl, i)
            j += 1
        if len(old2) > 0 and len(replaceWith2) > 0:
            j = 0
            for i in b:
                repl = replaceWith2[j]
                auxiliarRoute.changeCustomer(repl, i)
                j += 1

        auxiliarRoute.startValues()
        auxiliarRoute.calculeCost()
        return [auxiliarRoute.get_totalCost(), auxiliarRoute]

    '''
    Método calcula custo ao adicionar um nó a mais na rota
    @param customer, índice de inserção
    @return lista [custo com penalização, custo sem penalização, carregamento total, serviço total]
    '''

    def costWithNode(self, customer, index):
        cost = 0.0
        load = self._totalDemand + customer.get_demand()
        service = self._totalService + customer.get_service()
        length = len(self._tour)

        if length == 0:  # lista vazia:
            cost = 2 * dist.euclidianDistance(self._depot.get_x_coord(
            ), self._depot.get_y_coord(), customer.get_x_coord(), customer.get_y_coord())
            load = customer.get_demand()
            service = customer.get_service()
        # verificar se ele ligará ao depósito
        elif index == 0:
            cost = self._cost - dist.euclidianDistance(self._depot.get_x_coord(), self._depot.get_y_coord(), self._tour[0].get_x_coord(), self._tour[0].get_y_coord()) + \
                dist.euclidianDistance(self._depot.get_x_coord(), self._depot.get_y_coord(), customer.get_x_coord(), customer.get_y_coord()) + \
                dist.euclidianDistance(customer.get_x_coord(), customer.get_y_coord(
                ), self._tour[0].get_x_coord(), self._tour[0].get_y_coord())
        elif index == length:
            cost = self._cost - dist.euclidianDistance(self._depot.get_x_coord(), self._depot.get_y_coord(), self._tour[length-1].get_x_coord(), self._tour[length-1].get_y_coord()) + \
                dist.euclidianDistance(self._tour[length-1].get_x_coord(), self._tour[length-1].get_y_coord(), customer.get_x_coord(), customer.get_y_coord()) + \
                dist.euclidianDistance(self._depot.get_x_coord(), self._depot.get_y_coord(
                ), customer.get_x_coord(), customer.get_y_coord())

        # está entre dois clientes
        else:
            cost = self._cost - dist.euclidianDistance(self._tour[index-1].get_x_coord(), self._tour[index-1].get_y_coord(), self._tour[index].get_x_coord(), self._tour[index].get_y_coord()) + \
                dist.euclidianDistance(self._tour[index-1].get_x_coord(), self._tour[index-1].get_y_coord(), customer.get_x_coord(), customer.get_y_coord()) + \
                dist.euclidianDistance(customer.get_x_coord(), customer.get_y_coord(
                ), self._tour[index].get_x_coord(), self._tour[index].get_y_coord())

        # verificar se há penalizações
        costTotal = cost
        if load > self._depot.get_loadVehicle():
            costTotal += 1000 * (load - self._depot.get_loadVehicle())
        if cost + service > self._depot.get_durationRoute():
            costTotal += 1000 * abs(service + cost -
                                    self._depot.get_durationRoute())

        return [costTotal, cost, load, service]

    '''
    Método calcula custo ao adicionar dois nós consecutivos a mais na rota
    @param customer1, customer2, índice de inserção
    @return lista [custo com penalização, custo sem penalização, carregamento total, duração total]
    '''

    def costWith2Nodes(self, customer1, customer2, index):
        cost = 0.0
        load = self._totalDemand + customer1.get_demand() + customer2.get_demand()
        service = self._totalService + customer1.get_service() + customer2.get_service()
        length = len(self._tour)

        # verificar se ele ligará ao depósito
        if length == 0:  # lista vazia:
            cost = dist.euclidianDistance(self._depot.get_x_coord(), self._depot.get_y_coord(), customer1.get_x_coord(), customer1.get_y_coord()) + \
                dist.euclidianDistance(customer1.get_x_coord(), customer1.get_y_coord(), customer2.get_x_coord(), customer2.get_y_coord()) + \
                dist.euclidianDistance(customer2.get_x_coord(), customer2.get_y_coord(
                ), self._depot.get_x_coord(), self._depot.get_y_coord())
            load = customer1.get_demand() + customer2.get_demand()
            service = customer1.get_service() + customer2.get_service()
        elif index == 0:
            cost = self._cost - dist.euclidianDistance(self._depot.get_x_coord(), self._depot.get_y_coord(), self._tour[0].get_x_coord(), self._tour[0].get_y_coord()) + \
                dist.euclidianDistance(self._depot.get_x_coord(), self._depot.get_y_coord(), customer1.get_x_coord(), customer1.get_y_coord()) + \
                dist.euclidianDistance(customer1.get_x_coord(), customer1.get_y_coord(), customer2.get_x_coord(), customer2.get_y_coord()) + \
                dist.euclidianDistance(customer2.get_x_coord(), customer2.get_y_coord(
                ), self._tour[0].get_x_coord(), self._tour[0].get_y_coord())
        elif index == length:
            cost = self._cost - dist.euclidianDistance(self._depot.get_x_coord(), self._depot.get_y_coord(), self._tour[length-1].get_x_coord(), self._tour[length-1].get_y_coord()) + \
                dist.euclidianDistance(self._tour[length-1].get_x_coord(), self._tour[length-1].get_y_coord(), customer1.get_x_coord(), customer1.get_y_coord()) + \
                dist.euclidianDistance(customer1.get_x_coord(), customer1.get_y_coord(), customer2.get_x_coord(), customer2.get_y_coord()) + \
                dist.euclidianDistance(customer2.get_x_coord(), customer2.get_y_coord(
                ), self._depot.get_x_coord(), self._depot.get_y_coord())
        # está entre dois clientes
        else:
            cost = self._cost - dist.euclidianDistance(self._tour[index-1].get_x_coord(), self._tour[index-1].get_y_coord(), self._tour[index].get_x_coord(), self._tour[index].get_y_coord()) + \
                dist.euclidianDistance(self._tour[index-1].get_x_coord(), self._tour[index-1].get_y_coord(), customer1.get_x_coord(), customer1.get_y_coord()) + \
                dist.euclidianDistance(customer1.get_x_coord(), customer1.get_y_coord(), customer2.get_x_coord(), customer2.get_y_coord()) + \
                dist.euclidianDistance(customer2.get_x_coord(), customer2.get_y_coord(
                ), self._tour[index].get_x_coord(), self._tour[index].get_y_coord())

        # verificar se há penalizações
        costTotal = cost
        if load > self._depot.get_loadVehicle():
            costTotal += 1000 * (load - self._depot.get_loadVehicle())
        if cost + service > self._depot.get_durationRoute():
            costTotal += 1000 * abs(service + cost -
                                    self._depot.get_durationRoute())

        return [costTotal, cost, load, service]

    '''
    Método calcula custo ao remover um nó da rota
    @param customer
    @return lista [custo com penalização, custo sem penalização, carregamento total, duração total]
    '''

    def costWithoutNode(self, indexCst):
        cost = 0.0
        load = self._totalDemand - self._tour[indexCst].get_demand()
        service = self._totalService - self._tour[indexCst].get_service()
        length = len(self._tour)

        if length == 1:  # só tem esse cliente
            return [0, 0, 0, 0]
        # verificar se ele liga ao depósito
        elif indexCst == 0:
            cost = self._cost - dist.euclidianDistance(self._depot.get_x_coord(), self._depot.get_y_coord(), self._tour[indexCst].get_x_coord(), self._tour[indexCst].get_y_coord()) + \
                dist.euclidianDistance(self._depot.get_x_coord(), self._depot.get_y_coord(), self._tour[1].get_x_coord(), self._tour[1].get_y_coord()) - \
                dist.euclidianDistance(self._tour[indexCst].get_x_coord(), self._tour[indexCst].get_y_coord(
                ), self._tour[1].get_x_coord(), self._tour[1].get_y_coord())

        elif indexCst == length-1:
            cost = self._cost - dist.euclidianDistance(self._depot.get_x_coord(), self._depot.get_y_coord(), self._tour[indexCst].get_x_coord(), self._tour[indexCst].get_y_coord()) + \
                dist.euclidianDistance(self._depot.get_x_coord(), self._depot.get_y_coord(), self._tour[length-2].get_x_coord(), self._tour[length-2].get_y_coord()) - \
                dist.euclidianDistance(self._tour[indexCst].get_x_coord(), self._tour[indexCst].get_y_coord(
                ), self._tour[length-2].get_x_coord(), self._tour[length-2].get_y_coord())
        # está entre dois clientes
        else:
            cost = self._cost - dist.euclidianDistance(self._tour[indexCst-1].get_x_coord(), self._tour[indexCst-1].get_y_coord(), self._tour[indexCst].get_x_coord(), self._tour[indexCst].get_y_coord()) - \
                dist.euclidianDistance(self._tour[indexCst].get_x_coord(), self._tour[indexCst].get_y_coord(), self._tour[indexCst+1].get_x_coord(), self._tour[indexCst+1].get_y_coord()) + \
                dist.euclidianDistance(self._tour[indexCst-1].get_x_coord(), self._tour[indexCst-1].get_y_coord(
                ), self._tour[indexCst+1].get_x_coord(), self._tour[indexCst+1].get_y_coord())

        # verificar se há penalizações
        costTotal = cost
        if load > self._depot.get_loadVehicle():
            costTotal += 1000 * (load - self._depot.get_loadVehicle())
        if cost + service > self._depot.get_durationRoute():
            costTotal += 1000 * abs(service + cost -
                                    self._depot.get_durationRoute())

        return [costTotal, cost, load, service]

    '''
    Método calcula custo ao remover dois nós consecutivos da rota
    Método vai ser chamado apenas se existirem os dois nós consecutivos
    @param primeiro índice a ser removido
    @return lista [custo com penalização, custo sem penalização, carregamento total, duração total]
    '''

    def costWithout2Nodes(self, indexFst):
        cost = 0.0
        load = self._totalDemand - \
            self._tour[indexFst].get_demand(
            ) - self._tour[indexFst+1].get_demand()
        service = self._totalService - \
            self._tour[indexFst].get_service(
            ) - self._tour[indexFst+1].get_service()
        length = len(self._tour)

        if length == 2:  # só tem esses 2 clientes
            return [0, 0, 0, 0]
        # verificar se o primeiro liga ao depósito
        elif indexFst == 0:
            cost = self._cost - dist.euclidianDistance(self._depot.get_x_coord(), self._depot.get_y_coord(), self._tour[0].get_x_coord(), self._tour[0].get_y_coord()) - \
                dist.euclidianDistance(self._tour[0].get_x_coord(), self._tour[0].get_y_coord(), self._tour[1].get_x_coord(), self._tour[1].get_y_coord()) - \
                dist.euclidianDistance(self._tour[1].get_x_coord(), self._tour[1].get_y_coord(), self._tour[2].get_x_coord(), self._tour[2].get_y_coord()) + \
                dist.euclidianDistance(self._depot.get_x_coord(), self._depot.get_y_coord(
                ), self._tour[2].get_x_coord(), self._tour[2].get_y_coord())

        elif indexFst == length-2:
            cost = self._cost - dist.euclidianDistance(self._tour[length-3].get_x_coord(), self._tour[length-3].get_y_coord(), self._tour[indexFst].get_x_coord(), self._tour[indexFst].get_y_coord()) - \
                dist.euclidianDistance(self._tour[indexFst].get_x_coord(), self._tour[indexFst].get_y_coord(), self._tour[indexFst+1].get_x_coord(), self._tour[indexFst+1].get_y_coord()) - \
                dist.euclidianDistance(self._tour[indexFst+1].get_x_coord(), self._tour[indexFst+1].get_y_coord(), self._depot.get_x_coord(), self._depot.get_y_coord()) + \
                dist.euclidianDistance(self._tour[length-3].get_x_coord(
                ), self._tour[length-3].get_y_coord(), self._depot.get_x_coord(), self._depot.get_y_coord())
        # está entre dois clientes
        else:

            cost = self._cost - dist.euclidianDistance(self._tour[indexFst-1].get_x_coord(), self._tour[indexFst-1].get_y_coord(), self._tour[indexFst].get_x_coord(), self._tour[indexFst].get_y_coord()) - \
                dist.euclidianDistance(self._tour[indexFst].get_x_coord(), self._tour[indexFst].get_y_coord(), self._tour[indexFst+1].get_x_coord(), self._tour[indexFst+1].get_y_coord()) - \
                dist.euclidianDistance(self._tour[indexFst+1].get_x_coord(), self._tour[indexFst+1].get_y_coord(), self._tour[indexFst+2].get_x_coord(), self._tour[indexFst+2].get_y_coord()) + \
                dist.euclidianDistance(self._tour[indexFst-1].get_x_coord(), self._tour[indexFst-1].get_y_coord(
                ), self._tour[indexFst+2].get_x_coord(), self._tour[indexFst+2].get_y_coord())
        # verificar se há penalizações
        costTotal = cost
        if load > self._depot.get_loadVehicle():
            costTotal += 1000 * (load - self._depot.get_loadVehicle())
        if cost + service > self._depot.get_durationRoute():
            costTotal += 1000 * \
                (abs(cost + service - self._depot.get_durationRoute()))

        return [costTotal, cost, load, service]
