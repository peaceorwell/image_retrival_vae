from myapp_fac.admin import admin

@admin.route('/')
def index():
    return '<h1>Hello Admin from app factory!</h1>'
