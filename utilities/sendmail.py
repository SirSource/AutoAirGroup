import sendgrid
from sendgrid.helpers.mail import *


class SendMail:

    def __init__(self):
        self.sg = sendgrid.SendGridAPIClient(
            apikey='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')
        self.from_email = Email("info@autoair.io")

    def sendAccountCreationEmail(self, userEmail):
        """
        Sends email after account creation.
        :param userEmail: Email for the user.
        :return: Status code.
        """
        to_email = Email(userEmail)
        subject = "!Bienvenido a Auto Air Group!"
        content = Content("text/html",
                          "<html><h1>!Gracias por crear una cuenta con Auto Air Group!</h1> <h3>Desde su cuenta puede ver el historial de compras y tener un récord para sus recibos.</h3></html>")
        mail = Mail(self.from_email, subject, to_email, content)
        response = self.sg.client.mail.send.post(request_body=mail.get())
        return response

    def sendAccountRecoverEmail(self, userEmail, code):
        """
        Email to recover account.
        :param userEmail: User emial.
        :param code: The code that was generated for the link reset.
        :return: Status code.
        """
        to_email = Email(userEmail)
        subject = "Recuperar Acceso a su Cuenta"
        content = Content("text/html",
                          '<html>Para recuperar acceso a su cuenta copie y pegue la siguiente dirección en su navegador <a href="https://autoair.io/user/reset/password/' + str(
                              code) + '">Recuperar Contraseña</a></html>')
        mail = Mail(self.from_email, subject, to_email, content)
        response = self.sg.client.mail.send.post(request_body=mail.get())
        print("recovery pass")
        return response

    def sendOrderConfirmationEmail(self, userEmail, orderNum):
        """
        Email for oder completion.
        :param userEmail: User email.
        :param orderNum: Order Number.
        :return: Status Code.
        """
        to_email = Email("%s" % userEmail)
        subject = "Su compra con Auto Air Group"
        content = Content("text/plain",
                          '<html><h5>Gracias por comprar en Auto Air Group.</h5> <p>Puede ver un recibo de su orden (' + str(
                              orderNum) + ') <a href="127.0.0.1:5000/order/receipt/confirmation/' + str(
                              orderNum) + '">aquí</a>.</p></html>')
        mail = Mail(self.from_email, subject, to_email, content)
        response = self.sg.client.mail.send.post(request_body=mail.get())

        return response

    def sendChangePasswordLink(self, userEmail, link):
        """
        Email for password link reset alternate.
        :param userEmail: User email.
        :param link: Entire link with embedded key.
        :return: Status code.
        """
        print("level 1")
        to_email = Email("%s" % userEmail)
        print("level 2")
        subject = "Cambio de contrasena"
        content = Content("text/html",
                          "Favor de ir al siguiente enlace para cambiar de contrasena %s " '<html>' % link + '</html>')
        print("level 3")
        mail = Mail(self.from_email, subject, to_email, content)
        response = self.sg.client.mail.send.post(request_body=mail.get())
        print("password")
        return response
