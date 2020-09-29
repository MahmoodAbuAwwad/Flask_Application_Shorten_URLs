from flask import Flask, request, render_template

app = Flask(__name__,template_folder="templates")

from app import routes