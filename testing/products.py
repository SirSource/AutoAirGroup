# from handler.orders import OrdersHandler as o
#
# orders = o().getAllOrders()
# current = orders[0]
#
# productos = current['products']
# cantidad = current['qty']
# del current['products']
# del current['qty']
#
# print(orders)
# print(cantidad)
# print(productos)

from dao.orders import OrdersDao as od
print(od().getOrdersByOrderID(6))