# VerifyBot

Purpose of this bot is to do OTP verification. May later expand to MFA for certain actions.
Main goal was to automate the process of verifying emails through a OTP code sent though email.

## How it Works
user will request to have their email verified by providing the below information:

```bash
# start verification process
/msg verifybot !verification request <service> <username> <nick> <email>
# user should get an email with otp code that lasts 5 min
/msg verifybot !verification verify <service> <code>
# depending on the service, there may be hooks defined which willl trigger other actions.
# In the case of thunderIRC we send a message to the bot to verify an account.
```
