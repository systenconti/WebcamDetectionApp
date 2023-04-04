import smtplib
import ssl
from credentials import username, password
from email.message import EmailMessage


def send_email(image):
    host = "smtp.gmail.com"
    port = 465

    context = ssl.create_default_context()

    msg = EmailMessage()
    msg['Subject'] = 'Ktoś wszedł Ci na chatę!'
    # me == the sender's email address
    # family = the list of all recipients' email addresses
    msg['From'] = username
    msg['To'] = "sowasupergosc@gmail.com"
    msg.set_content('Poniżej zdjęcie sprawcy!')

    with open(image, "rb") as img:
        img_data = img.read()
    msg.add_attachment(img_data, maintype='image',
                       subtype='png', filename='intruder.png')

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.send_message(msg=msg)


if __name__ == "__main__":
    send_email("test.png")