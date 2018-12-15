from app import create_app, socket
from flask import g

app = create_app()

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db:
		db.commit()
		db.close()

if __name__ == '__main__':
	socket.run(app, host='0.0.0.0', port=80, debug=True)
