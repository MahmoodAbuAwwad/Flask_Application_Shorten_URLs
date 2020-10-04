from flask import Flask, request, render_template

app = Flask(__name__,template_folder="templates")
app.config['SECRET_KEY']= 'Hello Python!'

from app import routes 