from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, PasswordField
from wtforms.validators import Length, NumberRange, Email, InputRequired, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Super Secret Unguessable Key'


import db


@app.before_request
def before_request():
    db.open_db_connection()


@app.teardown_request
def teardown_request(exception):
    db.close_db_connection()


@app.route('/')
def feed():
    return render_template("index.html")
  
  
class PostForm(FlaskForm):
    price = FloatField('Price', validators=[NumberRange(min=1, max=100, message='Price must be between $1 and $100')])
    quantity = IntegerField('Quantity', validators=[NumberRange(min=1, max=1000, message='Quantity must be between 1 and 1000')])
    product = StringField('Product', validators=[Length(min=1, max=40, message='Product must be min of 1 and max of 40 characters')])
    loc = StringField('Location', validators=[Length(min=1, max=40, message='Location has to be between 1 and 40')])

    submit = SubmitField('Save Post')


# Create a post
@app.route('/posts/create', methods=['GET', 'POST'])
def create_post():
    post_form = PostForm()

    if post_form.validate_on_submit():
            rowcount = db.create_post(post_form.price.data,
                                      post_form.quantity.data,
                                      post_form.product.data,
                                      post_form.loc.data)

            if rowcount == 1:
                flash("Post added successfully")
                return redirect(url_for('all_posts'))
            else:
                flash("New post not created")

    for error in post_form.errors:
        for field_error in post_form.errors[error]:
            flash(field_error)
    return render_template('post-form.html', form=post_form, mode='create')


# Create a form member
class MemberForm(FlaskForm):
    first_name = StringField('First Name', validators=[Length(min=1, max=40)])
    last_name = StringField('Last Name', validators=[Length(min=1, max=40)])
    email = StringField('Email', validators=[Email()])
    phone = StringField('Phone', validators=[Length(min=10, max=10)])
    password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Save Member')


@app.route('/members/create', methods=['GET', 'POST'])
def create_member():
    member_form = MemberForm()

    if member_form.validate_on_submit():
        member = db.find_member(member_form.email.data)

        if member is not None:
            flash("Member {} already exists".format(member_form.email.data));
        else:
            rowcount = db.create_member(member_form.first_name.data,
                                        member_form.last_name.data,
                                        member_form.email.data,
                                        member_form.phone.data,
                                        member_form.password.data,
                                        5.0,
                                        True)

            if rowcount == 1:
                flash("Member {} created".format(member_form.email.data))
                return redirect(url_for('all_members'))
            else:
                flash("New member not created")

    return render_template('member-form.html', form=member_form, mode='create')


# Gets a list of all the members in the database
@app.route('/members')
def all_members():
    return render_template('all-members.html', members=db.all_members())


@app.route('/posts')
def all_posts():
    return render_template('all-posts.html', posts=db.all_posts())


if __name__ == '__main__':
    app.run()
