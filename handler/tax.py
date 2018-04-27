from dao.tax import TaxDao
from utilities.valid import Valid as v


class TaxHandler:

    def getTax(self):
        dao = TaxDao()
        list = dao.getTax()
        fee = list['fee']
        return fee

    def setTax(self, form):
        tax = form[0]
        dao = TaxDao()
        if not v().isFloat(tax):
            message = 'error'
            return False, message, tax
        tax = float(tax) / 100
        message = 'ok'
        return dao.setTax(tax), message, self.getTax()
