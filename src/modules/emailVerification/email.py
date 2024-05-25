import smtplib, ssl, os
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from mjml import mjml_to_html
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv(".env")

smtp_server = os.getenv("SMTP_SERVER")
port = os.getenv("SMTP_PORT")
sender_email = os.getenv("SMTP_EMAIL")
password = os.getenv("SMTP_PASSWORD")

print("PATH")
print(os.path.join(os.path.dirname(__file__), "templates" ))
templateLoader = FileSystemLoader( os.path.join(os.path.dirname(__file__), "templates" ))

env = Environment(
    loader=templateLoader,
    autoescape=select_autoescape()
)

def generateEmail(service, code):

    template = env.get_template("verify.mjml")

    updatedTempalte = template.render(service=service, code=code)
    
    return mjml_to_html(updatedTempalte)



def SendEmail(receiver_email, service, code):
    smtp_server = os.getenv("SMTP_SERVER")
    port = os.getenv("SMTP_PORT")
    sender_email = os.getenv("SMTP_EMAIL")
    password = os.getenv("SMTP_PASSWORD")

    message = MIMEMultipart("alternative")
    message["Subject"] = "ThunderIRC OTP Code"
    message["From"] = sender_email
    message["To"] = receiver_email
    text = """\
Hi,
Your code is %s""" % code
    html = generateEmail(service, code)
    
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html.html, "html")
    message.attach(part1)
    message.attach(part2)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.ehlo(smtp_server) # Can be omitted
        server.login(sender_email, password)
    
        server.sendmail(sender_email, receiver_email, message.as_string())
    
    print("Email sent")