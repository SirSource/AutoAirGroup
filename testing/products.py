from handler.products import ProductsHandler as p
import pymongo
from config.dbconfig import client
from dao.products import ProductsDao as p

# search

# print(p().getProductQty('EV93x678PFC'))
collection = client.AutoAirGroupdb.products
search_this_string = 'Wrangler'
#collection.create_index([('pdetails','text')])
products = p().genericProductSearch(search_this_string)
print(len(products))

# for doc in collection.find({'car.year':search_this_string}, {"_id": 0}):
#     products.append(doc)
#     print()
# "image": image,
#             "car": car,
#             "pid": pid,

#  "make": cmake,
#             "model": cmodel,
#             "year": cyear,
#             "motor": cmotor
print(products)

# deleteTest =['234DDDD','Guaynabo']
# print(p().deleteProductByIDAndLocation(deleteTest[0],deleteTest[1]))
# deleteTest =['234']
# print(p().deleteProductByID(deleteTest[0]))

# def printProducts(products, i):
#
#     print(str(i)+') product id: ' + str(products['pid']))
#     print('product category ' + str(products['pcategory']))
#     print('product name: ' + str(products['pname']))
#     print('product brand: ' + str(products['pbrand']))
#     print('product details: ' + str(products['pdetails']))
#     print('Car:' + str('\n\tmake: ') + products['make'] + '\n\tmodel: '
#           + products['model'] + '\n\tyear: ' + str(products['year'])
#           + '\n\tmotor: ' + str(products['motor']))
#     print('product location: ' + str(products['plocation']))
#     print('product price: ' + str(products['pprice']))
#     print('quantity: ' + str(products['qty'])+'\n')


########################################################################################################################
#                                           GET ALL PRODUCTS
########################################################################################################################

# print('=================================\nAll the products in the database\n=================================\n')
#
# products = p().getAllProducts()
# i =1
# for doc in products:
#     printProducts(doc,i)
#     i = i +1


########################################################################################################################


########################################################################################################################
#                                           GET PRODUCT  ID BY PRODUCT NAME
########################################################################################################################

# print('=================================\nProduct ID in the database\n=================================\n')
#
# pname = 'VW Compressor'
# products = p().getProductIDbyName(pname)
# for doc in products:
#     print("Product ID of " +pname + ": "+str(doc['pid']))

########################################################################################################################


########################################################################################################################
#                                           GET PRODUCT INFO BY PRODUCT NAME
########################################################################################################################

# print('\n=================================\nProduct ID in the database\n=================================\n')
#
# pname = 'VW Compressor'
# products = p().getProductInfoByProductName(pname)
# i = 1
# for doc in products:
#     printProducts(doc,i)
#     i= i+1

########################################################################################################################


########################################################################################################################
#                                           GET ALL CAR MAKES
########################################################################################################################

# print('\n=================================\nCAR MAKES in the database\n=================================\n')
#
# carMakes = p().getAllCarMake()
# print("Car makes:")
# for make in carMakes:
#     print('\t\t'+make)

########################################################################################################################


########################################################################################################################
#                                           GET ALL CAR MODELS
########################################################################################################################

# print('\n=================================\nCAR MODELS in the database\n=================================\n')
#
# carModels = p().getAllCarModel()
# print("Car models:")
# for model in carModels:
#     print('\t\t'+model)

########################################################################################################################


########################################################################################################################
#                                           GET ALL CAR YEAR
########################################################################################################################

# print('\n=================================\nCAR YEAR in the database\n=================================\n')
#
# carYears = p().getAllCarYear()
# print("Car years:")
# for year in carYears:
#     print('\t\t'+year)

########################################################################################################################


########################################################################################################################
#                                           GET ALL CAR MOTOR
########################################################################################################################

# print('\n=================================\nCAR MOTOR in the database\n=================================\n')
#
# carMotor = p().getAllCarMotor()
# print("Car motors:")
# for motor in carMotor:
#     print('\t\t'+motor)

########################################################################################################################


########################################################################################################################
#                                           GET QUANTITY BY PRODUCT ID AND LOCATION
########################################################################################################################

# print('\n=====================================\nQUANTITY OF PRODUCT in the database\n=====================================\n')
#
# pid = '234DDDA'
# plocation = 'Guaynabo'
# quantity = p().getQuantityByIDAndLocation(pid,plocation)
# print("Product quantity of " + pid + " in "+ plocation + ": "+str(quantity['qty']))


########################################################################################################################


########################################################################################################################
#                                           SEARCH PRODUCT BY CAR
########################################################################################################################

# print('\n=====================================\nPRODUCT BY CAR in the database\n=====================================\n')
#
# pid = '234DDDA'
#
# cmake = 'VW'
# cmodel = 'Vanagon'
# cyear = 1986
# cmotor = 'VW1986'
# car =[cmake,cmodel,cyear,cmotor]
#
# products = p().searchProductsByCar(car)
# i =1
# for doc in products:
#     printProducts(doc,i)
#     i=i+1
#
#
# #Using only cmake cmodel, and cyear
# print("\nSEARCH PRODUCT BY CAR MAKE, CAR MODEL, AND CAR YEAR\n")
# cmake = 'BMW'
# cmodel = 'M3'
# cyear = 2018
# car =[cmake,cmodel,cyear]
#
# products = p().searchProductsByCar(car)
# i =1
# for doc in products:
#     printProducts(doc,i)
#     i=i+1
#
# #Using only cmake cmodel
# print("\nSEARCH PRODUCT BY CAR MAKE, CAR MODEL\n")
# cmake = 'Hyundai'
# cmodel = 'Tucson'
# car =[cmake,cmodel]
#
# products = p().searchProductsByCar(car)
# i =1
# for doc in products:
#     printProducts(doc,i)
#     i=i+1


########################################################################################################################
