import time
import pyotp
from sqlalchemy.orm import Session
from .email import SendEmail
from .sql import Engine
from .models.email import Code, Email


def GenerateOTP(nick, service):
    # get email object by nick
    with Session(Engine) as session:
        email = session.query(Email).filter(Email.nick == nick).first()
    if email is None:
        print('No email found')
        return None
    
    # generate random string for secret key
    secret = pyotp.random_base32()
    with Session(Engine) as session:
        # create new row in table
        newCode = Code(
            email_id=email.id,
            secret=secret,
        )
        session.add(newCode)
        session.commit()
    totp = pyotp.TOTP(secret, interval=600)

    code = totp.now()
    # send code to email
    print(code)
    SendEmail(email.email, service, code)

    # set last_sent to current time
    with Session(Engine) as session:
        email.last_sent = int(time.time())
        session.commit()
    
    return True
        

def VerifyOTP(nick, passedCode):
    with Session(Engine) as session:
        email = session.query(Email).filter(Email.nick == nick).first()
        if email is None:
            return
        code = session.query(Code).filter(Code.email_id == email.id).first()
        if code is None:
            return
        print(code.secret)
        # convert secret to string
        code.secret = str(code.secret)
        totp = pyotp.TOTP(code.secret, interval=600)
        if totp.verify(passedCode):
           # remove code from table
           session.delete(code)
           session.commit()
           # remove user from table
           session.delete(email)
           session.commit()
           return True
        else:
            return False
        
def RegenerateOTP(nick):
    with Session(Engine) as session:
        foundEmail = session.query(Email).filter(Email.name == nick).first()
        if foundEmail is None:
            return
        foundCode = session.query(Code).filter(Code.email_id == foundEmail.id).first()
        if foundCode is None:
            return
        # generate new code
        secret = pyotp.random_base32()
        foundCode.secret = secret
        session.commit()
        totp = pyotp.TOTP(secret, interval=600)
        code = totp.now()
        print(code)
        SendEmail(foundEmail.email, code)
        # send code to email
        # set last_sent to current time
        foundEmail.last_sent = int(time.time())
        session.commit()
        return True