from handler.products import ProductsHandler as p
y = ['BMW','M3',2018,'CX222']
dictionary = p().searchProductsByCar(y)

for x in dictionary:
    print(x)



