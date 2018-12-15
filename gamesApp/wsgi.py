from app import app

application = app

if __name__ == '__main__':
	application.run()


#UWSGI command: uwsgi --socket 0.0.0.0:80 --protocol=http -w wsgi:app
#6LerdTwUAAAAAOVc_RKwqdsK9I-gKxZ8_xdhnT4j
