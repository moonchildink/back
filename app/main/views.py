from . import main
from flask import jsonify, request, render_template, url_for


@main.route('/')
def index():
    return render_template('index.html')
