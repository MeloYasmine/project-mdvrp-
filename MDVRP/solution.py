'''
Arquivo responsável pela representação e estruturação da solução
'''
from customers import Customers
from depots import Depots


class Solution:
    _giantTour = None
    _routes = None
    _cost = float()
    _depots = None
    _ranking = float()
    _nRoutesByDepot = {}  # número de rotas por depósito

    def __init__(self):
        self._giantTour = []  # lista de clientes, cada item um Customer
        self._routes = []  # lista de Route

        # self._idRoutes = []  # indicativo da rota

        self._cost = 0
        self._depots = []  # lista de depósitos, cada item o Depot de cada cliente
        self._infeasible = False
        nRoutesByDepot = []
        for dpt in Depots.get_depotsList():
            nRoutesByDepot.append((dpt, 0))
        # número de rotas por depósitos
        self._nRoutesByDepot = dict(nRoutesByDepot)

    def increaseRoute(self, keyDepot, quant=1):
        self._nRoutesByDepot[keyDepot] = self._nRoutesByDepot[keyDepot] + quant

    def decreaseRoute(self, keyDepot, quant=1):
        self._nRoutesByDepot[keyDepot] = self._nRoutesByDepot[keyDepot] - quant

    def get_nRoutesByDepot(self, keyDepot=None):
        if keyDepot == None:
            return self._nRoutesByDepot
        else:
            return self._nRoutesByDepot[keyDepot]

    def set_ranking(self, ranking):
        self._ranking = ranking

    def get_ranking(self):
        return self._ranking

    '''
    Método adiciona uma rota em uma lista
    '''

    def addRoutes(self, route):
        if route.is_infeasible():
            self._infeasible = True
        self.increaseRoute(str(route.get_depot().get_id()))
        self._routes.append(route)

    '''
    Método atualiza uma rota
    '''

    def setRoute(self, route, idRoute):
        oldRoute = self._routes[idRoute]
        if route.get_depot() != oldRoute.get_depot():
            self.increaseRoute(str(route.get_depot().get_id()))
            self.decreaseRoute(str(oldRoute.get_depot().get_id()))
        self._routes[idRoute] = route

    '''
    Método remove uma rota
    '''

    def removeRoutesEmpty(self):
        auxRoutes = []
        # verificar depósitos com excesso de rotas
        exceed = []
        depots = Depots.get_depotsList()
        for c in self._nRoutesByDepot:
            if depots[c].get_numberVehicles() < self._nRoutesByDepot[c]:
                exceed.append(c)
        # eliminar rotas vazias
        for r in self._routes:
            if r.get_tour():
                auxRoutes.append(r)
            else:  # está vazia
                keyDpt = str(r.get_depot().get_id())
                self.decreaseRoute(keyDpt)
                if keyDpt in exceed and depots[keyDpt].get_numberVehicles() >= self._nRoutesByDepot[keyDpt]:
                    self._cost -= 1000

        self._routes = auxRoutes

        # self._routes = list(filter(lambda x: [] != x.get_tour(), self._routes))
        # print(self._routes)

    '''
    Método concatena as rotas em uma única lista (giantTour)
    '''

    def formGiantTour(self):
        self._giantTour = []
        self._depots = []
        for r in self._routes:
            self._giantTour = self._giantTour + r.get_tour()
            for i in range(len(r.get_tour())):
                self._depots.append(r.get_depot())

    '''
    Método adiciona clientes no giantTour e o depósito correspondente
    '''

    def addGiantTour(self, customer, depot):
        self._giantTour.append(customer)
        self._depots.append(depot)

    '''
    Método calcula o custo total da solução
    '''

    def calculateCost(self, extraPenalty=0):
        self._cost = 0.0
        depots = Depots.get_depotsList()
        for r in self._routes:
            self._cost += r.get_totalCost()
        # penalidade por excesso de rotas
        if extraPenalty > 0:
            self._cost += extraPenalty
            self._infeasible = True
        else:
            # verificar número de rotas por depósito
            for i in self.get_nRoutesByDepot():
                nRoutes = self.get_nRoutesByDepot()[i]
                nVehicles = depots[i].get_numberVehicles()
                if nVehicles < nRoutes:  # excedente
                    exceed = nRoutes - nVehicles
                    self._cost += exceed * 1000

        #self._cost += self.diversity(10)
        # print(self._cost)

    '''
    Método retorna rotas
    '''

    def get_routes(self):
        return self._routes

    def get_giantTour(self):
        return self._giantTour

    def set_giantTour(self, giant):
        self._giantTour = giant

    def get_depots(self):
        return self._depots

    def set_depots(self, depots):
        self._depots = depots

    def get_cost(self):
        return self._cost

    def __str__(self):
        aux = ""
        if self._infeasible:
            aux = "inviável"

        return "ranking: " + str(self._ranking) + " \ngiantTour: " + str(self._giantTour) + "\n" + "depósitos: " + str(self._depots) + "\ncusto: " + str(self._cost) + " - " + aux

    def __repr__(self):
        aux = ""
        if self._infeasible:
            aux = "inviável"

        return "ranking: " + str(self._ranking)+" \ngiantTour: " + str(self._giantTour) + "\n" + "depósitos: " + str(self._depots) + "\ncusto: " + str(self._cost) + " - " + aux + "\n"
