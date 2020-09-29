from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/Hello')
def Hello():
    return "<html><body><h1>Hello, World!</h1></body></html>"
