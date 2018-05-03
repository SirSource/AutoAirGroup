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
        """
        Returns all the products available in the database
        :return:
        TESTED: YES: WORKS
        """
        dao = ProductsDao()
        list = dao.getAllProducts()
        result_list = []
        for row in list:
            result = self.products_dictionary(row)
            result_list.append(result)
        return result_list

    # Returns the ID of the product by entering the name of the product
    # author: Luis Perez
    # TESTED: YES; IT WORKS
    def getProductIDbyName(self, pname):
        dao = ProductsDao()
        list = dao.getProductIDbyName(pname)
        result_list = []
        for row in list:
            result_list.append(row)
        return result_list

    def getProductByID(self, pid):
        if not self.productExistByID(pid):
            return False, None, 'no_product'
        return True, ProductsDao().getProductByID(pid), 'product_exists'

    def getProductQty(self, pid):
        qty = ProductsDao().getProductQty(pid)
        print(qty)

    def getProductInfoByProductName(self, pname):
        """
        Returns Information of product by searching its product name
        :param pname:
        :return:
        TESTED: YES: IT WORKS
        """
        dao = ProductsDao()
        list = dao.getProductByName(pname)
        result_list = []
        for row in list:
            result = self.products_dictionary(row)
            result_list.append(result)
        return result_list

    # returns all the car make available in the db
    # author: Luis Perez
    # TESTED: YES WORKS
    def getAllCarMake(self):
        dao = ProductsDao()
        list = dao.getCarMake()
        result_list = []
        for row in list:
            result_list.append(row)
        return result_list

    # returns all the car model available in the db
    # author: Luis Perez
    # TESTED: YES WORKS
    def getAllCarModel(self):
        dao = ProductsDao()
        list = dao.getCarModel()
        result_list = []
        for row in list:
            result_list.append(row)
        return result_list

    # returns all the car year available in the db
    # author: Luis Perez
    # TESTED: YES WORKS
    def getAllCarYear(self):
        dao = ProductsDao()
        list = dao.getCarYear()
        result_list = []
        for row in list:
            result_list.append(row)
        return result_list

    # returns all the car motor available in the db
    # author: Luis Perez
    # TESTED: YES WORKS
    def getAllCarMotor(self):
        dao = ProductsDao()
        list = dao.getCarMotor()
        result_list = []
        for row in list:
            result_list.append(row)
        return result_list

    # Returns product info by car make, car model, car year, car motor
    # author: Luis Perez
    def searchProductsByCar(self, args):

        dao = ProductsDao()
        # TESTED: YES; works
        if (len(args) == 4):
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
        elif len(args) == 3:
            cmake = args[0]
            cmodel = args[1]
            cyear = args[2]
            plist = dao.getProductByMakeModelYear(cmake, cmodel, cyear)
            result_list = []
            for row in plist:
                result = self.products_dictionary(row)
                result_list.append(result)
            return result_list

        # TESTED: YES; works
        elif (len(args) == 2):
            cmake = args[0]
            cmodel = args[1]

            plist = dao.getProductByCarMakeModel(cmake, cmodel)
            result_list = []
            for row in plist:
                result = self.products_dictionary(row)
                result_list.append(result)
            return result_list
        # TESTED: YES
        elif (len(args) == 1):
            cmake = args[0]
            plist = dao.getProductByCarMake(cmake)
            result_list = []
            for row in plist:
                result = self.products_dictionary(row)
                result_list.append(result)
            return result_list

    def getQuantityByIDAndLocation(self, pid, plocation):
        """
        Returns the quantity of the product by its id and location
        author: Luis Perez
        TESTED: YES WORKS
        :param pid:
        :param plocation:
        :return:
        """
        dao = ProductsDao()

        return dao.getQtyByIDandLocation(pid, plocation)

    def getInfoForCheckout(self, pid):
        """

        :param pid:
        :return:
        TESTED: NO
        """
        dao = ProductsDao()
        checkoutList = dao.getInfoForCheckout(pid)
        result_list = []
        for row in checkoutList:
            result = self.products_dictionary(row)
            result_list.append(result)
        return result_list

    def addProduct(self, image, form):
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
        cmake = form['cmake']
        cmodel = form['cmodel']
        cyear = form['cyear']
        cmotor = form['cmotor'].upper()
        pid = form['pid'].upper()
        pcategory = form['category']
        pname = form['pname']
        pdetails = form['description']
        plocation = form['store']
        pprice = form['pprice']
        pbrand = form['pbrand']
        pshipping = form['pshipping']
        qty = form['qty']
        featured = form['featured']

        if cmake == '' or cmodel == '' or cyear == '' or cmotor == '' or pid == '' or pcategory == '' or pname == '' or pdetails == '' or plocation == '' or pprice == '' or pbrand == '' or qty == '' or pshipping == '' or featured == '':
            return False, None, 'invalid_form'
        if not qty.isdigit():
            return False, None, 'invalid_form'

        qty = int(qty)

        try:
            pprice = float(pprice)
            pshipping = float(pshipping)
        except:
            return False, None, 'invalid_form'

        if image == '':
            image = 'no_photo.png'

        dao = ProductsDao()

        if dao.productExistByID(pid):
            return False, None, 'product_exists'
        else:
            product = dao.insertProduct(image, cmake, cmodel, cyear, cmotor, pid, pcategory, pname, pdetails, plocation,
                                        pprice,
                                        pbrand, qty, pshipping, featured)
            return True, product, 'product_added'

    def updateProductQtyByLocation(self, pid, plocation, qty):
        """

        :param pid:
        :param plocation:
        :param qty:
        :return:
        TESTED: NO
        """
        dao = ProductsDao()
        p = dao.productExistByIDAndLocation(pid, plocation)
        try:
            if p['pid'] == pid:
                try:
                    pass
                except:
                    pass
        except:
            pass

    def updateProductQtyInEveryLocation(self, pid, qty):
        """

        :param pid:
        :param qty:
        :return:
        TESTED: NO
        """
        dao = ProductsDao()
        p = dao.productExistByID(pid)
        try:
            if p['pid'] == pid:
                try:
                    pass
                except:
                    pass
        except:
            pass

    def updateProductImage(self, pid):
        """

        :param pid:
        :return:
        TESTED: NO
        """
        dao = ProductsDao()
        p = dao.productExistByID(pid)
        try:
            if p['pid'] == pid:
                try:
                    pass
                except:
                    pass
        except:
            pass

    def updateAllProductAttributes(self, image, cmake, cmodel, cyear, cmotor, pid, pcategory, pname, pdetails,
                                   plocation, pprice, pbrand, qty):
        pass

    def deleteProductByID(self, pid):
        """
        Deletes the product by its id. First it verifies that it exist

        :param pid:
        :return:
        TESTED: YES
        """
        dao = ProductsDao()
        p = dao.productExistByID(pid)
        try:
            if p['pid'] == pid:
                try:
                    dao.deleteProductByID(pid)
                    return True
                except:
                    return False


        except:
            return False

    def deleteProductByIDAndLocation(self, pid, plocation):
        """
        :param pid:
        :param plocation:
        :return:
        TESTED: YES
        """

        dao = ProductsDao()
        p = dao.productExistByIDAndLocation(pid, plocation)
        try:
            if p['pid'] == pid and p['plocation'] == plocation:

                try:
                    dao.deleteProductByIDAndLocation(pid, plocation)
                    return True
                except:
                    return False
        except:
            return False

    #--Auxiliary Functions--#
    def productExistByID(self, pid):
        product = ProductsDao().productExistByID(pid)
        if product == None:
            return False
        return True