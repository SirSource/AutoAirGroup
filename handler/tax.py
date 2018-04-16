from dao.tax import TaxDao

class TaxHandler:

    def getAllUsers(self):
        dao = TaxDao()
        list = dao.getTax()
        return list