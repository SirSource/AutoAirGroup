from handler.orders import OrdersHandler as o
from dao.orders import OrdersDao as od

class OrdersTester:


# cart = [{'EV939678PFC': '2'}, {'CN30024PFC': '4'}, {'FI1173C': '10'}]
#
# o().createOrderfromCart(cart)

    sequence = od().getOrderSequenceNumber()
    sequence = sequence + 1
    od().updateOrderSequenceNumber(sequence)

# print(o().countCompleteOrders())
# order = o().getOrdersByPhone("7875555555")
# print(order)

# def printOrder(item):
#     products = item['products']
#     del item['products']
#     print('---------------')
#     print('Order #:' + str(item['orderid']))
#     print('Name: ' + str(item['ufirst']) + ' ' + str(item['ulast']))
#     print('Email: ' + str(item['uemail']))
#     print('Total: ' + str(item['total']))
#     print('Items Purchased:')
#     for x in products:
#         print('\tProduct ID :' + str(x['pid']))
#         print('\tQuantity: ' + str(x['qty']))
#         print('\tUnit Price: ' + str(x['unit_price']))
#     print('Order Status: ' + str(item['payment_status']))
#     print('Shipping Status: ' + str(item['shipping']))
#     print('Date: ' + str(item['date']))
#     print('Ship to address:')
#     print('\t' + str(item['place']))
#     print('\t' + str(item['street']))
#     print('\t' + str(item['city']) + ' P.R. ' + str(item['zipcode']))
#
# def printAllOrder(orders):
#     for item in orders:
#         products = item['products']
#         del item['products']
#         print('---------------')
#         print('Order #:' + str(item['orderid']))
#         print('Name: ' + str(item['ufirst']) + ' ' + str(item['ulast']))
#         print('Email: ' + str(item['uemail']))
#         print('Total: ' + str(item['total']))
#         print('Items Purchased:')
#         for x in products:
#             print('\t======================')
#             print('\tProduct ID :' + str(x['pid']))
#             print('\tQuantity: ' + str(x['qty']))
#             print('\tUnit Price: ' + str(x['unit_price']))
#         print('Order Status: ' + str(item['payment_status']))
#         print('Shipping Status: ' + str(item['shipping']))
#         print('Date: ' + str(item['date']))
#         print('Ship to address:')
#         print('\t' + str(item['place']))
#         print('\t' + str(item['street']))
#         print('\t' + str(item['city']) + ' P.R. ' + str(item['zipcode']))
#
# print('====================\nOrders in the System:\n====================')
# orders = o().getAllOrders()
# printAllOrder(orders)
# print('====================\nOrders by ID:\n====================')
# control = True
# oid = None
# orden = None
# while (control):
#     oid = input('Enter order ID:')
#     if o().orderExists(oid):
#         orden = o().getOrdersByOrderID(oid)
#         control = False
#     else:
#         print('The order does not exist or incorrect oid!')
# printOrder(orden)
# print('====================\nOrders by email:\n====================')
# control = True
# oid = None
# orden = None
# while (control):
#     email = input('Enter email associated with an order:')
#     if o().emailOrderExists(email):
#         orden = o().getOrdersByEmail(email)
#         control = False
#     else:
#         print('The order does not exist or incorrect email!')
# printAllOrder(orden)
# print('====================\nOrders by status:\n====================')
# status = input('Order Status: ')
# orden = o().getOrdersByStatus(status)
# if not orden:
#     print("No orders with status [" + status + "]")
# else:
#     printAllOrder(orden)
# print('====================\nOrders shipped orders:\n====================')
# orden = o().getOrdersShipped()
# if not orden:
#     print("No orders have shipped")
# else:
#     printAllOrder(orden)
