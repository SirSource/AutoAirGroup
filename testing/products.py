from handler.products import ProductsHandler as p
test = ["BMW","M3"]
test1=["Honda","Civic"]
dictionary = p().searchProductsByCar(test)
for row in dictionary:
    print(row)
# dictionary = p().searchProductsByCar(test1)
# print(dictionary)


from handler.tax import TaxHandler as t

# tax = t().getTax()
# fee = tax['fee']
# print(fee)
