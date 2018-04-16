from handler.products import ProductsHandler as p

dictionary = p().getAllProducts()
list = []

for x in dictionary:
    print(x)