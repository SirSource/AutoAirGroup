from dao.tax import TaxDao

class TaxHandler:

    def getTax(self):
        dao = TaxDao()
        list = dao.getTax()
        fee = list['fee']
        return fee

    def setTax(self, form):
        tax = form[0]
        dao = TaxDao()
        if not self.isFloat(tax):
            return False
        tax = float(tax)/100
        return dao.setTax(tax)

    #---Validations---#

    def isFloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False