import sys, os


from pyircsdk import IRCSDKConfig, IRCSDK

from modules.emailVerification.emailVerification import EmailVerificationModule

host = os.getenv('HOST', 'irc.thunderirc.net')
port = os.getenv('PORT', '6697')
# convert port string to int
port = int(port)
ssl = os.getenv('SSL', 'True')
nick = os.getenv('NICK', 'verifybot')
channel = os.getenv('CHANNEL', '#thunderirc')
user = os.getenv('USER', 'verifybot')
realname = os.getenv('REALNAME', 'verifybot')
nickservFormat = os.getenv('NICKSERV_FORMAT', 'nickserv :identify %s')
nickservPassword = os.getenv('NICKSERV_PASSWORD', None)
passw = os.getenv('PASS', None)
nodataTimeout = os.getenv('NODATA_TIMEOUT', 0)


irc = IRCSDK(IRCSDKConfig(
    host=host,
    port=port,
    nick=nick,
    # string false to boolean
    ssl=ssl == 'True',
    channel=channel,
    user=user,
    realname=realname,
    nickservFormat=nickservFormat,
    nickservPassword=nickservPassword,
    password=passw,
    nodataTimeout=int(nodataTimeout)
))

emailVerificationModule = EmailVerificationModule(irc)
emailVerificationModule.startListening()


irc.connect(None)