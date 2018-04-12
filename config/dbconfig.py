import pymongo
import certifi
import ssl

client = pymongo.MongoClient('mongodb+srv://devUser:AAG2018@cluster0-tomfu.mongodb.net/AutoAirGroupdb',ssl_cert_reqs=ssl.CERT_REQUIRED, ssl_ca_certs=certifi.where())

