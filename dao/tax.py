from config.dbconfig import client


class TaxDao:
    def __init__(self):
        self.db = client.AutoAirGroupdb.tax

    def getTax(self):
        tax = self.db.find_one()
        return tax

    def setTax(self, tax):
        return self.db.update({'fee': self.getTax()['fee']}, {'$set':{'fee': tax}})