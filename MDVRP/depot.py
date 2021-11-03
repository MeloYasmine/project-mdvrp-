import config


class Depot:

    def __init__(self):
        self._id = ""
        self._x_coord = 0.0
        self._y_coord = 0.0
        self._durationRoute = 0.0
        self._numberVehicles = 0
        self._loadVehicle = 0.0
        self._loadTotal = 0.0

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_x_coord(self):
        return self._x_coord

    def get_y_coord(self):
        return self._y_coord

    def set_xy_coord(self, x, y):
        self._x_coord = x
        self._y_coord = y

    def get_durationRoute(self, soft=False):
        if config.SOFT_DURATION:
            return self._durationRoute*2
        return self._durationRoute

    def get_durationTotal(self):
        if config.SOFT_DURATION:
            return self._durationRoute*2
        return self._durationRoute * self._numberVehicles

    def set_durationRoute(self, d):
        self._durationRoute = d

    def get_numberVehicles(self):
        if config.SOFT_VEHICLES:
            return self._numberVehicles*2
        return self._numberVehicles

    def set_numberVehicles(self, v):
        self._numberVehicles = v

    def get_loadVehicle(self):
        return self._loadVehicle

    def set_loadVehicle(self, l):
        self._loadVehicle = l

    def get_loadTotal(self):
        return self._loadTotal

    def set_loadTotal(self, l):
        self._loadTotal = l

    def __eq__(self, other_depot):
        return self._id == other_depot.get_id()

    def __str__(self):
        return "id: " + str(self._id) + "  coord: " + str(self._x_coord) + ".." + str(self._y_coord) + "  loadTotal: " + str(self._loadTotal) + "  vehicles: " + str(self._numberVehicles)

    def __repr__(self):
        return str(self._id)
