from flask import g
from app import create_app, socket
app = create_app()

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db:
		db.commit()
		db.close()

if __name__ == '__main__':
	#app.run(host='0.0.0.0', port=5001)
	socket.run(app, host='0.0.0.0', port=5001)