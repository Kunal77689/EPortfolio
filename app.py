from flask import Flask, render_template, redirect, url_for, flash, get_flashed_messages
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import Length, Email, DataRequired, ValidationError
app = Flask(__name__)
app.config['SECRET_KEY'] = '61547750776fb973d858c0a1'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db = SQLAlchemy(app)

class contact_database(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    user_name = db.Column(db.String(length = 32), nullable = False)
    user_email = db.Column(db.String(length = 64), nullable = False)
    user_message = db.Column(db.String(length = 1000), nullable = False)



class send_query(FlaskForm):
    name = StringField(label = 'Name: ', validators = [Length(max = 30), DataRequired()])
    email = StringField(label = 'Email Address: ', validators = [Email(), DataRequired()])
    Message = StringField(label = 'Message: ', validators = [Length(max = 1000), DataRequired()])
    submit = SubmitField(label = 'Submit')



@app.route('/')
def home_page():
    return render_template('home.html')
@app.route('/about')
def about_page():
    return render_template('about.html')
@app.route('/projects')
def blog_page():
    return render_template('blog.html')
@app.route('/contact', methods = ['GET', 'POST'])
def contact_page():
    form = send_query()
    if form.validate_on_submit():
        new_entry = contact_database(user_name = form.name.data,
                                     user_email = form.email.data,
                                     user_message = form.Message.data)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('home_page'))
    if form.errors != {}:
        for msg in form.errors.values():
            flash(msg)
    return render_template('contact.html', form=form)

if __name__ == "main":
    app.run()
