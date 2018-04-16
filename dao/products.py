from config.dbconfig import client


class ProductsDao:

    def __init__(self):
        self.db = client.AutoAirGroupdb.products

    def getAllProducts(self):
        allProducts = []
        products = self.db
        for doc in products.find():
            allProducts.append(doc)
        return allProducts

    def getAllProductsByCategory(self, category):
        allProducts = []
        products = self.db
        for doc in products.find({"pcategory": category}):
            allProducts.append(doc)
        return allProducts

    def getAllProductsByBrand(self, brand):
        allProducts = []
        products = self.db
        for doc in products.find({"pbrand": brand}):
            allProducts.append(doc)
        return allProducts

    def getProductByID(self, pid):
        products = self.db
        p = []
        for doc in products.find({"pid": pid}):
            p.append(doc)
        return p

    def getProductIDbyName(self, pname):
        products = self.db
        pid = []
        for doc in products.find({'pname': pname}, {'pid': 1, '_id': 0}):
            pid.append(doc)
        return pid

    # Returns all the car make available in the db
    def getCarMake(self):
        products = self.db
        cm = []
        for doc in products.find({}, {'car.make': 1}):
            cm.append(doc)
        return cm

    # Returns all the car model available in the db
    def getCarModel(self):
        products = self.db
        cm = []
        for doc in products.find({}, {'car.model': 1}):
            cm.append(doc)
        return cm

    # Returns all the car years available in the db
    def getCarYear(self):
        products = self.db
        cy = []
        for doc in products.find({}, {'car.year': 1}):
            cy.append(doc)
        return cy

    # Returns all the car motors available in the db
    def getCarMotor(self):
        products = self.db
        cm = []
        for doc in products.find({}, {'car.motor': 1}):
            cm.append(doc)
        return cm

    # Returns the product information by searching the car make, car model,
    # car year, and car motor
    def getProductsByCar(self, cmake, cmodel, cyear, cmotor):
        products = self.db
        p = []
        for doc in products.find({'car.make': cmake, 'car.model': cmodel, 'car.year': cyear, 'car.motor': cmotor},
                                 {'car.make': 0, 'car.model': 0, 'car.year': 0, 'car.motor': 0}):
            p.append(doc)

        return p
