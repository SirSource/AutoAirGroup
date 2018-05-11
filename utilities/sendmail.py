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


class Sendmail:

    def __init__(self):
        self.sg = sendgrid.SendGridAPIClient(
            apikey='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')
        self.from_email = Email("info@autoair.io")

    def sendAccountCreationEmail(self, userEmail):
        to_email = Email(userEmail)
        subject = "!Bienvenido a Auto Air Group!"
        content = Content("text/plain", "<h1>Your order number is...</h1>")
        mail = Mail(self.from_email, subject, to_email, content)
        response = self.sg.client.mail.send.post(request_body=mail.get())
        return response

    def sendAccountRecoverEmail(self, userEmail):
        to_email = Email(userEmail)
        subject = "Auto Air Group Order Details"
        content = Content("text/plain", "Your order number is...")
        mail = Mail(self.from_email, subject, to_email, content)
        response = self.sg.client.mail.send.post(request_body=mail.get())
        return response

    def sendAccountCreationEmail(self, userEmail):
        to_email = Email(userEmail)
        subject = "Auto Air Group Order Details"
        content = Content("text/plain", "Your order number is...")
        mail = Mail(self.from_email, subject, to_email, content)
        response = self.sg.client.mail.send.post(request_body=mail.get())
        return response

    def sendOrderConfirmationEmail(self, userEmail):
        to_email = Email(userEmail)
        subject = "Auto Air Group Order Details"
        content = Content("text/plain", "Your order number is...")
        mail = Mail(self.from_email, subject, to_email, content)
        response = self.sg.client.mail.send.post(request_body=mail.get())
        return response
