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

    #Returns the product ID based on product name
    # author: Luis Perez
    # tested:YES
    def getProductIDbyName(self, pname):
        products = self.db
        pid = []
        for doc in products.find({'pname': pname}, {'pid': 1, '_id': 0}):
            pid.append(doc)
        return pid

    # Returns all the car make available in the db
    # author: Luis Perez
    # tested:YES
    def getCarMake(self):
        products = self.db
        cm = []
        for doc in products.find({}, {'car.make': 1}):
            cm.append(doc)
        return cm

    # Returns all the car model available in the db
    # author: Luis Perez
    # tested:YES
    def getCarModel(self):
        products = self.db
        cm = []
        for doc in products.find({}, {'car.model': 1}):
            cm.append(doc)
        return cm

    # Returns all the car years available in the db
    # author: Luis Perez
    # tested:YES
    def getCarYear(self):
        products = self.db
        cy = []
        for doc in products.find({}, {'car.year': 1}):
            cy.append(doc)
        return cy

    # Returns all the car motors available in the db
    # author: Luis Perez
    #TESTED:YES
    def getCarMotor(self):
        products = self.db
        cm = []
        for doc in products.find({}, {'car.motor': 1}):
            cm.append(doc)
        return cm

    # Returns the product information by searching the car make, car model,
    # car year, and car motor
    # author: Luis Perez
    # tested:YES
    def getProductsByCar(self, cmake, cmodel, cyear, cmotor):
        products = self.db
        p = []
        for doc in products.find({'car.make': cmake, 'car.model': cmodel, 'car.year': cyear, 'car.motor': cmotor}):
            p.append(doc)
        return p

    # Returns the product information based on the make of the car, model, and year
    # author: Luis Perez
    # tested:YES
    def getProductByMakeModelYear(self, cmake, cmodel, cyear):
        products = self.db
        p = []
        for doc in products.find({'car.make': cmake, 'car.model': cmodel, 'car.year': cyear}):
            p.append(doc)
        return p

    #Returns the product information based on car make and model
    # author: Luis Perez
    # tested:YES
    def getProductByCarMakeModel(self, cmake, cmodel):
        products = self.db
        p = []
        for doc in products.find({'car.make': cmake, 'car.model': cmodel}):
            p.append(doc)
        return p


    def getProductByCarYear(self,cyear):
        """
         Returns the product information based on car year
         author: Luis Perez
        tested:NO
        :param cyear: car year
        :return: returns the product information by year of the car
        """
        products = self.db
        p = []
        for doc in products.find({'car.year':cyear}):
            p.append(doc)
        return p


    def getProductByCarMake(self, cmake):
        products = self.db
        p = []
        for doc in products.find({'car.make': cmake}):
            p.append(doc)
        return p

    #################################################################################################################
    #       INSERT PRODUCT
    #################################################################################################################

    def insertProduct(self,image,cmake,cmodel,cyear,cmotor,pid,pcategory,pname,pdetails,plocation,pprice,pbrand,qty):
        """

         Inserts a new product to the database
         author: Luis Perez
         TESTED: NO

          :param image: image of the product if any
          :param cmake: car make
          :param cmodel: car model
          :param cyear: car year
          :param cmotor: car motor
          :param pid: product id
          :param pcategory: product category
          :param pname: product name
          :param pdetails:  information about the product if any
          :param plocation: in what store of AutoAirGroup is located
          :param pprice: price of the product
          :param pbrand: brand of the product
          :param qty: quantity of the product in that specific location

         """
        #car object
        car = {
            "make":cmake,
            "model":cmodel,
            "year":cyear,
            "motor":cmotor
        }

        product = {
            "image":image,
            "car":car,
            "pid":pid,
            "pcategory":pcategory,
            "pname":pname,
            "pdetails":pdetails,
            "plocation":plocation,
            "pprice":pprice,
            "pbrand":pbrand,
            "qty":qty
        }
        return self.db.insert_one(product).inserted_id




