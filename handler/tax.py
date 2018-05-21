from dao.tax import TaxDao
from utilities.valid import Valid as v


class TaxHandler:

    def getTax(self):
        """
        Fetch tax from database.
        :return: The feee.
        """
        dao = TaxDao()
        list = dao.getTax()
        fee = list['fee']
        return fee

    def setTax(self, form):
        """
        Sets the new tax in the database.
        :param form: The fee from the form.
        :return: Old Tax, message, and the new tax.
        """
        tax = form[0]
        dao = TaxDao()
        if not v().isFloat(tax):
            message = 'error'
            return False, message, tax
        tax = float(tax) / 100
        message = 'ok'
        return dao.setTax(tax), message, self.getTax()
