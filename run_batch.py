from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from myapp import app as frontend
from myapp_fac import create_app
import config

backend = create_app('config')

applications = DispatcherMiddleware(frontend, {'/backend': backend})

run_simple('0.0.0.0', 5000, applications, use_reloader=True, use_debugger=True)