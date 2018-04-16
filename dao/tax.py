from config.dbconfig import client


class TaxDao:
    def __init__(self):
        self.db = client.AutoAirGroupdb.tax

    def getTax(self):
        tax = self.db
        return tax