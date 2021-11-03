class Customer:

    def __init__(self):
        self._id = ""
        self._x_coord = 0
        self._y_coord = 0
        self._service = 0
        self._demand = 0
        self._beginTimeWindow = 0
        self._endTimeWindow = 0
        self._depotsDistances = []
        self._neighborsDistances = []


    def get_id(self):
        return self._id

    def set_id(self,id):
        self._id = id

    def get_x_coord(self):
        return self._x_coord

    def get_y_coord(self):
        return self._y_coord

    def set_xy_coord(self,x,y):
        self._x_coord = x
        self._y_coord = y

    def get_service(self):
        return self._service

    def set_service(self,s):
        self._service = s

    def get_demand(self):
        return self._demand

    def set_demand(self,d):
        self._demand = d

    def get_beginTimeWindow(self):
        return self._beginTimeWindow

    def set_beginTimeWindow(self,w):
        self._beginTimeWindow = w

    def get_endTimeWindow(self):
        return self._endTimeWindow

    def set_endTimeWindow(self,c):
        self._endTimeWindow = c

    def get_depotsDistances(self):
        return self._depotsDistances

    def set_depotsDistances(self,depotsDistances):
        self._depotsDistances = depotsDistances

    def get_neighborsDistances(self):
        return self._neighborsDistances

    def set_neighborsDistances(self,neighborsDistances):
        self._neighborsDistances = neighborsDistances

    def __eq__(self,other_customer):
        return self._id == other_customer.get_id()


    def __str__(self):
        return "id: " + str(self._id) + "  coord: " + str(self._x_coord) + ".." + str(self._y_coord) + " demand: " + str(self._demand)

    def __repr__(self):
        return str(self._id)
