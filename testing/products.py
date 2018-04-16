from handler.products import ProductsHandler as p

dictionary = p().getAllProducts()

for x in dictionary:
    print(x)