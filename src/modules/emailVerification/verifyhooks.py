
def verifyBNCHook(irc, nick):
    irc.privmsg("ThunderIRC", "!bnc approve %s" % nick)


# make dict of verify hooks
VerifyHooks = {
    "bnc": verifyBNCHook
}