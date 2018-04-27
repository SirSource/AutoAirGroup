from dao.tax import TaxDao
from utilities.valid import Valid as v


class TaxHandler:

    def getTax(self):
        dao = TaxDao()
        list = dao.getTaxs()
        fee = list['fee']
        return fee

    def setTax(self, form):
        tax = form[0]
        dao = TaxDao()
        if not v().isFloat(tax):
            return False
        tax = float(tax) / 100
        return dao.setTax(tax)