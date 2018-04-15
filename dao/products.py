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
    
    def getProductByID(self,pid):
        products = self.db
        p = []
        for doc in products.find({"pid":pid}):
            p.append(doc)
        return p

    def getProductIDbyName(self, pname):
        products = self.db
        pid = []
        for doc in products.find({'pname': pname},{'pid':1, '_id':0}):
            pid.append(doc)
        return pid
