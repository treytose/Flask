import smtplib

def send_email(subject, message):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo() #saying hello to the server, must call to prevent future errors
    smtpObj.starttls() #starts TLS encryption for our connection

    smtpObj.login('redhatter011@gmail.com', '$011Oh0858558011$')

    m = 'Subject: {}\n\n{}'.format(subject, message)

    resp = smtpObj.sendmail('redhatter011@gmail.com', 'treyholthe@gmail.com', m)
    smtpObj.quit()

    if not resp:
        return 'Email Successfully sent'
    return 'Error sending email'
