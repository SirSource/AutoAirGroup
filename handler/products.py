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

    def product_id_dictionary(self,row):
        pid = row['pid']
        result = {*pid,*row}
        return result

    def getAllProducts(self):
        dao = ProductsDao()
        list = dao.getAllProducts()
        result_list = []
        for row in list:
            result = self.products_dictionary(row)
            result_list.append(result)
        return jsonify(Products=result_list)

    #Returns the ID of the product by entering the name of the product
    def getProductIDbyName(self,pname):
        dao = ProductsDao()
        list = dao.getProductIDbyName(pname)
        result_list = []
        for row in list:
           result = self.product_id_dictionary(row)
           result_list.append(result)
        return jsonify(Products = list)


