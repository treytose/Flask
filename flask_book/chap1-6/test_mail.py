from app import mail, app
from flask_mail import Message

msg = Message('Subject', sender='treytose@gmail.com', recipients=['treyholthe@gmail.com'])
msg.body = 'Test 1 2 3'
msg.html = '<b> HTML </b> body'

with app.app_context():
	mail.send(msg)
