from dao.formOptions import FormDao as f

list = f().getAllCarMakes()
models = f().getAllCarModels()

# for x in list:
#     print('<option value="' + str(x['make']) + '">' + str(x['make']) + '</option>')


# for x in list:
#     makeId= x['make_id']
#     print("cars[" + str(x['make']) + "] = new Array(", end="")
#     for y in models:
#         if makeId == y['make_id']:
#             print('"' + y['model'] + '", ', end="")
#     print(");", end="")
#     print()