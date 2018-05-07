from config.dbconfig import client


class TaxDao:
    def __init__(self):
        self.db = client.AutoAirGroupdb.tax

    def getTax(self):
        """
        Retrieves the tax from the database.
        :return: Tax value from the database.
        """
        tax = self.db.find_one()
        return tax

    def setTax(self, tax):
        """
        Sets the tax value in the database.
        :param tax: New tax value.
        :return: The monodb objectID.
        """
        return self.db.update({'fee': self.getTax()['fee']}, {'$set':{'fee': tax}})