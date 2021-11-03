import math


class MovimentsLocalSearch:

    def removeUinsertAfterV(self, solution, idRouteU, idRouteV, idU, idV, cost=math.inf, onlyCost=False):
        '''
        Método remove u e o insere após v
        '''
        # print("removeUinsertAfterV - onlyCost: {}".format(onlyCost))
        # print("\n\n\nCost: "+str(cost))
        routeU = solution.get_routes()[idRouteU]
        routeV = solution.get_routes()[idRouteV]
        lenTourU = len(routeU.get_tour())
        lenTourV = len(routeV.get_tour())
        # print("Mesmo do inicio")
        # print("idRouteU: {}   idRouteV:{}".format(idRouteU, idRouteV))
        # print("RouteU")
        # print(routeU)
        # print("RouteV")
        # print(routeV)
        # print("idU: {}  idV:{}".format(idU, idV))
        if lenTourU > 0 and idU < lenTourU and idV < lenTourV:
            if idRouteU != idRouteV:  # rotas diferentes
                costRouteU, costRouteV = routeU.costRemoveUinsertAfterV(
                    idU, idV, routeU, routeV)

                # print("costU: {}   costV: {}".format(costRouteU, costRouteV))

                newCost = solution.get_cost() - routeU.get_totalCost() - \
                    routeV.get_totalCost() + \
                    costRouteU[0] + costRouteV[0]

                # print("newCost: {}".format(newCost))

                if onlyCost:
                    # print("newCost: {}".format(newCost))
                    return [solution, newCost]

                if newCost < cost:
                    # print("achou melhor")
                    u = routeU.get_tour()[idU]
                    routeU.popCustomer(idU)
                    routeU.set_cost(
                        costRouteU[1], costRouteU[2], costRouteU[3])
                    routeV.insertCustomer(u, idV+1)
                    routeV.set_cost(
                        costRouteV[1], costRouteV[2], costRouteV[3])
                    # solution.setRoute(routeU, idRouteU)
                    # solution.setRoute(routeV, idRouteV)
                    solution.formGiantTour()
                    solution.calculateCost()
            else:  # mesmas rotas
                # print("Mesmas rotas")
                # print("Mesma rota - u")
                # print(routeU)
                # print("idU: {}  idV:{}".format(idU, idV))
                if idU != idV:
                    costRouteU = routeU.costRemoveUinsertAfterVSameRoute(
                        idU, idV, routeU)

                    # print("costU: {} ".format(costRouteU))

                    newCost = solution.get_cost() - routeU.get_totalCost() + \
                        costRouteU[0]

                    # print("newCost: {}".format(newCost))

                    if onlyCost:
                        # print("newCost: {}".format(newCost))
                        return [solution, newCost]

                    if newCost < cost:
                        # print("achou melhor")
                        idVAux = idV
                        if idV > idU:
                            idVAux -= 1
                        u = routeU.get_tour()[idU]
                        routeU.popCustomer(idU)
                        routeU.insertCustomer(u, idVAux+1)
                        routeU.set_cost(
                            costRouteU[1], costRouteU[2], costRouteU[3])

                        # solution.setRoute(routeU, idRouteU)
                        solution.formGiantTour()
                        solution.calculateCost()

        return [solution, solution.get_cost()]

    def removeUXinsertAfterV(self, solution, idRouteU, idRouteV, idU, idV, cost=math.inf, onlyCost=False):
        '''
        Método remove u e x  e insere UX após v
        '''
        # print("removeUXinsertAfterV - onlyCost: {}".format(onlyCost))
        routeU = solution.get_routes()[idRouteU]
        routeV = solution.get_routes()[idRouteV]
        if len(routeU.get_tour()) > 1 and (idU + 1) < len(routeU.get_tour()):
            if idRouteU != idRouteV:  # rotas diferentes
                costRouteU, costRouteV = routeU.costRemoveUXinsertAfterV(
                    idU, idV, routeU, routeV)

                # print("costU: {}   costV: {}".format(costRouteU, costRouteV))

                newCost = solution.get_cost() - routeU.get_totalCost() - \
                    routeV.get_totalCost() + \
                    costRouteU[0] + costRouteV[0]

                if onlyCost:
                    # print("newCost: {}".format(newCost))
                    return [solution, newCost]

                if newCost < cost:
                    u = routeU.get_tour()[idU]
                    x = routeU.get_tour()[idU+1]
                    routeU.popCustomer(idU)
                    routeU.popCustomer(idU)
                    routeU.set_cost(
                        costRouteU[1], costRouteU[2], costRouteU[3])
                    routeV.insertCustomer(u, idV+1)
                    routeV.insertCustomer(x, idV+2)
                    routeV.set_cost(
                        costRouteV[1], costRouteV[2], costRouteV[3])
                    # solution.setRoute(routeU, idRouteU)
                    # solution.setRoute(routeV, idRouteV)
                    solution.formGiantTour()
                    solution.calculateCost()
            else:  # mesmas rotas
                # print("Mesmas rotas")
                if idU != idV and (idU+1) != idV:
                    costRouteU = routeU.costRemoveUXinsertAfterVSameRoute(
                        idU, idV, routeU)

                    # print("costU: {} ".format(costRouteU))

                    newCost = solution.get_cost() - routeU.get_totalCost() + \
                        costRouteU[0]

                    if onlyCost:
                        # print("newCost: {}".format(newCost))
                        return [solution, newCost]

                    if newCost < cost:
                        idVAux = idV
                        if idV > idU:
                            idVAux -= 2
                        u = routeU.get_tour()[idU]
                        x = routeU.get_tour()[idU+1]
                        routeU.popCustomer(idU)
                        routeU.popCustomer(idU)
                        routeU.insertCustomer(u, idVAux+1)
                        routeU.insertCustomer(x, idVAux+2)
                        routeU.set_cost(
                            costRouteU[1], costRouteU[2], costRouteU[3])

                        # solution.setRoute(routeU, idRouteU)
                        solution.formGiantTour()
                        solution.calculateCost()

        return [solution, solution.get_cost()]

    def removeUXinsertXUAfterV(self, solution, idRouteU, idRouteV, idU, idV, cost=math.inf, onlyCost=False):
        '''
        Método remove u e x  e insere XU após v
        '''
        # print("removeUXinsertXUAfterV - onlyCost: {}".format(onlyCost))
        routeU = solution.get_routes()[idRouteU]
        routeV = solution.get_routes()[idRouteV]
        if len(routeU.get_tour()) > 1 and (idU + 1) < len(routeU.get_tour()):
            if idRouteU != idRouteV:  # rotas diferentes
                costRouteU, costRouteV = routeU.costRemoveUXinsertXUAfterV(
                    idU, idV, routeU, routeV)

                # print("costU: {}   costV: {}".format(costRouteU, costRouteV))

                newCost = solution.get_cost() - routeU.get_totalCost() - \
                    routeV.get_totalCost() + \
                    costRouteU[0] + costRouteV[0]

                if onlyCost:
                    # print("newCost: {}".format(newCost))
                    return [solution, newCost]

                if newCost < cost:
                    u = routeU.get_tour()[idU]
                    x = routeU.get_tour()[idU+1]
                    routeU.popCustomer(idU)
                    routeU.popCustomer(idU)
                    routeU.set_cost(
                        costRouteU[1], costRouteU[2], costRouteU[3])
                    routeV.insertCustomer(x, idV+1)
                    routeV.insertCustomer(u, idV+2)
                    routeV.set_cost(
                        costRouteV[1], costRouteV[2], costRouteV[3])
                    # solution.setRoute(routeU, idRouteU)
                    # solution.setRoute(routeV, idRouteV)
                    solution.formGiantTour()
                    solution.calculateCost()
            else:  # mesmas rotas
                # print("Mesmas rotas")
                if idU != idV and (idU+1) != idV:
                    costRouteU = routeU.costRemoveUXinsertXUAfterVSameRoute(
                        idU, idV, routeU)

                    # print("costU: {} ".format(costRouteU))

                    newCost = solution.get_cost() - routeU.get_totalCost() + \
                        costRouteU[0]

                    if onlyCost:
                        # print("newCost: {}".format(newCost))
                        return [solution, newCost]

                    if newCost < cost:
                        idVAux = idV
                        if idV > idU:
                            idVAux -= 2
                        u = routeU.get_tour()[idU]
                        x = routeU.get_tour()[idU+1]
                        routeU.popCustomer(idU)
                        routeU.popCustomer(idU)
                        routeU.insertCustomer(x, idVAux+1)
                        routeU.insertCustomer(u, idVAux+2)
                        routeU.set_cost(
                            costRouteU[1], costRouteU[2], costRouteU[3])

                        # solution.setRoute(routeU, idRouteU)
                        solution.formGiantTour()
                        solution.calculateCost()

        return [solution, solution.get_cost()]

    def swap(self, solution, idRouteU, idRouteV, idU, idV, cost=math.inf, onlyCost=False):
        # print("swap - onlyCost: {}".format(onlyCost))
        '''
        Método troca u com v
        '''
        if idRouteU != idRouteV:  # rotas diferentes
            routeU = solution.get_routes()[idRouteU]
            routeV = solution.get_routes()[idRouteV]
            costRouteU, costRouteV = routeU.costSwapNodes(
                idU, idV, routeU, routeV)

            # print("costU: {}   costV: {}".format(costRouteU, costRouteV))

            newCost = solution.get_cost() - routeU.get_totalCost() - \
                routeV.get_totalCost() + \
                costRouteU[0] + costRouteV[0]

            if onlyCost:
                # print("newCost: {}".format(newCost))
                return [solution, newCost]

            if newCost < cost:
                u = routeU.get_tour()[idU]
                v = routeV.get_tour()[idV]
                routeU.changeCustomer(v, idU)
                routeU.set_cost(costRouteU[1], costRouteU[2], costRouteU[3])
                routeV.changeCustomer(u, idV)
                routeV.set_cost(costRouteV[1], costRouteV[2], costRouteV[3])
                # solution.setRoute(routeU, idRouteU)
                # solution.setRoute(routeV, idRouteV)
                solution.formGiantTour()
                solution.calculateCost()
        else:  # mesmas rotas
            # print("Mesmas rotas")
            routeU = solution.get_routes()[idRouteU]
            costRouteU = routeU.costSwapSameRoute(idU, idV, routeU)

            # print("costU: {} ".format(costRouteU))

            newCost = solution.get_cost() - routeU.get_totalCost() + \
                costRouteU[0]

            if onlyCost:
                return [solution, newCost]

            if newCost < cost:
                u = routeU.get_tour()[idU]
                v = routeU.get_tour()[idV]
                routeU.changeCustomer(v, idU)
                routeU.changeCustomer(u, idV)
                routeU.set_cost(costRouteU[1], costRouteU[2], costRouteU[3])
                # solution.setRoute(routeU, idRouteU)
                solution.formGiantTour()
                solution.calculateCost()

        return [solution, solution.get_cost()]

    def shiftUXwithVY(self, solution, idRouteU, idRouteV, idU, idV, cost=math.inf, onlyCost=False):
        # print("shiftUXwithVY - onlyCost: {}".format(onlyCost))
        routeU = solution.get_routes()[idRouteU]
        routeV = solution.get_routes()[idRouteV]
        if (idU + 1) < len(routeU.get_tour()) and (idV + 1) < len(routeV.get_tour()):
            if idRouteU != idRouteV:  # rotas diferentes
                costRouteU, costRouteV = routeU.costShiftUXwithVY(
                    idU, idV, routeU, routeV)

                newCost = solution.get_cost() - routeU.get_totalCost() - \
                    routeV.get_totalCost() + \
                    costRouteU[0] + costRouteV[0]

                # print("costU: {}   costV: {}".format(costRouteU, costRouteV))
                if onlyCost:
                    # print("newCost: {}".format(newCost))
                    return [solution, newCost]

                if newCost < cost:
                    u = routeU.get_tour()[idU]
                    v = routeV.get_tour()[idV]
                    x = routeU.get_tour()[idU+1]
                    y = routeV.get_tour()[idV+1]
                    routeU.changeCustomer(v, idU)
                    routeU.changeCustomer(y, idU+1)
                    routeU.set_cost(
                        costRouteU[1], costRouteU[2], costRouteU[3])
                    routeV.changeCustomer(u, idV)
                    routeV.changeCustomer(x, idV+1)
                    routeV.set_cost(
                        costRouteV[1], costRouteV[2], costRouteV[3])
                    # solution.setRoute(routeU, idRouteU)
                    # solution.setRoute(routeV, idRouteV)
                    solution.formGiantTour()
                    solution.calculateCost()

            else:
                # print("Mesma rota")
                if idU != idV and (idU+1) != idV and (idV+1) != idU:
                    costRouteU = routeU.costShiftUXwithVYsameRoute(
                        idU, idV, routeU)

                    # print("costU: {} ".format(costRouteU))

                    newCost = solution.get_cost() - routeU.get_totalCost() + \
                        costRouteU[0]
                    if onlyCost:
                        # print("newCost: {}".format(newCost))
                        return [solution, newCost]

                    if newCost < cost:
                        u = routeU.get_tour()[idU]
                        v = routeU.get_tour()[idV]
                        x = routeU.get_tour()[idU+1]
                        y = routeU.get_tour()[idV+1]
                        routeU.changeCustomer(v, idU)
                        routeU.changeCustomer(y, idU+1)
                        routeU.changeCustomer(u, idV)
                        routeU.changeCustomer(x, idV+1)
                        routeU.set_cost(
                            costRouteU[1], costRouteU[2], costRouteU[3])
                        # solution.setRoute(routeU, idRouteU)
                        solution.formGiantTour()
                        solution.calculateCost()

        return [solution, solution.get_cost()]

    def shiftUXwithV(self, solution, idRouteU, idRouteV, idU, idV, cost=math.inf, onlyCost=False):
        '''
        Método troca (u,x) e v
        '''
        # print("shiftUXwithV - onlyCost: {}".format(onlyCost))
        routeU = solution.get_routes()[idRouteU]
        routeV = solution.get_routes()[idRouteV]
        if (idU + 1) < len(routeU.get_tour()):
            if idRouteU != idRouteV:  # rotas diferentes
                costRouteU, costRouteV = routeU.costShiftUXwithV(
                    idU, idV, routeU, routeV)

                newCost = solution.get_cost() - routeU.get_totalCost() - \
                    routeV.get_totalCost() + \
                    costRouteU[0] + costRouteV[0]

                # print("costU: {}   costV: {}".format(costRouteU, costRouteV))
                if onlyCost:
                    # print("newCost: {}".format(newCost))
                    return [solution, newCost]
                if newCost < cost:
                    u = routeU.get_tour()[idU]
                    v = routeV.get_tour()[idV]
                    x = routeU.get_tour()[idU+1]
                    routeU.changeCustomer(v, idU)
                    routeU.popCustomer(idU+1)
                    routeU.set_cost(
                        costRouteU[1], costRouteU[2], costRouteU[3])
                    routeV.changeCustomer(u, idV)
                    routeV.insertCustomer(x, idV+1)
                    routeV.set_cost(
                        costRouteV[1], costRouteV[2], costRouteV[3])
                    # solution.setRoute(routeU, idRouteU)
                    # solution.setRoute(routeV, idRouteV)
                    solution.formGiantTour()
                    solution.calculateCost()

            else:
                # print("Mesma rota")
                if idU != idV and (idU+1) != idV:
                    costRouteU = routeU.costShiftUXwithVsameRoute(
                        idU, idV, routeU)

                    # print("costU: {} ".format(costRouteU))

                    newCost = solution.get_cost() - routeU.get_totalCost() + \
                        costRouteU[0]

                    if onlyCost:
                        # print("newCost: {}".format(newCost))
                        return [solution, newCost]

                    if newCost < cost:
                        u = routeU.get_tour()[idU]
                        v = routeV.get_tour()[idV]
                        x = routeU.get_tour()[idU+1]
                        idVAux = idV
                        if idV > idU:
                            idVAux = idV-1
                        routeU.changeCustomer(v, idU)
                        routeU.changeCustomer(u, idV)
                        routeU.popCustomer(idU+1)
                        routeU.insertCustomer(x, idVAux+1)
                        routeU.set_cost(
                            costRouteU[1], costRouteU[2], costRouteU[3])
                        # solution.setRoute(routeU, idRouteU)
                        solution.formGiantTour()
                        solution.calculateCost()

        return [solution, solution.get_cost()]

    def shiftUXVYwithUVXY(self, solution, idRouteU, idRouteV, idU, idV, cost=math.inf, onlyCost=False):
        # print("shiftUXVYwithUVXY - onlyCost: {}".format(onlyCost))
        '''
        Método troca (u,x) e (v,y) por (u,v) e (x,y)
        '''
        routeU = solution.get_routes()[idRouteU]
        routeV = solution.get_routes()[idRouteV]
        if (idU + 1) < len(routeU.get_tour()) and (idV + 1) < len(routeV.get_tour()):
            if idRouteU != idRouteV:  # rotas diferentes
                costRouteU, costRouteV = routeU.costShiftUXVYwithUVXY(
                    idU, idV, routeU, routeV)
                newCost = solution.get_cost() - routeU.get_totalCost() - \
                    routeV.get_totalCost() + \
                    costRouteU[0] + costRouteV[0]

                # print("costU: {}   costV: {}".format(costRouteU, costRouteV))
                if onlyCost:
                    # print("newCost: {}".format(newCost))
                    return [solution, newCost]

                if newCost < cost:
                    v = routeV.get_tour()[idV]
                    x = routeU.get_tour()[idU+1]
                    routeU.changeCustomer(v, idU+1)
                    routeU.set_cost(
                        costRouteU[1], costRouteU[2], costRouteU[3])
                    routeV.changeCustomer(x, idV)
                    routeV.set_cost(
                        costRouteV[1], costRouteV[2], costRouteV[3])
                    # solution.setRoute(routeU, idRouteU)
                    # solution.setRoute(routeV, idRouteV)
                    solution.formGiantTour()
                    solution.calculateCost()
            else:  # mesmas rotas
                # print("Mesma rota")
                if idU != idV and (idU+1) != idV and (idV+1) != idU:
                    costRouteU = routeU.costShiftUXVYwithUVXYSameRoute(
                        idU, idV, routeU)

                    # print("costU: {} ".format(costRouteU))

                    newCost = solution.get_cost() - routeU.get_totalCost() + \
                        costRouteU[0]
                    if onlyCost:
                        # print("newCost: {}".format(newCost))
                        return [solution, newCost]

                    if newCost < cost:
                        v = routeU.get_tour()[idV]
                        x = routeU.get_tour()[idU+1]
                        routeU.changeCustomer(v, idU+1)
                        routeU.changeCustomer(x, idV)
                        routeU.set_cost(
                            costRouteU[1], costRouteU[2], costRouteU[3])
                        # solution.setRoute(routeU, idRouteU)
                        solution.formGiantTour()
                        solution.calculateCost()

        return [solution, solution.get_cost()]

    def shiftUXVYwithUYXV(self, solution, idRouteU, idRouteV, idU, idV, cost=math.inf, onlyCost=False):
        # print("shiftUXVYwithUYXV - onlyCost: {}".format(onlyCost))
        '''
        Método troca (u,x) e (v,y) por (u,y) e (x,v)
        '''
        routeU = solution.get_routes()[idRouteU]
        routeV = solution.get_routes()[idRouteV]
        if (idU + 1) < len(routeU.get_tour()) and (idV + 1) < len(routeV.get_tour()):
            if idRouteU != idRouteV:  # rotas diferentes
                costRouteU, costRouteV = routeU.costShiftUXVYwithUYXV(
                    idU, idV, routeU, routeV)
                newCost = solution.get_cost() - routeU.get_totalCost() - \
                    routeV.get_totalCost() + \
                    costRouteU[0] + costRouteV[0]

                # print("costU: {}   costV: {}".format(costRouteU, costRouteV))
                if onlyCost:
                    # print("newCost: {}".format(newCost))
                    return [solution, newCost]

                if newCost < cost:
                    v = routeV.get_tour()[idV]
                    x = routeU.get_tour()[idU+1]
                    y = routeV.get_tour()[idV+1]
                    routeU.changeCustomer(y, idU+1)
                    routeU.set_cost(
                        costRouteU[1], costRouteU[2], costRouteU[3])
                    routeV.changeCustomer(x, idV)
                    routeV.changeCustomer(v, idV+1)
                    routeV.set_cost(
                        costRouteV[1], costRouteV[2], costRouteV[3])
                    # solution.setRoute(routeU, idRouteU)
                    # solution.setRoute(routeV, idRouteV)
                    solution.formGiantTour()
                    solution.calculateCost()
            else:  # mesmas rotas
                # print("Mesma rota")
                if idU != idV and (idU+1) != idV and (idV+1) != idU:
                    costRouteU = routeU.costShiftUXVYwithUYXVSameRoute(
                        idU, idV, routeU)

                    # print("costU: {} ".format(costRouteU))

                    newCost = solution.get_cost() - routeU.get_totalCost() + \
                        costRouteU[0]

                    if onlyCost:
                        # print("newCost: {}".format(newCost))
                        return [solution, newCost]

                    if newCost < cost:
                        v = routeU.get_tour()[idV]
                        x = routeU.get_tour()[idU+1]
                        y = routeU.get_tour()[idV+1]
                        routeU.changeCustomer(y, idU+1)
                        routeU.changeCustomer(x, idV)
                        routeU.changeCustomer(v, idV+1)
                        routeU.set_cost(
                            costRouteU[1], costRouteU[2], costRouteU[3])
                        # solution.setRoute(routeU, idRouteU)
                        solution.formGiantTour()
                        solution.calculateCost()

        return [solution, solution.get_cost()]
