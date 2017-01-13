from myapp_fac.main import main
from flask import render_template

@main.route('/')
def search_image():
    return render_template('templates/upload.html')
