from flask import jsonify

from dao.products import ProductsDao


class ProductsHandler:

    def products_dictionary(self, row):
        car = row['car']
        del row['car']
        del row['_id']
        del row['image']
        result = {**car, **row}
        return result

    def product_id_dictionary(self, row):
        pid = row['pid']
        result = {*pid, *row}
        return result

    def product_carInfo_dictionary(self, row):
        car = row['car']
        del row['_id']
        result = {**car, **row}
        return result

    # =========================================================#

    def getAllProducts(self):
        dao = ProductsDao()
        list = dao.getAllProducts()
        result_list = []
        for row in list:
            result = self.products_dictionary(row)
            result_list.append(result)
        return jsonify(Products=result_list)

    # Returns the ID of the product by entering the name of the product
    def getProductIDbyName(self, pname):
        dao = ProductsDao()
        list = dao.getProductIDbyName(pname)
        result_list = []
        for row in list:
            result = self.product_id_dictionary(row)
            result_list.append(result)
        return jsonify(Products=list)

    # returns all the car make available in the db
    def getAllCarMake(self):
        dao = ProductsDao()
        list = dao.getCarMake()
        result_list = []
        for row in list:
            result = self.product_carInfo_dictionary(row)
            result_list.append(result)
        return jsonify(CarMake=list)

    # returns all the car model available in the db
    def getAllCarModel(self):
        dao = ProductsDao()
        list = dao.getCarModel()
        result_list = []
        for row in list:
            result = self.product_carInfo_dictionary(row)
            result_list.append(result)
        return jsonify(CarModel=list)

    # returns all the car year available in the db
    def getAllCarYear(self):
        dao = ProductsDao()
        list = dao.getCarYear()
        result_list = []
        for row in list:
            result = self.product_carInfo_dictionary(row)
            result_list.append(result)
        return jsonify(CarYear=list)

    # returns all the car motor available in the db
    def getAllCarMotor(self):
        dao = ProductsDao()
        list = dao.getCarMotor()
        result_list = []
        for row in list:
            result = self.product_carInfo_dictionary(row)
            result_list.append(result)
        return jsonify(CarMotor=list)

    # Returns product info by car make, car model, car year, car motor
    def searchProductsByCar(self, args):
        cmake = args.get('cmake')
        cmodel = args.get('cmodel')
        cyear = args.get('cyear')
        cmotor = args.get('cmotor')

        dao = ProductsDao()
        if (len(args) == 4) and cmake and cmodel and cyear and cmotor:
            plist = dao.getProductsByCar(cmake, cmodel, int(cyear), cmotor)
            result_list = []
            for row in plist:
                result = self.products_dictionary(row)
                result_list.append(result)
            return jsonify(Products=result_list)
