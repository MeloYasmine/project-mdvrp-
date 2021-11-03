'''
Arquivo responsável por armazenar dados de todos os clientes
@author Fabiana Barreto Pereira
'''

from customer import Customer


class Customers:
    _customersList={}

    def addCustomers(rd):
        clist=[]
        for i in range(rd.get_numberCustomers()):
            dataCustomer = rd.get_dataCustomers()[i].split()
            nColumn =len(dataCustomer)
            cst = Customer()
            cst.set_id(int(dataCustomer[0]))
            cst.set_xy_coord(float(dataCustomer[1]),float(dataCustomer[2]))
            cst.set_service(float(dataCustomer[3]))
            cst.set_demand(float(dataCustomer[4]))
            cst.set_beginTimeWindow(float(dataCustomer[(nColumn-2)]))
            cst.set_endTimeWindow(float(dataCustomer[(nColumn-1)]))

            clist.append((dataCustomer[0],cst))

        Customers._customersList=dict(clist)

    def get_customersList():
        return Customers._customersList
