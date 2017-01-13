from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
 
class AttachForm(Form):
    attach = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])