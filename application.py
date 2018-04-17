import os
from pathlib import PurePath

from flask import Flask, session, request, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, FloatField, IntegerField, PasswordField, SelectField, TextAreaField
from wtforms.validators import Length, NumberRange, Email, InputRequired, EqualTo, DataRequired, Regexp
from flask_wtf.file import FileField, FileRequired

from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Team Bryson Key'


import db

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


# Opens the database connection
@app.before_request
def before_request():
    db.open_db_connection()


# Closes the database connection
@app.teardown_request
def teardown_request(exception):
    db.close_db_connection()


# A form to sign in to an existing account
class SignInForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=8),
                                                     Regexp(r'.*[A-Za-z]', message="Password must have at least one letter"),
                                                     Regexp(r'.*[0-9]', message="Password must have at least one digit"),
                                                     Regexp(r'.*[!@#$%^&*_+=]', message="Password must have at least one special character")])
    submit = SubmitField('Sign In')


# A form to sign up for a new account
class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=1, max=80)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('New Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match'),
                                                         Length(min=8),
                                                         Regexp(r'.*[A-Za-z]', message="Password must have at least one letter"),
                                                         Regexp(r'.*[0-9]', message="Password must have at least one digit"),
                                                         Regexp(r'.*[!@#$%^&*_+=]', message="Password must have at least one special character")])
    confirm = PasswordField('Confirm Password', validators=[InputRequired()])
    submit = SubmitField('Sign Up')


@app.route('/')
def index():
    return render_template('index.html')


# Allows users to sign in
@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    sign_in_form = SignInForm()

    if sign_in_form.validate_on_submit() and sign_in_form.validate():
        user = db.find_user_by_email(sign_in_form.email.data)

        if user:
            is_active = True
        else:
            is_active = False

        if authenticate(sign_in_form.email.data, sign_in_form.password.data) and is_active:
            current = User(sign_in_form.email.data)
            login_user(current)
            session['username'] = current.email
            session['id'] = current.id

            flash('Sign in successful!', category='success')
            return redirect(url_for('all_posts'))
        else:
            flash('Invalid email address or password', category='danger')
            return redirect(url_for('sign_in'))

    return render_template('sign-in.html', sign_in_form=sign_in_form)


# Allows users to sign up
@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    sign_up_form = SignUpForm()

    user = db.find_user_by_email(sign_up_form.email.data)

    if user is not None:
        flash("User {} already exists".format(sign_up_form.email.data), category='danger')
        return redirect(url_for('sign_up'))
    else:
        if sign_up_form.validate_on_submit() and sign_up_form.validate():
            user = db.create_user(sign_up_form.name.data, sign_up_form.email.data, sign_up_form.password.data, 5.0, True)

            if user:
                is_active = True
            else:
                is_active = False

            if authenticate(sign_up_form.email.data, sign_up_form.password.data) and is_active:
                current = User(sign_up_form.email.data)
                login_user(current)
                session['username'] = current.email

                flash('Sign up successful!', category='success')
                return redirect(url_for('all_posts'))
            else:
                flash('Invalid email address or password', category="danger")
                return redirect(url_for('sign_up'))

    return render_template('sign-up.html', sign_up_form=sign_up_form)


# Make sure the user email and password match with what they should be
def authenticate(email, password):
    valid_users = db.all_users()

    for user in valid_users:
        if email == user['email'] and user['password'] == password:
            return email
    return None


# Necessary for the login manager to work
@login_manager.user_loader
def load_user(id):
    return User(id)


# A User class for creating User objects
class User(object):
    def __init__(self, email):
        self.email = email
        user = db.find_user_by_email(self.email)
        if user is not None:
            # self.name = db.find_member_info(self.email)['first_name']
            self.id = user['id']
        else:
            self.name = 'no name'

        self.is_active = True
        self.is_authenticated = True

    def get_id(self):
        return self.email

    def __repr__(self):
        return "<User '{}' {} {}".format(self.email, self.is_authenticated, self.is_active)


# Signs the user out
@app.route('/signout')
def sign_out():
    session.pop('user', None)
    return redirect(url_for('index'))


# The form to create or update a user
class UserForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=1, max=80)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('New Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match'),
                                                         Length(min=8),
                                                         Regexp(r'.*[A-Za-z]', message="Password must have at least one letter"),
                                                         Regexp(r'.*[0-9]', message="Password must have at least one digit"),
                                                         Regexp(r'.*[!@#$%^&*_+=]', message="Password must have at least one special character")])
    confirm = PasswordField('Repeat Password', validators=[InputRequired()])
    submit = SubmitField('Save User')


# Allows an administrator to create a user
@app.route('/users/new', methods=['GET', 'POST'])
def create_user():
    user_form = UserForm()

    if user_form.validate_on_submit():
        user = db.find_user_by_email(user_form.email.data)

        if user is not None:
            flash("User {} already exists".format(user_form.email.data), category='danger')
        else:
            rowcount = db.create_user(user_form.name.data,
                                      user_form.email.data,
                                      user_form.password.data,
                                      5.0,
                                      True)

            if rowcount == 1:
                flash("User {} created".format(user_form.name.data), category='success')
                return redirect(url_for('all_users'))
            else:
                flash("New user not created", category='danger')

    return render_template('user-form.html', form=user_form, mode='create')


# Edit a post by a user's ID (primary key)
@app.route('/users/edit/<id>', methods=['GET', 'POST'])
def edit_user(id):
    row = db.find_user_by_id(id)

    if row is None:
        flash("User doesn't exist", category='danger')
        return redirect(url_for('all_users'))

    user_form = UserForm(name=row['name'],
                         email=row['email'],
                         password=row['password'])

    if user_form.validate_on_submit():
        rowcount = db.update_user(user_form.name.data,
                                  user_form.email.data,
                                  user_form.password.data,
                                  id)

        if rowcount == 1:
            flash("User '{}' updated".format(user_form.name.data), category='success')
            return redirect(url_for('all_users'))
        else:
            flash('User not updated', category='danger')

    return render_template('user-form.html', form=user_form, mode='update')


# Disable a user by their ID (primary key)
@app.route('/users/disable/<id>')
def disable_user_by_id(id):
    user = db.find_user_by_id(id)
    db.disable_user_by_id(id)
    flash("User {} disabled".format(user['name']), category='success')
    return redirect(url_for('all_users'))


# Enable a user by their ID (primary key)
@app.route('/users/enable/<id>')
def enable_user_by_id(id):
    user = db.find_user_by_id(id)
    db.enable_user_by_id(id)
    flash("User {} enabled".format(user['name']), category='success')
    return redirect(url_for('all_users'))


# Gets a list of all the users in the database
@app.route('/users')
def all_users():
    return render_template('all-users.html', users=db.all_users())


# Testing page
@app.route('/test', methods=['GET', 'POST'])
def test():
    query = ProductSearchForm(request.form)

    if request.method == 'POST':
        query_list = query.search.data.lower().split(" ")
        posts = db.search_products(query_list)
        return render_template('posts.html', form=query, posts=posts, mode='results')

    return render_template('test.html', search_form=query)


# A user's profile
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    query = ProductSearchForm(request.form)

    if request.method == 'POST':
        query_list = query.search.data.lower().split(" ")
        posts = db.search_products(query_list)
        return render_template('posts.html', search_form=query, posts=posts, mode='results')

    return render_template('profile.html', search_form=query)


# A list of the current user's posts
@app.route('/my-posts', methods=['GET', 'POST'])
def my_posts():
    user_id = session['id']
    query = ProductSearchForm(request.form)

    if user_id is None:
        flash('User is not logged in!', category='danger')
        posts = []
    else:
        posts = db.posts_by_user(user_id)

    if request.method == 'POST':
        query_list = query.search.data.lower().split(" ")
        posts = db.search_products(query_list)
        return render_template('posts.html', search_form=query, posts=posts, mode='results')

    return render_template('posts.html', search_form=query, posts=posts, mode='my-posts')


# A list of the a user's posts
@app.route('/posts/user/<user_id>', methods=['GET', 'POST'])
def user_posts(user_id):
    query = ProductSearchForm(request.form)
    user = db.find_user_by_id(user_id)

    if user_id is None:
        flash('No user with id {}'.format(user_id), category='danger')
        posts = []
    else:
        posts = db.posts_by_user(user_id)

    if request.method == 'POST':
        query_list = query.search.data.lower().split(" ")
        posts = db.search_products(query_list)
        return render_template('posts.html', search_form=query, posts=posts, mode='results')

    return render_template('posts.html', search_form=query, user=user, posts=posts, mode='user')


# A list of the user's favorites
@app.route('/favorites', methods=['GET', 'POST'])
def my_favorites():
    query = ProductSearchForm(request.form)

    if session:
        user_id = session['id']
        favorites = db.favorites_by_user(user_id)

        if request.method == 'POST':
            query_list = query.search.data.lower().split(" ")
            posts = db.search_products(query_list)
            return render_template('posts.html', search_form=query, posts=posts, mode='results')

        return render_template('posts.html', user_id=user_id, search_form=query, posts=favorites, mode='favorites')


# Adds a post to favorites
# TODO: Check for duplicates
@app.route('/favorites/add/<post_id>')
def add_to_favorites(post_id):
    if session:
        user_id = session['id']
        post = db.find_post_by_id(post_id)

        db.add_to_favorites(user_id, post_id)
        flash("{} added to favorites".format(post['product']), category='success')

    return redirect(url_for('all_posts'))


@app.route('/favorites/remove/<post_id>')
def remove_from_favorites(post_id):
    if session:
        user_id = session['id']
        favorites = db.favorites_by_user(user_id)
        post = db.find_post_by_id(post_id)

        if favorites:
            db.delete_from_favorites(user_id, post_id)
            flash("{} removed from favorites".format(post['product']), category='success')
        else:
            flash("Unable to remove from favorites", category='danger')
    return redirect(url_for('my_favorites'))
  

# The form to create or edit a post
class PostForm(FlaskForm):
    product = StringField('Product (ex. Strawberries)', validators=[InputRequired(), Length(min=1, max=100, message='Product must be between 1 and 100 characters')])
    description = TextAreaField('Description (<150 characters)', validators=[InputRequired(), Length(min=1, max=150, message='Description must be between 1 and 150 characters')])
    price = FloatField('Price (ex. 5.99)', validators=[InputRequired(), NumberRange(min=0.01, message='Price must be at least $0.01')])
    quantity = IntegerField('Quantity', validators=[InputRequired(), NumberRange(min=1, max=1000000, message='Quantity must be between 1 and 1,000,000')])
    unit = SelectField('Unit', choices=[('item', 'item'),
                                        ('oz', 'oz'),
                                        ('lb', 'lb'),
                                        ('gal', 'gal'),
                                        ('kg', 'kg')])
    category = SelectField('Category', choices=[('Vegetables', 'Vegetables'),
                                                ('Fruits', 'Fruits'),
                                                ('Meat', 'Meat'),
                                                ('Dairy', 'Dairy'),
                                                ('Grains', 'Grains'),
                                                ('Other', 'Other')])
    zip = IntegerField('ZIP Code (ex. 46969)', validators=[InputRequired(), NumberRange(min=3000, max=99999, message='ZIP code not valid - must be 5 characters')])
    image = FileField('Image', validators=[FileRequired(message="Image required")])

    submit = SubmitField('Save Post')


# Create a post
@app.route('/posts/new', methods=['GET', 'POST'])
def create_post():
    post_form = PostForm()
    
    if session:
        user_id = session['id']

        if post_form.validate_on_submit():
                post_dict = db.create_post(user_id,
                                           post_form.price.data,
                                           post_form.quantity.data,
                                           post_form.unit.data,
                                           post_form.product.data,
                                           post_form.category.data,
                                           post_form.zip.data,
                                           post_form.description.data)
                uploaded_photo = post_form.image.data

                photo_row = db.init_photo(post_dict['id'])

                file_name = "file{:04d}".format(photo_row['id'])

                extension = PurePath(uploaded_photo.filename).suffix
                file_name += extension

                file_path = os.path.join('static/photos', file_name)

                file_path2 = os.path.join('photos', file_name)

                save_path = os.path.join(app.static_folder, file_path2)
                uploaded_photo.save(save_path)

                db.set_photo(photo_row['id'], file_path)

                if post_dict['rowcount'] == 1:
                    flash("{} added successfully".format(post_form.product.data), category='success')
                    return redirect(url_for('all_posts'))
                else:
                    flash("Post not created", category='danger')

        for error in post_form.errors:
            for field_error in post_form.errors[error]:
                flash(field_error, category='danger')
        return render_template('post-form.html', post_form=post_form, mode='create')


# Edit a post
@app.route('/posts/edit/<id>', methods=['GET', 'POST'])
def edit_post(id):
    row = db.find_post_by_id(id)

    if row is None:
        flash("Post doesn't exist", category='danger')
        return redirect(url_for('index'))

    post_form = PostForm(price=row['price'],
                         quantity=row['quantity'],
                         unit=row['unit'],
                         product=row['product'],
                         zip=row['zip'],
                         description=row['description'])

    if post_form.validate_on_submit():
        rowcount = db.update_post(post_form.price.data,
                                  post_form.quantity.data,
                                  post_form.unit.data,
                                  post_form.product.data,
                                  post_form.zip.data,
                                  post_form.description.data,
                                  id)

        if rowcount == 1:
            flash("'{}' post updated".format(post_form.product.data), category='success')
            return redirect(url_for('all_posts'))
        else:
            flash('Post not updated', category='danger')

    return render_template('post-form.html', post_form=post_form, mode='update')


@app.route('/posts/<id>', methods=['GET', 'POST'])
def post_details(id):
    post = db.find_post_by_id(id)
    query = ProductSearchForm(request.form)

    if request.method == 'POST':
        query_list = query.search.data.lower().split(" ")
        posts = db.search_products(query_list)
        return render_template('posts.html', search_form=query, posts=posts, mode='results')

    return render_template('post-details.html', search_form=query, post=post)


# All the posts in the database - also handles searching
@app.route('/posts', methods=['GET', 'POST'])
def all_posts():
    query = ProductSearchForm(request.form)

    if request.method == 'POST':
        query_list = query.search.data.lower().split(" ")
        posts = db.search_products(query_list)

        if not posts:
            flash('No Results Found', category='danger')
            return render_template('posts.html', search_form=query, posts=[], mode='results')
        else:
            return render_template('posts.html', search_form=query, posts=posts, mode='results')
    return render_template('posts.html', search_form=query, posts=db.all_posts(), mode='feed')


class ProductSearchForm(FlaskForm):
    search = StringField('Search', [DataRequired()])
    submit = SubmitField('Search')


@app.route('/posts/delete/<id>')
def delete_post_by_id(id):
    post = db.find_post_by_id(id)
    if post is None:
        flash("Post doesn't exist", category='danger')
    else:
        db.delete_post_by_id(id)
        flash("Post deleted", category='success')
        return redirect(url_for('my_posts'))


if __name__ == '__main__':
    app.run()
