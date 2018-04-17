from handler.products import ProductsHandler as p

dictionary = p().getAllProducts()

for x in dictionary:
    print(x)

from handler.tax import TaxHandler as t

tax = t().getTax()
fee = tax['fee']
print(fee)
