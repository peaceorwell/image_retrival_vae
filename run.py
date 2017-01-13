from myapp import app
#from myapp_fac import create_app
import config

#app = create_app('config')

app.run(host='10.2.2.121',port=4001,threaded=True,debug=True)
#app1.run(host='0.0.0.0', debug=True)
