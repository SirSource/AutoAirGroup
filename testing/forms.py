from dao.formOptions import FormDao as f
from utilities.sendmail import Sendmail as s

# list = f().getAllCarMakes()
# models = f().getAllCarModels()

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


# hello = s().sendAccountCreationEmail('jcd_fusion@hotmail.com')
# print(hello)

from handler.passReset import PassResetHandler as pr
form = 'test@email.com'
pr().resetPassword(form)
#pr().getReset(form)