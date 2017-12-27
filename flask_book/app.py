from flask import Flask, request, current_app

app = Flask(__name__)


@app.before_first_request
def first_request():
    print("before_first_request called!")

@app.before_request
def before():
    print("before_request called!")

@app.after_request
def after_request(response):
    print("after_request response: ")
    print("After request called!")
    return response

@app.route('/')
def index():
    return '<h1> Hello World! </h1>'

if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0', debug=True)
