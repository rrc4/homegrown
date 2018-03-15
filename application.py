from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField, PasswordField, BooleanField, ValidationError, IntegerField
from wtforms.validators import Email, Length, DataRequired, NumberRange, InputRequired, EqualTo, Regexp

app = Flask(__name__)


import db
app.config['SECRET_KEY'] = 'Super Secret Unguessable Key'




@app.before_request
def before_request():
    db.open_db_connection()


@app.teardown_request
def teardown_request(exception):
    db.close_db_connection()




@app.route('/')
def feed():
    return render_template("feed.html")


class PostForm(FlaskForm):
    price = FloatField('Price', validators=[NumberRange(min=1, max=100, message='Price has to be between 1 and 100 dollars')])
    quantity = IntegerField('Quantity', validators=[NumberRange(min=1, max=1000, message='The Quantity has to be between 1 and 1000')])
    product = StringField('Product', validators=[Length(min=1, max=40, message='Product has to be min of 1 and max of 40')])
    loc = StringField('Location', validators=[Length(min=1, max=40, message='Location has to be between 1 and 40')])

    submit = SubmitField('Save Post')


# Create a member
@app.route('/post/create', methods=['GET', 'POST'])
def create_post():
    post_form = PostForm()

    if post_form.validate_on_submit():
            rowcount = db.create_post(post_form.price.data,
                                      post_form.quantity.data,
                                      post_form.product.data,
                                      post_form.loc.data)

            if rowcount == 1:
                flash("Trip added successfully")
                return redirect(url_for('feed'))
            else:
                flash("New trip not created")

    for error in post_form.errors:
        for field_error in post_form.errors[error]:
            flash(field_error)
    return render_template('post_form.html', form=post_form, mode='create')


if __name__ == '__main__':
    app.run()
