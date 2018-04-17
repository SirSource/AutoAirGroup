from bson import Decimal128

from dao.staff import StaffDao as s
from config.dbconfig import client as db
import bson


# s().insertStaff('Gustavo', 'Marrero', 'AAG1', True, 'gustavo.marrero1@upr.edu', 'gamar123', 'Rio Piedras')



db.AutoAirGroupdb.products.insert_one({'image': "", "pid":"1", "pcategory": "Compressor", "pname":"algarete", "pdetails": "das", "plocation": "baya,on", "pprice": Decimal128('5.99'), "pbrand":"Apple","qty": 23})
