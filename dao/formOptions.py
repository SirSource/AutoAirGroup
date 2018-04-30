from config.dbconfig import client


class FormDao:

    def __init__(self):
        self.db = client.AutoAirGroupdb

    def getAllCarMakes(self):
        cars = self.db.car_make
        carMakes = []
        for doc in cars.find():
            carMakes.append(doc)
        return carMakes

    def getAllCarModels(self):
        cars = self.db.car_model
        models = []
        for doc in cars.find():
            models.append(doc)
        return models