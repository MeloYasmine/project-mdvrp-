import copy


class AuxiliaryLS:

    '''
    Método insere u após v (v não é um depósito)
    @return novo custo, nova rotaU, nova rotaV
    '''

    def insertUafterV(self, routeU, routeV, iu, iv, totalCost):
        auxRouteU = copy.deepcopy(routeU)
        auxRouteV = copy.deepcopy(routeV)
        u = auxRouteU.get_tour()[iu]
        v = auxRouteV.get_tour()[iv]
        # print(u)
        # print(v)

        indV = iv
        # remove u
        costRouteU = auxRouteU.costWithoutNode(iu)
        auxRouteU.popCustomer(iu)
        auxRouteU.set_cost(
            costRouteU[1], costRouteU[2], costRouteU[3])
        # pertencem a diferentes rotas
        if u not in auxRouteV.get_tour():
            # insere u após v
            costRouteV = auxRouteV.costWithNode(u, indV+1)
            auxRouteV.insertCustomer(u, indV+1)
            auxRouteV.set_cost(
                costRouteV[1], costRouteV[2], costRouteV[3])

            newCost = totalCost - routeU.get_totalCost() - routeV.get_totalCost() + \
                costRouteU[0] + costRouteV[0]

            if newCost < totalCost:
                return newCost, auxRouteU, auxRouteV
        # pertencem a mesma rota
        else:
            if iv > iu:
                indV = iv - 1
            # insere u após v
            costRouteV = auxRouteU.costWithNode(u, indV+1)
            auxRouteU.insertCustomer(u, indV+1)
            auxRouteU.set_cost(
                costRouteV[1], costRouteV[2], costRouteV[3])

            auxRouteV = copy.deepcopy(auxRouteU)
            # print(auxRouteV)

            newCost = totalCost - routeU.get_totalCost() + \
                costRouteV[0]

            if newCost < totalCost:
                return newCost, auxRouteU, auxRouteV

        return totalCost, routeU, routeV

    '''
    Método insere u após v (v é um depósito)
    @return novo custo, nova rotaU, nova rotaV
    '''

    def insertUafterDepot(self, routeU, routeV, iu, totalCost):
        auxRouteU = copy.deepcopy(routeU)
        auxRouteV = copy.deepcopy(routeV)
        u = auxRouteU.get_tour()[iu]
        # print(u)

        # remove u
        costRouteU = auxRouteU.costWithoutNode(iu)
        auxRouteU.popCustomer(iu)
        auxRouteU.set_cost(
            costRouteU[1], costRouteU[2], costRouteU[3])
        # pertencem a diferentes rotas
        if u not in auxRouteV.get_tour():
            # insere u após v
            costRouteV = routeV.costWithNode(u, 0)
            auxRouteV.insertCustomer(u, 0)
            auxRouteV.set_cost(
                costRouteV[1], costRouteV[2], costRouteV[3])

            newCost = totalCost - routeU.get_totalCost() - routeV.get_totalCost() + \
                costRouteU[0] + costRouteV[0]

            if newCost < totalCost:
                return newCost, auxRouteU, auxRouteV
        # pertencem a mesma rota
        else:
            # insere u após v
            costRouteV = auxRouteU.costWithNode(u, 0)
            auxRouteU.insertCustomer(u, 0)
            auxRouteU.set_cost(
                costRouteV[1], costRouteV[2], costRouteV[3])

            auxRouteV = copy.deepcopy(auxRouteU)

            newCost = totalCost - routeU.get_totalCost() + \
                costRouteV[0]

            if newCost < totalCost:
                return newCost, auxRouteU, auxRouteV

        return totalCost, routeU, routeV

    '''
    Método insere u e x após v (v não é um depósito)
    @return novo custo, nova rotaU, nova rotaV
    '''

    def insertUXafterV(self, routeU, routeV, iu, iv, totalCost):
        auxRouteU = copy.deepcopy(routeU)
        auxRouteV = copy.deepcopy(routeV)
        u = auxRouteU.get_tour()[iu]
        v = auxRouteV.get_tour()[iv]
        x = auxRouteU.get_tour()[iu+1]
        # print(u)
        # print(v)

        indV = iv
        # remove u e x
        costRouteU = auxRouteU.costWithout2Nodes(iu)
        auxRouteU.popCustomer(iu)
        auxRouteU.popCustomer(iu)
        auxRouteU.set_cost(
            costRouteU[1], costRouteU[2], costRouteU[3])

        # pertencem a diferentes rotas
        if u not in auxRouteV.get_tour():
            # insere u e x após v
            costRouteV = auxRouteV.costWith2Nodes(
                u, x, indV+1)
            auxRouteV.insertCustomer(u, indV+1)
            auxRouteV.insertCustomer(x, indV+2)
            auxRouteV.set_cost(
                costRouteV[1], costRouteV[2], costRouteV[3])

            newCost = totalCost - routeU.get_totalCost() - routeV.get_totalCost() + \
                costRouteU[0] + costRouteV[0]

            if newCost < totalCost:
                return newCost, auxRouteU, auxRouteV
        # pertencem a mesma rota
        else:
            if iv > iu:
                indV = iv - 2
            # insere u e x após v
            costRouteV = auxRouteU.costWith2Nodes(
                u, x, indV+1)
            auxRouteU.insertCustomer(u, indV+1)
            auxRouteU.insertCustomer(x, indV+2)
            auxRouteU.set_cost(
                costRouteV[1], costRouteV[2], costRouteV[3])

            auxRouteV = copy.deepcopy(auxRouteU)

            newCost = totalCost - routeU.get_totalCost() + \
                costRouteV[0]

            if newCost < totalCost:
                return newCost, auxRouteU, auxRouteV

        return totalCost, routeU, routeV

    '''
    Método insere u e x após v (v é um depósito)
    @return novo custo, nova rotaU, nova rotaV
    '''

    def insertUXafterDepot(self, routeU, routeV, iu, totalCost):
        auxRouteU = copy.deepcopy(routeU)
        auxRouteV = copy.deepcopy(routeV)
        u = auxRouteU.get_tour()[iu]
        x = auxRouteU.get_tour()[iu+1]
        # print(u)

        # remove u e x
        costRouteU = auxRouteU.costWithout2Nodes(iu)
        auxRouteU.popCustomer(iu)
        auxRouteU.popCustomer(iu)
        auxRouteU.set_cost(
            costRouteU[1], costRouteU[2], costRouteU[3])

        # pertencem a diferentes rotas
        if u not in auxRouteV.get_tour():
            # insere u e x após v
            costRouteV = auxRouteV.costWith2Nodes(
                u, x, 0)

            auxRouteV.insertCustomer(u, 0)
            auxRouteV.insertCustomer(x, 1)
            auxRouteV.set_cost(
            costRouteV[1], costRouteV[2], costRouteV[3])

            newCost = totalCost - routeU.get_totalCost() - routeV.get_totalCost() + \
                costRouteU[0] + costRouteV[0]

            if newCost < totalCost:
                return newCost, auxRouteU, auxRouteV
        # pertencem a mesma rota
        else:
            # insere u e x após v
            costRouteV = auxRouteU.costWith2Nodes(
                u, x, 0)
            auxRouteU.insertCustomer(u, 0)
            auxRouteU.insertCustomer(x, 1)
            auxRouteU.set_cost(
                costRouteV[1], costRouteV[2], costRouteV[3])

            auxRouteV = copy.deepcopy(auxRouteU)

            newCost = totalCost - routeU.get_totalCost() + \
                costRouteV[0]

            if newCost < totalCost:
                return newCost, auxRouteU, auxRouteV

        return totalCost, routeU, routeV

    '''
    Método insere (x,u) após v (v não é um depósito)
    @return novo custo, nova rotaU, nova rotaV
    '''

    def insertXUafterV(self, routeU, routeV, iu, iv, totalCost):
        auxRouteU = copy.deepcopy(routeU)
        auxRouteV = copy.deepcopy(routeV)
        u = auxRouteU.get_tour()[iu]
        v = auxRouteV.get_tour()[iv]
        x = auxRouteU.get_tour()[iu+1]
        # print(u)
        # print(v)

        indV = iv
        # remove u e x
        costRouteU = auxRouteU.costWithout2Nodes(iu)
        auxRouteU.popCustomer(iu)
        auxRouteU.popCustomer(iu)
        auxRouteU.set_cost(
            costRouteU[1], costRouteU[2], costRouteU[3])

        # pertencem a diferentes rotas
        if u not in auxRouteV.get_tour():
            # insere x e u após v
            costRouteV = auxRouteV.costWith2Nodes(
                x, u, indV+1)
            auxRouteV.insertCustomer(x, indV+1)
            auxRouteV.insertCustomer(u, indV+2)
            auxRouteV.set_cost(
                costRouteV[1], costRouteV[2], costRouteV[3])

            newCost = totalCost - routeU.get_totalCost() - routeV.get_totalCost() + \
                costRouteU[0] + costRouteV[0]

            if newCost < totalCost:
                return newCost, auxRouteU, auxRouteV
        # pertencem a mesma rota
        else:
            if iv > iu:
                indV = iv - 2
            # insere u e x após v
            costRouteV = auxRouteU.costWith2Nodes(
                x, u, indV+1)
            auxRouteU.insertCustomer(x, indV+1)
            auxRouteU.insertCustomer(u, indV+2)
            auxRouteU.set_cost(
                costRouteV[1], costRouteV[2], costRouteV[3])

            auxRouteV = copy.deepcopy(auxRouteU)

            newCost = totalCost - routeU.get_totalCost() + \
                costRouteV[0]

            if newCost < totalCost:
                return newCost, auxRouteU, auxRouteV

        return totalCost, routeU, routeV

    '''
    Método insere (x,u) após v (v não é um depósito)
    @return novo custo, nova rotaU, nova rotaV
    '''

    def insertXUafterDepot(self, routeU, routeV, iu, totalCost):
        auxRouteU = copy.deepcopy(routeU)
        auxRouteV = copy.deepcopy(routeV)
        u = auxRouteU.get_tour()[iu]
        x = auxRouteU.get_tour()[iu+1]
        # print(u)

        # remove u e x
        costRouteU = auxRouteU.costWithout2Nodes(iu)
        auxRouteU.popCustomer(iu)
        auxRouteU.popCustomer(iu)
        auxRouteU.set_cost(
            costRouteU[1], costRouteU[2], costRouteU[3])

        # pertencem a diferentes rotas
        if u not in auxRouteV.get_tour():
            # insere x e u após v
            costRouteV = auxRouteV.costWith2Nodes(
                x, u, 0)
            auxRouteV.insertCustomer(x, 0)
            auxRouteV.insertCustomer(u, 1)
            auxRouteV.set_cost(
            costRouteV[1], costRouteV[2], costRouteV[3])

            newCost = totalCost - routeU.get_totalCost() - routeV.get_totalCost() + \
                costRouteU[0] + costRouteV[0]

            if newCost < totalCost:
                return newCost, auxRouteU, auxRouteV
        # pertencem a mesma rota
        else:
            # insere u e x após v
            costRouteV = auxRouteU.costWith2Nodes(
                x, u, 0)
            auxRouteU.insertCustomer(x, 0)
            auxRouteU.insertCustomer(u, 1)
            auxRouteU.set_cost(
                costRouteV[1], costRouteV[2], costRouteV[3])

            auxRouteV = copy.deepcopy(auxRouteU)

            newCost = totalCost - routeU.get_totalCost() + \
                costRouteV[0]

            if newCost < totalCost:
                return newCost, auxRouteU, auxRouteV

        return totalCost, routeU, routeV

    '''
    Método troca cliente u com o cliente v
    @return novo custo, nova rotaU, nova rotaV
    '''

    def swapUV(self, routeU, routeV, iu, iv, totalCost):
        auxRouteU = copy.deepcopy(routeU)
        auxRouteV = copy.deepcopy(routeV)
        u = auxRouteU.get_tour()[iu]
        v = auxRouteV.get_tour()[iv]
        # print(u)
        # print(v)
        # pertencem a diferentes rotas
        if u not in auxRouteV.get_tour():
            listIdOld = [iu]
            listNew = [v]
            costRouteU = auxRouteU.costShiftNodes(
                listIdOld, listNew, auxRouteU)
            listIdOld = [iv]
            listNew = [u]
            costRouteV = auxRouteV.costShiftNodes(
                listIdOld, listNew, auxRouteV)

            auxRouteU.popCustomer(iu)
            auxRouteU.insertCustomer(v, iu)
            auxRouteU.set_cost(
                costRouteU[1], costRouteU[2], costRouteU[3])
            # print(auxRouteU)
            auxRouteV.popCustomer(iv)
            auxRouteV.insertCustomer(u, iv)
            auxRouteV.set_cost(
                costRouteV[1], costRouteV[2], costRouteV[3])
            # print(auxRouteV)
            newCost = totalCost - routeU.get_totalCost() - routeV.get_totalCost() + \
                costRouteU[0] + costRouteV[0]

            if newCost < totalCost:
                return newCost, auxRouteU, auxRouteV
        # pertencem a mesma rota
        else:
            aux1 = [iu]
            aux2 = [iv]
            # print(aux1)
            # print(aux2)
            costRouteV = auxRouteU.costShiftNodesSameRoute(
                aux1, aux2, auxRouteU)  # [custo total, rota]
            auxRouteU = costRouteV[1]
            auxRouteV = copy.deepcopy(auxRouteU)
           
            newCost = totalCost - routeU.get_totalCost() + \
                costRouteV[0]

            if newCost < totalCost:
                return newCost, auxRouteU, auxRouteV

        return totalCost, routeU, routeV

    '''
    Método troca cliente (u,x) com o cliente v
    @return novo custo, nova rotaU, nova rotaV
    '''

    def swapUXwithV(self, routeU, routeV, iu, iv, totalCost):
        auxRouteU = copy.deepcopy(routeU)
        auxRouteV = copy.deepcopy(routeV)
        u = auxRouteU.get_tour()[iu]
        v = auxRouteV.get_tour()[iv]
        routeUSize = len(routeU.get_tour())
        # print(u)
        # print(v)
        # pertencem a diferentes rotas
        if u not in routeV.get_tour():
            if iu+1 < routeUSize:
                listIdOld = [iu, iu+1]
                listNew = [v]
                costRouteU = auxRouteU.costShiftNodes(
                    listIdOld, listNew, auxRouteU)

                listIdOld = [iv]
                listNew = [u, routeU.get_tour()[iu+1]]
                costRouteV = auxRouteV.costShiftNodes(
                    listIdOld, listNew, auxRouteV)

                auxRouteU.popCustomer(iu)
                auxRouteU.insertCustomer(v, iu)
                auxRouteU.popCustomer(iu+1)
                auxRouteU.set_cost(
                    costRouteU[1], costRouteU[2], costRouteU[3])


                auxRouteV.popCustomer(iv)
                auxRouteV.insertCustomer(u, iv)
                auxRouteV.insertCustomer(
                    routeU.get_tour()[iu+1], iv+1)
                auxRouteV.set_cost(
                    costRouteV[1], costRouteV[2], costRouteV[3])

                newCost = totalCost - routeU.get_totalCost() - routeV.get_totalCost() + \
                    costRouteU[0] + costRouteV[0]

                if newCost < totalCost:
                    return newCost, auxRouteU, auxRouteV
        # pertencem a mesma rota
        else:
            if iu+1 < routeUSize and routeU.get_tour()[iu+1] != v:
                aux1 = [iu, iu+1]
                aux2 = [iv]
                costRouteU = auxRouteU.costShiftNodesSameRoute(
                    aux1, aux2, auxRouteU)  # [custo total, rota]
                auxRouteU = costRouteU[1]

                auxRouteV = copy.deepcopy(auxRouteU)

                newCost = totalCost - routeU.get_totalCost() + \
                    costRouteU[0]

                if newCost < totalCost:
                    return newCost, auxRouteU, auxRouteV

        return totalCost, routeU, routeV

    '''
    Método troca cliente (u,x) com o cliente (v,y)
    @return novo custo, nova rotaU, nova rotaV
    '''

    def swapUXwithVY(self, routeU, routeV, iu, iv, totalCost):
        auxRouteU = copy.deepcopy(routeU)
        auxRouteV = copy.deepcopy(routeV)
        u = auxRouteU.get_tour()[iu]
        v = auxRouteV.get_tour()[iv]
        routeUSize = len(routeU.get_tour())
        routeVSize = len(routeV.get_tour())
        # print(u)
        # print(v)
        # pertencem a diferentes rotas
        if u not in auxRouteV.get_tour():
            if iu+1 < routeUSize and iv+1 < routeVSize:
                # print("Não devia entrar aqui")
                listIdOld = [iu, iu+1]
                listNew = [v, routeV.get_tour()[iv+1]]
                costRouteU = auxRouteU.costShiftNodes(
                    listIdOld, listNew, auxRouteU)

                listIdOld = [iv, iv+1]
                listNew = [u, routeU.get_tour()[iu+1]]
                costRouteV = auxRouteV.costShiftNodes(
                    listIdOld, listNew, auxRouteV)

                auxRouteU.popCustomer(iu)
                auxRouteU.insertCustomer(v, iu)
                auxRouteU.popCustomer(iu+1)
                auxRouteU.insertCustomer(routeV.get_tour()[iv+1], iu+1)
                auxRouteU.set_cost(
                    costRouteU[1], costRouteU[2], costRouteU[3])
                
                auxRouteV.popCustomer(iv)
                auxRouteV.insertCustomer(u, iv)
                auxRouteV.popCustomer(iv+1)
                auxRouteV.insertCustomer(routeU.get_tour()[iu+1], iv+1)
                auxRouteV.set_cost(
                    costRouteV[1], costRouteV[2], costRouteV[3])

                newCost = totalCost - routeU.get_totalCost() - routeV.get_totalCost() + \
                    costRouteU[0] + costRouteV[0]

                if newCost < totalCost:
                    return newCost, auxRouteU, auxRouteV
        # pertencem a mesma rota
        else:
            maximum = max(iu, iv)
            minor = min(iu, iv)
            if maximum+1 < routeUSize and minor+1 < maximum:
                aux1 = [iu, iu+1]
                aux2 = [iv, iv+1]
                costRouteU = auxRouteU.costShiftNodesSameRoute(
                    aux1, aux2, auxRouteU)  # [custo total, rota]
                auxRouteU = costRouteU[1]

                auxRouteV = copy.deepcopy(auxRouteU)

                newCost = totalCost - routeU.get_totalCost() + \
                    costRouteU[0]

                if newCost < totalCost:
                    return newCost, auxRouteU, auxRouteV

        return totalCost, routeU, routeV

    '''
    Método troca cliente (u,x) e (v,y) por (u,v) e (x,y), se  Se T(u) == T(v)
    @return novo custo, nova rotaU, nova rotaV
    '''

    def replaceUXandVYwithUVandXYsameTrip(self, routeU, routeV, iu, iv, totalCost):
        auxRouteU = copy.deepcopy(routeU)
        auxRouteV = copy.deepcopy(routeV)
        u = auxRouteU.get_tour()[iu]
        v = auxRouteV.get_tour()[iv]
        routeUSize = len(routeU.get_tour())
        # print(u)
        # print(v)
        # pertencem a mesma rota
        if u in auxRouteV.get_tour():
            def minor(x, y): return x if x < y else y
            def maximum(x, y): return x if x > y else y
            max = maximum(iu, iv)
            min = minor(iu, iv)
            if max+1 < routeUSize and min+1 < max:
                aux1 = [iu, iu+1]
                replaceWith1 = [u, v]
                # print("aux1")
                # print(aux1)
                # print("replaceWith1")
                # print(replaceWith1)
                aux2 = [iv, iv+1]
                replaceWith2 = [
                    routeU.get_tour()[iu+1], routeU.get_tour()[iv+1]]
                # print("aux2")
                # print(aux2)
                # print("replaceWith2")
                # print(replaceWith2)
                costRouteU = auxRouteU.costReplaceNodes(
                    auxRouteU, aux1, replaceWith1, aux2, replaceWith2)  # [custo total,rota]
                auxRouteU = costRouteU[1]
                auxRouteV = copy.deepcopy(auxRouteU)

                newCost = totalCost - routeU.get_totalCost() + \
                    costRouteU[0]

                if newCost < totalCost:
                    return newCost, auxRouteU, auxRouteV

        return totalCost, routeU, routeV

    '''
    Método troca cliente (u,x) e (v,y) por (u,v) e (x,y), se  Se T(u) != T(v)
    @return novo custo, nova rotaU, nova rotaV
    '''

    def replaceUXandVYwithUVandXYdifTrip(self, routeU, routeV, iu, iv, totalCost):
        auxRouteU = copy.deepcopy(routeU)
        auxRouteV = copy.deepcopy(routeV)
        u = auxRouteU.get_tour()[iu]
        v = auxRouteV.get_tour()[iv]
        routeUSize = len(routeU.get_tour())
        routeVSize = len(routeV.get_tour())
        # print(u)
        # print(v)
        # não pertencem a mesma rota
        if u not in auxRouteV.get_tour():
            if iu+1 < routeUSize and iv+1 < routeVSize:
                aux1 = [iu, iu+1]
                replaceWith1 = [u, v]
                aux2 = [iv, iv+1]
                replaceWith2 = [
                    routeU.get_tour()[iu+1], routeV.get_tour()[iv+1]]
                # print("aux2")
                # print(aux2)
                # print("replaceWith2")
                # print(replaceWith2)
                costRouteU = auxRouteU.costReplaceNodes(
                    auxRouteU, aux1, replaceWith1)  # [custo total,rota]
                auxRouteU = costRouteU[1]

                costRouteV = auxRouteV.costReplaceNodes(
                    auxRouteV, aux2, replaceWith2)  # [custo total,rota]
                auxRouteV = costRouteV[1]

                newCost = totalCost - routeU.get_totalCost() - routeV.get_totalCost() + \
                    costRouteU[0] + costRouteV[0]

                if newCost < totalCost:
                    return newCost, auxRouteU, auxRouteV

        return totalCost, routeU, routeV

    '''
    Método troca cliente (u,x) e (v,y) por (u,y) e (x,v), se  Se T(u) != T(v)
    @return novo custo, nova rotaU, nova rotaV
    '''

    def replaceUXandVYwithUYandXVdifTrip(self, routeU, routeV, iu, iv, totalCost):
        auxRouteU = copy.deepcopy(routeU)
        auxRouteV = copy.deepcopy(routeV)
        u = auxRouteU.get_tour()[iu]
        v = auxRouteV.get_tour()[iv]
        routeUSize = len(routeU.get_tour())
        routeVSize = len(routeV.get_tour())
        # print(u)
        # print(v)
        # não pertencem a mesma rota
        if u not in auxRouteV.get_tour():
            if iu+1 < routeUSize and iv+1 < routeVSize:
                aux1 = [iu, iu+1]
                replaceWith1 = [
                    u, routeV.get_tour()[iv+1]]
                aux2 = [iv, iv+1]
                replaceWith2 = [
                    routeU.get_tour()[iu+1], v]
                # print("aux2")
                # print(aux2)
                # print("replaceWith2")
                # print(replaceWith2)
                costRouteU = auxRouteU.costReplaceNodes(
                    auxRouteU, aux1, replaceWith1)  # [custo total,rota]
                auxRouteU = costRouteU[1]

                costRouteV = auxRouteV.costReplaceNodes(
                    auxRouteV, aux2, replaceWith2)  # [custo total,rota]
                auxRouteV = costRouteV[1]

                newCost = totalCost - routeU.get_totalCost() - routeV.get_totalCost() + \
                    costRouteU[0] + costRouteV[0]

                if newCost < totalCost:
                    return newCost, auxRouteU, auxRouteV

        return totalCost, routeU, routeV
