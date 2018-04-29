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

    def getProductByName(self, pname):
        """

        :param pname:
        :return:
        """
        products = self.db
        p = []
        for doc in products.find({"pname": pname}):
            p.append(doc)
        return p

    # Returns the product ID based on product name
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
        for doc in products.distinct('car.make'):
            cm.append(doc)
        return cm

    # Returns all the car model available in the db
    # author: Luis Perez
    # tested:YES
    def getCarModel(self):
        products = self.db
        cm = []
        for doc in products.distinct('car.model'):
            cm.append(doc)
        return cm

    # Returns all the car years available in the db
    # author: Luis Perez
    # tested:YES
    def getCarYear(self):
        products = self.db
        cy = []
        for doc in products.distinct('car.year'):
            cy.append(str(doc))
        return cy

    # Returns all the car motors available in the db
    # author: Luis Perez
    # TESTED:YES
    def getCarMotor(self):
        products = self.db
        cm = []
        for doc in products.distinct('car.motor'):
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

    # Returns the product information based on car make and model
    # author: Luis Perez
    # tested:YES
    def getProductByCarMakeModel(self, cmake, cmodel):
        products = self.db
        p = []
        for doc in products.find({'car.make': cmake, 'car.model': cmodel}):
            p.append(doc)
        return p

    def getProductByCarYear(self, cyear):
        """
         Returns the product information based on car year
         author: Luis Perez
        tested:NO
        :param cyear: car year
        :return: returns the product information by year of the car
        """
        products = self.db
        p = []
        for doc in products.find({'car.year': cyear}):
            p.append(doc)
        return p

    def getProductByCarMake(self, cmake):
        """

        :param cmake:
        :return:
        """
        products = self.db
        p = []
        for doc in products.find({'car.make': cmake}):
            p.append(doc)
        return p

    def getInfoForCheckout(self, pid):
        """
        Returns the information when a user checks out in the shopping cart
        Author: Luis Perez
        :param pid:
        :return: Returns the
        """
        checkout = []
        for doc in self.db.find({'pid': pid}, {'pid': 1, 'pname': 1, 'pprice': 1, '_id': 0}):
            checkout.append(doc)
        return checkout

    def productExistByMany(self, cmake, cmodel, cyear, cmotor, pid, plocation):
        """

        :param pid:
        :param pname:
        :param plocation:
        :return:
        """
        products = self.db
        p = products.find_one({'car.make': cmake,
                              'car.model': cmodel,
                              'car.year': cyear,
                              'car.motor': cmotor,
                              'pid': pid,
                              'plocation': plocation})
        return p

    def getQtyByIDandLocation(self, pid, plocation):

        return self.db.find_one({'pid': pid, 'plocation': plocation}, {'qty': 1, '_id': 0})

    def productExistByID(self, pid):
        """
        Returns if a product exist by its id
        :param pid:
        :return:
        TESTED: NO
        """
        products = self.db
        p = products.find_one({'pid': pid})
        return p

    def productExistByIDAndLocation(self, pid, plocation):
        """

        :param pid:
        :return:
        TESTED: YES
        """
        products = self.db
        p = products.find_one({'pid': pid, 'plocation': plocation})
        return p

    #################################################################################################################
    #       INSERT PRODUCT
    #################################################################################################################

    def insertProduct(self, image, cmake, cmodel, cyear, cmotor, pid, pcategory, pname, pdetails, plocation, pprice,
                      pbrand, qty, pshipping, featured):
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
        # car obect
        car = {
            "make": cmake,
            "model": cmodel,
            "year": cyear,
            "motor": cmotor
        }

        product = {
            "image": image,
            "car": car,
            "pid": pid,
            "pcategory": pcategory,
            "pname": pname,
            "pdetails": pdetails,
            "plocation": plocation,
            "pprice": pprice,
            "pbrand": pbrand,
            "qty": qty,
            "pshipping": pshipping,
            "featured": featured
        }
        return self.db.insert_one(product).inserted_id

    ################################################################################
    #       UPDATE PRODUCT
    ################################################################################

    def updateProductQtyByLocation(self, pid, plocation, qty):
        """
        Updates the qty of the product by location and product id
        :param pid: product id
        :param plocation: location where the product is
        :param qty: quantity update
        :return:
        TESTED: NO
        """
        return self.db.update({'pid': pid, 'plocation': plocation}, {'$set': {'qty': qty}})

    def updateProductById(self, image, cmake, cmodel, cyear, cmotor, pid, pcategory, pname, pdetails, plocation, pprice,
                          pbrand, qty):
        """
        Updates the product by product ID
        author: Luis Perez
        :param image:
        :param cmake:
        :param cmodel:
        :param cyear:
        :param cmotor:
        :param pid:
        :param pcategory:
        :param pname:
        :param pdetails:
        :param plocation:
        :param pprice:
        :param pbrand:
        :param qty:
        :return:
        TESTED NO
        """
        car = {
            "make": cmake,
            "model": cmodel,
            "year": cyear,
            "motor": cmotor
        }

        product = {
            "image": image,
            "car": car,
            "pid": pid,
            "pcategory": pcategory,
            "pname": pname,
            "pdetails": pdetails,
            "plocation": plocation,
            "pprice": pprice,
            "pbrand": pbrand,
            "qty": qty
        }

        return self.db.update({'pid': pid}, {'$set': {'product': product}})

    def deleteProductByID(self, pid):
        """
        Deletes the product by its id
        :param pid:
        :return:
        TESTED NO
        """
        return self.db.delete_many({"pid": pid})

    def deleteProductByIDAndLocation(self, pid, plocation):
        """
        Deletes the product in the specified location
        :param pid:
        :param plocation:
        :return:
        TESTED: YES
        """
        return self.db.delete_many({'pid': pid, 'plocation': plocation})

    def countCategory(self, category):
        count = self.db.count({"pcategory": category})
        return count