import smtplib

def sendEmail(subject, message, receiver):
    print("Sending Email to: " + str(receiver) + "...")
    # creates SMTP session
    host = 'smtp.gmail.com'
    port = 587
    s = smtplib.SMTP(host, port)
    user = "example@gmail.com" # You're gmail id here
    password = "4eyrttrgde5y" # You'r gmail app password here, not actual gmail password
    '''
    To get app password, go to https://support.google.com/accounts/answer/185833?hl=en and follow the instructions here.

    Go to your Google Account.
    Select Security.
    Under "Signing in to Google," select App Passwords. You may need to sign in. If you don’t have this option, it might be because:
        2-Step Verification is not set up for your account.
        2-Step Verification is only set up for security keys.
        Your account is through work, school, or other organization.
        You turned on Advanced Protection.
    At the bottom, choose Select app (Select `Mail` here) and choose the app you using and then Select device and choose the device you’re using and then Generate.
    Follow the instructions to enter the App Password. The App Password is the 16-character code in the yellow bar on your device.
    Tap Done.

    '''
    # start TLS for security
    s.ehlo()
    s.starttls()
    
    # Authentication (username, password)
    s.login(user, password)
    
    # message to be sent
    from_mail = "example@gmail.com" # Your gmail id here. Most of the time should be same as your username.
    message = 'From: {}\nSubject: {}\n\n{}'.format(from_mail, subject, message)
    # print(message)
    # sending the mail
    s.sendmail(from_mail, receiver, message)
    
    # terminating the session
    s.quit()

def sendEmailVerification(code, receiver):
    sendEmail("Verification Code", "Your verification code is: " + str(code) + "\n\nApp Team", str(receiver).strip())

# Test
if __name__ == "__main__":
    sendEmailVerification("test 7890", "receiver@gmail.com")