from flask import render_template
from . import main

@main.route('/', methods=['GET'])
def home():
    return render_template('home.html')