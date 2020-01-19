from app import mail
from flask_mail import Message
from flask import current_app, render_template

app = current_app

def send_email(to, subject, template, **kwargs):
        msg = Message(subject, sender=app.config['FLASKY_MAIL_SENDER'],
                      recipients=[to])

        msg.body = render_template(template + '.txt', **kwargs) #kwargs are used for jinja2 arguments
        msg.html = render_template(template + '.html', **kwargs)
        mail.send(msg)
