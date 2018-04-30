import os
import datetime

from pathlib import PurePath
from functools import wraps

from flask import Flask, session, request, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, FloatField, IntegerField, PasswordField, SelectField, TextAreaField, BooleanField
from wtforms.validators import Length, NumberRange, Email, InputRequired, EqualTo, DataRequired, Regexp
from flask_wtf.file import FileField, FileRequired

from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Team Bryson Key'

import db

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
today = datetime.date.today()


# Opens the database connection
@app.before_request
def before_request():
    db.open_db_connection()


# Closes the database connection
@app.teardown_request
def teardown_request(exception):
    db.close_db_connection()


# Allow/disallow users from accessing pages based on their roles
def requires_roles(*roles):

    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not hasattr(current_user, 'role'):
                flash('You must be signed in to do this!', category="danger")
                return redirect(url_for('all_posts'))
            elif current_user.role not in roles:
                flash('You must be an admin to access this page!', category="danger")
                return redirect(url_for('all_posts'))
            return f(*args, **kwargs)

        return wrapped

    return wrapper


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


@app.route('/home')
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
            current = User(user['id'])
            login_user(current)
            session['email'] = current.email
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

            user = db.find_user_by_email(sign_up_form.email.data)

            if authenticate(sign_up_form.email.data, sign_up_form.password.data) and is_active:
                current = User(user['id'])
                login_user(current)
                session['email'] = current.email
                session['id'] = current.id

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
    # print(User(id))
    return User(id)


# A User class for creating User objects
class User(object):
    def __init__(self, id):
        self.id = id
        user = db.find_user_by_id(self.id)

        if user is not None:
            self.id = user['id']
            self.name = user['name']
            self.email = user['email']
            self.role = user['role']
            self.is_authenticated = True
        else:
            self.id = 'no id'
            self.name = 'no name'
            self.email = 'no email'
            self.role = 'no role'
            self.is_authenticated = False

        self.is_active = True

    def get_id(self):
        return self.id

    def get_role(self):
        return self.role

    def __repr__(self):
        return "<User {}   Email: {}   Role: {}   Is Authenticated: {}   Is Active: {}".format(self.id, self.email, self.role, self.is_authenticated, self.is_active)


# Signs the user out
@app.route('/signout')
def sign_out():
    logout_user()
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


# Allows an admin to create a user
@app.route('/users/new', methods=['GET', 'POST'])
@requires_roles('admin')
def create_user():
    user_form = UserForm()

    if hasattr(current_user, 'role'):
        role = current_user.get_role()
    else:
        role = ""

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

    return render_template('user-form.html', form=user_form, mode='create', role=role)


# Allows an admin to edit a user
@app.route('/users/edit/<id>', methods=['GET', 'POST'])
@requires_roles('admin')
def edit_user(id):
    row = db.find_user_by_id(id)

    if hasattr(current_user, 'role'):
        role = current_user.get_role()
    else:
        role = ""

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

    return render_template('user-form.html', form=user_form, mode='update', role=role)


# Disable a user by their ID (primary key)
@app.route('/users/disable/<id>')
@requires_roles('admin')
def disable_user_by_id(id):
    user = db.find_user_by_id(id)
    db.disable_user_by_id(id)
    flash("User {} disabled".format(user['name']), category='success')
    return redirect(url_for('all_users'))


# Enable a user by their ID (primary key)
@app.route('/users/enable/<id>')
@requires_roles('admin')
def enable_user_by_id(id):
    user = db.find_user_by_id(id)
    db.enable_user_by_id(id)
    flash("User {} enabled".format(user['name']), category='success')
    return redirect(url_for('all_users'))


# Gets a list of all the users in the database
@app.route('/users')
@requires_roles('admin')
def all_users():
    if hasattr(current_user, 'role'):
        role = current_user.get_role()
    else:
        role = ""

    return render_template('all-users.html', users=db.all_users(), role=role)


# Admin dashboard to update users or posts
@app.route('/admin/dashboard', methods=['GET', 'POST'])
@requires_roles('admin')
def admin_dashboard():
    if hasattr(current_user, 'role'):
        role = current_user.get_role()
    else:
        role = ""

    return render_template('admin-dashboard.html', role=role)


# A user's profile
@app.route('/profile', methods=['GET', 'POST'])
@requires_roles('user')
@login_required
def profile():
    if hasattr(current_user, 'role'):
        role = current_user.get_role()
    else:
        role = ""

    query = ProductSearchForm(request.form)

    if request.method == 'POST':
        query_list = query.search.data.lower().split(" ")
        posts = db.search_products(query_list)
        return render_template('posts.html', date=today, search_form=query, posts=posts, mode='results', role=role)

    return render_template('profile.html', search_form=query, role=role)


# A list of the current user's posts
@app.route('/my-posts', methods=['GET', 'POST'])
@requires_roles('user')
@login_required
def my_posts():
    user_id = session['id']
    query = ProductSearchForm(request.form)

    if hasattr(current_user, 'role'):
        role = current_user.get_role()
    else:
        role = ""

    if user_id is None:
        flash('User is not logged in!', category='danger')
        posts = []
    else:
        posts = db.posts_by_user(user_id)

    if request.method == 'POST':
        query_list = query.search.data.lower().split(" ")
        posts = db.search_products(query_list)
        return render_template('posts.html', date=today, search_form=query, posts=posts, mode='results', role=role)

    return render_template('posts.html', date=today, search_form=query, posts=posts, mode='my-posts', role=role)


# A list of the a user's posts
@app.route('/posts/user/<user_id>', methods=['GET', 'POST'])
@requires_roles('user')
@login_required
def user_posts(user_id):
    query = ProductSearchForm(request.form)
    user = db.find_user_by_id(user_id)

    if hasattr(current_user, 'role'):
        role = current_user.get_role()
    else:
        role = ""

    if user_id is None:
        flash('No user with id {}'.format(user_id), category='danger')
        posts = []
    else:
        posts = db.posts_by_user(user_id)

    if request.method == 'POST':
        query_list = query.search.data.lower().split(" ")
        posts = db.search_products(query_list)
        return render_template('posts.html', date=today, search_form=query, posts=posts, mode='results', role=role)

    return render_template('posts.html', date=today, search_form=query, user=user, posts=posts, mode='user', role=role)


# A list of the user's favorites
@app.route('/favorites', methods=['GET', 'POST'])
@requires_roles('user')
@login_required
def my_favorites():
    query = ProductSearchForm(request.form)

    if hasattr(current_user, 'role'):
        role = current_user.get_role()
    else:
        role = ""

    if session:
        user_id = session['id']
        favorites = db.favorites_by_user(user_id)

        if request.method == 'POST':
            query_list = query.search.data.lower().split(" ")
            posts = db.search_products(query_list)
            return render_template('posts.html', date=today, search_form=query, posts=posts, mode='results', role=role)

        return render_template('posts.html', date=today, user_id=user_id, search_form=query, posts=favorites, mode='favorites', role=role)


# Adds a post to favorites
@app.route('/favorites/add/<post_id>')
@requires_roles('user')
@login_required
def add_to_favorites(post_id):
    if session:
        user_id = session['id']

        post = db.find_post_by_id(post_id)
        favorites = db.find_duplicate_in_favorites(user_id, post_id)

        if not favorites:
            db.add_to_favorites(user_id, post_id)
            flash("{} added to favorites".format(post['product']), category='success')
        else:
            flash("{} already added to favorites".format(post['product']), category='danger')

    return redirect(url_for('all_posts'))


@app.route('/favorites/remove/<post_id>')
@requires_roles('user')
@login_required
def remove_from_favorites(post_id):
    if session:
        user_id = session['id']
        favorites = db.favorites_by_user(user_id)

        if favorites:
            db.delete_from_favorites(user_id, post_id)
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
@requires_roles('user')
@login_required
def create_post():
    post_form = PostForm()

    if hasattr(current_user, 'role'):
        role = current_user.get_role()
    else:
        role = ""
    
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
        return render_template('post-form.html', post_form=post_form, mode='create', role=role)


# Edit a post
@app.route('/posts/edit/<id>', methods=['GET', 'POST'])
@requires_roles('user')
@login_required
def edit_post(id):
    row = db.find_post_by_id(id)

    if hasattr(current_user, 'role'):
        role = current_user.get_role()
    else:
        role = ""

    if row is None:
        flash("Post doesn't exist", category='danger')
        return redirect(url_for('all_posts'))

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

    return render_template('post-form.html', post_form=post_form, mode='update', role=role)


# Returns a more in-depth look at a post
@app.route('/posts/<id>', methods=['GET', 'POST'])
def post_details(id):
    post = db.find_post_by_id(id)
    user_id = post['user_id']
    user = db.find_user_by_id(user_id)
    query = ProductSearchForm(request.form)

    if hasattr(current_user, 'role'):
        role = current_user.get_role()
    else:
        role = ""

    if request.method == 'POST':
        query_list = query.search.data.lower().split(" ")
        posts = db.search_products(query_list)
        return render_template('posts.html', date=today, search_form=query, posts=posts, mode='results', role=role)

    if post['user_id'] == current_user.get_id():
        return render_template('post-details.html', date=today, search_form=query, post=post, role=role)
    else:
        return render_template('post-details.html', date=today, search_form=query, post=post, user=user, role=role)


# All the posts in the database - also handles searching
@app.route('/', methods=['GET', 'POST'])
def all_posts():
    query = ProductSearchForm(request.form)
    selected = FilterForm(request.form)

    if hasattr(current_user, 'role'):
        role = current_user.get_role()
    else:
        role = ""

    if selected.data['submit'] is True:
        key_list = []
        for key, value in selected.data.items():
            if key != "submit" and key != "csrf_token":
                if value:
                    key_list.append(key)
        filtered_posts = db.filter_products(key_list)

        if not filtered_posts:
            if not key_list:
                return render_template('posts.html', date=today, filter_form=selected, search_form=query, posts=db.all_posts(), mode='results', role=role)
            else:
                return render_template('posts.html', date=today, filter_form=selected, search_form=query, posts=[], mode='results', role=role)
        else:
            return render_template('posts.html', date=today, filter_form=selected, search_form=query, posts=filtered_posts, mode='results', role=role)

    if query.search.data is not None:
        query_list = query.search.data.lower().split(" ")
        posts = db.search_products(query_list)

        if not posts:
            return render_template('posts.html', date=today, filter_form=selected, search_form=query, posts=[], mode='results', role=role)
        else:
            return render_template('posts.html', date=today, filter_form=selected, search_form=query, posts=posts, mode='results', role=role)
    return render_template('posts.html', date=today, filter_form=selected, search_form=query, posts=db.all_posts(), mode='feed', role=role)


class ProductSearchForm(FlaskForm):
    search = StringField('Search', [DataRequired()])
    submit = SubmitField('Search')


class FilterForm(FlaskForm):
    vegetables = BooleanField('Vegetables')
    fruits = BooleanField('Fruit')
    meat = BooleanField('Meat')
    dairy = BooleanField('Dairy')
    grains = BooleanField('Grains')
    other = BooleanField('Other')
    submit = SubmitField('Filter')


@app.route('/posts/delete/<id>')
@requires_roles('user')
@login_required
def delete_post_by_id(id):
    post = db.find_post_by_id(id)
    if post is not None:
        db.delete_post_by_id(id)
        return redirect(url_for('my_posts'))


if __name__ == '__main__':
    app.run()
