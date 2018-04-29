from config.dbconfig import client
from dao.products import ProductsDao as p


class CategoryDao:

    def __init__(self):
        self.db = client.AutoAirGroupdb.category

    def getCategories(self):
        allCategories = []
        categories = self.db
        for doc in categories.find():
            allCategories.append(doc)
        return allCategories

    def insertCategoryItem(self, item):
        return self.db.update({'category': item}, {'$set': {'category': item}}, {'upsert': True})

    def deleteCategoryItem(self, item):
        return self.db.delete_many({"category": item})

    def countCategory(self, item):
        return p().countCategory(item)