from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField, PasswordField, BooleanField, ValidationError, IntegerField
from wtforms.validators import Email, Length, DataRequired, NumberRange, InputRequired, EqualTo, Regexp

app = Flask(__name__)

import db



@app.route('/')
def feed():
    return render_template("feed.html")




class postForm(FlaskForm):
    #Variables for a post are:  price, picture, time, info, quantitiy, name, pickup location
    price = FloatField('Price (i.e. 6.25', validators=[NumberRange(min=1, max=100, message='Price has to be between 1 and 100 dollars')])
    quantity = IntegerField('Quantity', validators=[NumberRange(min=1, max=50, message='The Quantity has to be between 1 and 50')])
    name = StringField('Name', validators=[Length(min=1, max=40, message='Name has to be min of 1 and max of 40')])



    year = StringField('Year', validators=[Regexp(r'^\d{4}$', message='Year has to be 4 digits'), Length(min=1, max=40, message="Year has to be min of 1 and max of 40")])
    semester = SelectField('Semester', choices=[('fall', 'Fall'), ('interterm', 'Interterm'), ('spring', 'Spring'), ('spring break', 'Spring Break')])
    #email = StringField('Email', validators=[Email()])
    #first_name = StringField('First Name', validators=[Length(min=1, max=40)])
    #last_name = StringField('Last Name', validators=[Length(min=1, max=40)])
    #password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    #confirm = PasswordField('Repeat Password')
    submit = SubmitField('Save Trip')


# Create a member
@app.route('/post/create', methods=['GET', 'POST'])
def create_trip():
    post_form = postForm()

    if post_form.validate_on_submit():
            rowcount = db.create_member(post_form.destination.data,
                                        post_form.year.data,
                                        post_form.semester.data)

            if rowcount == 1:
                flash("Trip added successfully")
                return redirect(url_for('trip_report'))
            else:
                flash("New trip not created")

    for error in post_form.errors:
        for field_error in post_form.errors[error]:
            flash(field_error)
    return render_template('trip_form.html', form=post_form, mode='create')






















if __name__ == '__main__':
    app.run()
