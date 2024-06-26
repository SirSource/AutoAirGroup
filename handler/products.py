from dao.products import ProductsDao
from bson.decimal128 import Decimal128
from utilities.valid import Valid as v


class ProductsHandler:

    def products_dictionary(self, row):
        """
        Creates a list of products to return
        :param row: The array element of a product.
        :return: The list of all products formatted as a dictionary.
        """
        car = row['car']
        del row['car']
        del row['_id']
        result = {**car, **row}
        return result

    def product_id_dictionary(self, row):
        """
        Creates a list of products to return from an id.
        :param row: The array element of a product.
        :return: The list of all products formatted as a dictionary.
        """
        pid = row['pid']
        result = {*pid, *row}
        return result

    def product_carInfo_dictionary(self, row):
        """
        Creates a list of products to return from car information.
        :param row: The array element of a product.
        :return: The list of all products formatted as a dictionary.
        """
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

    def getAllProductsCatalog(self):
        """
        Returns all the products available in the database
        :return:
        TESTED: YES: WORKS
        """
        dao = ProductsDao()
        list = dao.getAllProductsCatalog()
        result_list = []
        for row in list:
            result = self.products_dictionary(row)
            result_list.append(result)
        return result_list

    # Returns the ID of the product by entering the name of the product
    # author: Luis Perez
    # TESTED: YES; IT WORKS
    def getProductIDbyName(self, pname):
        pname = v().removeSpecialChars(pname)
        dao = ProductsDao()
        list = dao.getProductIDbyName(pname)
        result_list = []
        for row in list:
            result_list.append(row)
        return result_list

    def getProductByID(self, pid):
        """
        Fetch a product by the id.
        :param pid: Id of product.
        :return: Boolean, product if any, message.
        """
        pid = v().sanitize(pid)
        if not self.productExistByID(pid):
            return False, None, 'no_product'
        return True, ProductsDao().getProductByID(pid), 'product_exists'

    def getProductQty(self, pid):
        """
        Fetch a product by the quantity.
        :param pid: Id of the product.
        :return: Qty of the product or zero if nothing.
        """
        try:
            qty = ProductsDao().getProductQty(pid)
            return (qty)
        except:
            return 0

    def getProductInfoByProductName(self, pname):
        """
        Returns Information of product by searching its product name
        :param pname:
        :return:
        TESTED: YES: IT WORKS
        """
        pname = v().removeSpecialChars(pname)
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

        # Returns product info by car make, car model, car year, car motor
        # author: Luis Perez

    def searchProductsByCar(self, args):
        """

        :param args:
        :return:
        """
        cmake = args['cmake']
        cmodel = args['cmodel']
        cyear = args['cyear']
        pcategory = args['pcategory']

        dao = ProductsDao()
        # TESTED: YES; works
        if not (cmake == "None" or cmodel == "None" or cyear == "None" or pcategory == "None"):
            try:
                plist = dao.getProductsByCar(cmake, cmodel, cyear, pcategory)
                result_list = []
                for row in plist:
                    result = self.products_dictionary(row)
                    result_list.append(result)
                return True, result_list, 'search_successful'
            except:
                return False, None, 'product_not_found'
        # TESTED: YES; works

        # If user only enters year it will select all product from the car year
        elif cmake == 'None' and cmodel == 'None' and pcategory == 'None' and (not cyear == 'None'):
            try:
                plist = dao.getProductByCarYear(cyear)
                result_list = []
                for row in plist:
                    result = self.products_dictionary(row)
                    result_list.append(result)
                return True, result_list, 'search_successful'
            except:
                return False, None, 'product_not_found'

        # If user only enters product category
        elif cmake == "None" and cmodel == "None" and cyear == "None" and not pcategory == "None":
            try:
                plist = dao.getAllProductsByCategory(pcategory)
                result_list = []
                for row in plist:
                    result = self.products_dictionary(row)
                    result_list.append(result)

                return True, result_list, 'search_successful'

            except:
                return False, None, "product_not_found"

        # If user only enters car make and car model
        elif pcategory == "None" and cyear == "None" and not cmake == "None" and not cmodel == "None":
            try:
                plist = dao.getProductByCarMakeModel(cmake, cmodel)
                result_list = []
                for row in plist:
                    result = self.products_dictionary(row)
                    result_list.append(result)
                return True, result_list, 'search_successful'
            except:
                return False, None, 'product_not_found'

            # If user only enters car make and car model and car year
        elif pcategory == "None" and not cyear == "None" and not cmake == "None" and not cmodel == "None":
            try:
                plist = dao.getProductByMakeModelYear(cmake, cmodel, cyear)
                result_list = []
                for row in plist:
                    result = self.products_dictionary(row)
                    result_list.append(result)
                return True, result_list, 'search_successful'
            except:
                return False, None, "product_not_found"

    def getGenericSearch(self, args):
        """

        :param args:
        :return:
        """
        dao = ProductsDao()
        string = str(args['cmake']) + " " + str(args['cmodel']) + " " + str(args['cyear']) + " " + str(
            args['pcategory'])
        print(len(args))
        print(string)
        plist = dao.getGenericSearch(string)
        result_list = []
        for row in plist:
            result = self.products_dictionary(row)
            result_list.append(result)
        return result_list

    def getGenericSearchCatalog(self, args):
        """

        :param args:
        :return:
        """
        dao = ProductsDao()
        string = str(args)
        plist = dao.getGenericSearchCatalog(string)
        result_list = []

        for row in plist:
            result = self.products_dictionary(row)
            if result['featured'] == 'yes':
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
        cmotor = v().removeSpecialChars(form['cmotor'].upper())
        pid = v().sanitize(form['pid'].upper())
        pcategory = form['category']
        pname = v().removeSpecialChars(form['pname'])
        pdetails = form['description']
        plocation = form['store']
        pprice = form['pprice']
        pbrand = v().removeSpecialChars(form['pbrand'])
        pshipping = form['pshipping']
        qty = v().sanitize(form['qty'])
        featured = form['featured']

        if cmake == '' or cmodel == '' or cyear == '' or cmotor == '' or pid == '' or pcategory == '' or pname == '' or pdetails == '' or plocation == '' or pprice == '' or pbrand == '' or qty == '' or pshipping == '' or featured == '':
            return False, None, 'invalid_form'
        if not qty.isdigit():
            return False, None, 'invalid_form'

        qty = int(qty)

        try:
            pprice = Decimal128(pprice)
            pshipping = Decimal128(pshipping)
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

    def decreaseProductQty(self, pid, qty):
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
                    dao.decreaseProductQty(pid, qty)
                    return True, "update_successful"
                except:
                    return False, "update_not_successful"
        except:
            return False, "no_id_exist"

    def increaseProductQty(self, pid, qty):
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
                    dao.increaseProductQty(pid, qty)
                    return True, "update_successful"
                except:
                    return False, "update_not_successful"
        except:
            return False, "no_id_exist"

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

    # --Auxiliary Functions--#
    def productExistByID(self, pid):
        """
        Check is a product exists.
        :param pid: ID of product.
        :return: True if exists, False if not.
        """
        product = ProductsDao().productExistByID(pid)
        if product == None:
            return False
        return True

    def EditProductByID(self, image, form):
        """
        EDITS ALL FIELDS OF PRODUCTS IF THERE IS ANY CHANGE
        :param form:
        :return:
        """
        cmake = form['cmake']
        cmodel = form['cmodel']
        cyear = form['cyear']
        cmotor = v().removeSpecialChars(form['cmotor'].upper())
        pid = v().sanitize(form['pid'].upper())
        pcategory = form['category']
        pname = v().removeSpecialChars(form['pname'])
        pdetails = form['description']
        plocation = form['store']
        pprice = form['pprice']
        pbrand = v().removeSpecialChars(form['pbrand'])
        pshipping = form['pshipping']
        qty = v().sanitize(form['qty'])
        featured = form['featured']
        if image == None:
            try:

                if cmake == '' or cmodel == '' or cyear == '' or cmotor == '' or pid == '' or pcategory == '' or pname == '' or pdetails == '' or plocation == '' or pprice == '' or pbrand == '' or qty == '' or pshipping == '' or featured == '':
                    return False, None, 'invalid_form'
                if not qty.isdigit():
                    return False, None, 'invalid_form'

                dao = ProductsDao()
                product = dao.updateProductByIdWithSameImage(cmake, cmodel, cyear, cmotor, pid, pcategory, pname,
                                                             pdetails, plocation, Decimal128(pprice), pbrand, int(qty),
                                                             Decimal128(pshipping), featured)
                return bool(product['updatedExisting']), product, 'update_successful'

            except:
                return False, None, 'update_not_successful'
        else:
            try:
                dao = ProductsDao()
                product = dao.updateProductByIdWithDiffImage(image, cmake, cmodel, cyear, cmotor, pid, pcategory, pname,
                                                             pdetails, plocation, Decimal128(pprice), pbrand, int(qty),
                                                             Decimal128(pshipping), featured)
                return bool(product['updatedExisting']), product, 'update_successful'

            except:
                return False, None, 'update_not_successful'

    def genericProductSearch(self, string):
        """
        Create a generic search from a query.
        :param string: Query
        :return: Search results.
        """
        return ProductsDao().genericProductSearch(string)

    def productQtyAvailable(self, pid, qty):
        """
        Check if a product is available.
        :param pid: ID of product.
        :param qty: Quantity of product to check availability.
        :return: True if enough, False if not.
        """
        dao = ProductsDao()
        product = dao.getProductByID(pid)
        print(product)
        pQty = product[0]['qty']
        print('qty: ' + str(qty) + ' pQty: ' + str(pQty) + " result = " + str(pQty - qty))
        if (pQty - qty) < 0:
            return False
        else:
            return True
