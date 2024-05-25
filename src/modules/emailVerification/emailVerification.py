from pyircsdk import Module
from sqlalchemy.orm import Session
from .verifyhooks import VerifyHooks
from .otp import GenerateOTP, RegenerateOTP, VerifyOTP
from .models.email import Code, Email
from .sql import Engine


class EmailVerificationModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "verification")

    def handleCommand(self, message, command):
        if message.command == 'PRIVMSG':
            if command.command == self.fantasy + self.command:
                if command.args[0] == "request":
                    self.handleRequest(message, command)
                elif command.args[0] == "verify":
                    self.handleVerify(message, command)
                elif command.args[0] == "resend":
                    self.handleResend(message, command)

    def handleResend(self, message, command):
        if RegenerateOTP(message.messageFrom):
            self.irc.privmsg(message.messageTo, "Email sent")
        else:
            self.irc.privmsg(message.messageTo, "Oops something went wrong")


    def handleVerify(self, message, command):
        print("handleVerify")
        args = command.args[1:]
        print(command.args)
        print(args)
        print(message.messageFrom)
        service = args[0]
        passedCode = args[1]
        with Session(Engine) as session:
            email = session.query(Email).filter(Email.nick == message.messageFrom).one()
        if email is None:
            self.irc.privmsg(message.messageTo, "No email found")
        if VerifyOTP(message.messageFrom, passedCode):
            self.irc.privmsg(message.messageTo, "Email verified")
            VerifyHooks[service](self.irc, email.name)
        else:
            self.irc.privmsg(message.messageTo, "Invalid code")
        
                
    def handleRequest(self, message, command):
        print("handleRequest")
        
        args = command.args[1:]
        print(command.args)
        print(args)
        print(message.messageFrom)
        service = args[0]
        email = args[3]
        username = args[1]
        nick = args[2]
        with Session(Engine) as session:
            # check if email exists
            foundEmail = session.query(Email).filter(Email.email == email).first()
            if foundEmail is not None:
                self.irc.privmsg(message.messageTo, "Email already exists")
                return
            newEmail = Email(
                email=email,
                name=username,
                nick=nick,
                last_sent=0
            )
            session.add(newEmail)
            session.commit()
        if GenerateOTP(nick, service):
            print("Generated OTP")
            self.irc.privmsg(nick, "An email has been sent to you. Please reply with !verficiation verify %s <code>" % service)
        else:
            print("Invalid OTP")
            self.irc.privmsg(nick, "Oops something went wrong, contact admins to fix it")
        



