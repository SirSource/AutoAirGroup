import sendgrid
from sendgrid.helpers.mail import *

# ======= ENVIAR EMAIL =========== #
'''    #No perder el apikey !!!!
sg = sendgrid.SendGridAPIClient(apikey='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')
from_email = Email("gustavodev@live.com")  #Email de origen
to_email = Email("gustavo.marrero1@upr.edu")   # El destinatario
subject = "Auto Air Group Order Details"
content = Content("text/plain", "Your order number is...")
mail = Mail(from_email, subject, to_email, content)
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)
'''


class SendMail:

    def __init__(self):
        self.sg = sendgrid.SendGridAPIClient(
            apikey='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')
        self.from_email = Email("info@autoair.io")

    def sendAccountCreationEmail(self, userEmail):
        to_email = Email(userEmail)
        subject = "!Bienvenido a Auto Air Group!"
        content = Content("text/html",
                          "<html><h1>!Gracias por crear una cuenta con Auto Air Group!</h1> <h3>Desde su cuenta puede ver el historial de compras y tener un récord para sus recibos.</h3></html>")
        mail = Mail(self.from_email, subject, to_email, content)
        response = self.sg.client.mail.send.post(request_body=mail.get())
        return response

    def sendAccountRecoverEmail(self, userEmail, code):
        to_email = Email(userEmail)
        subject = "Recuperar Acceso a su Cuenta"
        content = Content("text/html",
                          'Para recuperar acceso a su cuenta haga clic en el enlace: <html>https://autoair.io/user/reset/password/'+str(
                              code)+'</html> Recuperar acceso')
        mail = Mail(self.from_email, subject, to_email, content)
        response = self.sg.client.mail.send.post(request_body=mail.get())
        print("recovery pass")
        return response

    def sendOrderConfirmationEmail(self, userEmail, orderNum, total):
        to_email = Email("%s" % userEmail)
        subject = "Su compra en Auto Air Group"
        content = Content("text/plain",
                          "Gracias por comprar en Auto Air Group. Su número de orden es: " + str(orderNum) + ".")
        mail = Mail(self.from_email, subject, to_email, content)
        response = self.sg.client.mail.send.post(request_body=mail.get())

        return response

    def sendChangePasswordLink(self, userEmail, link):
        print("level 1")
        to_email = Email("%s" % userEmail)
        print("level 2")
        subject = "Cambio de contrasena"
        content = Content("text/html", "Favor de ir al siguiente enlace para cambiar de contrasena %s " '<html>' % link +'</html>')
        print("level 3")
        mail = Mail(self.from_email, subject, to_email, content)
        response = self.sg.client.mail.send.post(request_body=mail.get())
        print("password")
        return response
