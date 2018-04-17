from dao.products import ProductsDao

class ProductsHandler:

    def products_dictionary(self, row):
        car = row['car']
        del row['car']
        del row['_id']
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
        return result_list

    # Returns the ID of the product by entering the name of the product
    # author: Luis Perez
    def getProductIDbyName(self, pname):
        dao = ProductsDao()
        list = dao.getProductIDbyName(pname)
        result_list = []
        for row in list:
            result = self.product_id_dictionary(row)
            result_list.append(result)
        return result_list

    # returns all the car make available in the db
    # author: Luis Perez
    def getAllCarMake(self):
        dao = ProductsDao()
        list = dao.getCarMake()
        result_list = []
        for row in list:
            result = self.product_carInfo_dictionary(row)
            result_list.append(result)
        return result_list

    # returns all the car model available in the db
    # author: Luis Perez
    def getAllCarModel(self):
        dao = ProductsDao()
        list = dao.getCarModel()
        result_list = []
        for row in list:
            result = self.product_carInfo_dictionary(row)
            result_list.append(result)
        return result_list

    # returns all the car year available in the db
    # author: Luis Perez
    def getAllCarYear(self):
        dao = ProductsDao()
        list = dao.getCarYear()
        result_list = []
        for row in list:
            result = self.product_carInfo_dictionary(row)
            result_list.append(result)
        return result_list

    # returns all the car motor available in the db
    # author: Luis Perez
    def getAllCarMotor(self):
        dao = ProductsDao()
        list = dao.getCarMotor()
        result_list = []
        for row in list:
            result = self.product_carInfo_dictionary(row)
            result_list.append(result)
        return result_list

    # Returns product info by car make, car model, car year, car motor
    # author: Luis Perez
    def searchProductsByCar(self, args):

        dao = ProductsDao()
        # TESTED: YES; works
        if (len(args)==4):
            cmake = args[0]
            cmodel = args[1]
            cyear = args[2]
            cmotor = args[3]
            plist = dao.getProductsByCar(cmake, cmodel, cyear, cmotor)
            result_list = []
            for row in plist:
                result = self.products_dictionary(row)
                result_list.append(result)
            return result_list
        # TESTED: YES; works
        elif len(args)==3:
            cmake = args[0]
            cmodel = args[1]
            cyear = args[2]
            print(cmake+" "+cmodel+" "+cyear)
            plist = dao.getProductByMakeModelYear(cmake,cmodel,cyear)
            result_list = []
            for row in plist:
                result = self.products_dictionary(row)
                result_list.append(result)
            return result_list

        # TESTED: YES; works
        elif(len(args)==2):
            cmake = args[0]
            cmodel = args[1]

            plist = dao.getProductByCarMakeModel(cmake, cmodel)
            result_list = []
            for row in plist:
                result = self.products_dictionary(row)
                result_list.append(result)
            return result_list
        # TESTED: YES
        elif(len(args)==1):
            cmake = args[0]
            plist = dao.getProductByCarMake(cmake)
            result_list = []
            for row in plist:
                result = self.products_dictionary(row)
                result_list.append(result)
            return result_list






