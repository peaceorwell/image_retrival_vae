from flask import Flask
from myapp.admin import admin
from flaskext.mysql import MySQL
from flask_bootstrap import Bootstrap
import config
from extract import extractor

app = Flask(__name__)
app.config.from_object('config')
Bootstrap(app)
app.register_blueprint(admin)
mysql = MySQL()
mysql.init_app(app)
caffe_net_500_vae = extractor('100')



from . import views
