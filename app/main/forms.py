from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')
    
class ViewsForm(FlaskForm):
    views_title = StringField('Views Title')
    description = TextAreaField('Views')
    submit = SubmitField('Submit')
    
class CommentForm(FlaskForm):
    comment = TextAreaField('Comment')
    submit = SubmitField('Post a comment')
    
    
