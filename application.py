from flask import Flask, session, request, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, PasswordField, SelectField
from wtforms.validators import Length, NumberRange, Email, InputRequired, EqualTo, DataRequired

from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Team Bryson Key'


import db

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


@app.before_request
def before_request():
    db.open_db_connection()


@app.teardown_request
def teardown_request(exception):
    db.close_db_connection()


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


@app.route('/', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit() and login_form.validate():
        user = db.find_user_by_email(login_form.email.data)

        if user:
            is_active = True
        else:
            is_active = False

        if authenticate(login_form.email.data, login_form.password.data) and is_active:
            current = User(login_form.email.data)
            login_user(current)
            session['username'] = current.email

            print(current)
            print(session['username'])

            return redirect(url_for('all_posts'))
        else:
            flash('Invalid email address or password', category="danger")
            return redirect(url_for('login'))

    return render_template('index.html', login_form=login_form)


def authenticate(email, password):
    valid_users = db.all_users()

    for user in valid_users:
        if email == user['email'] and user['password'] == password:
            return email
    return None


@login_manager.user_loader
def load_user(id):
    return User(id)


class User(object):

    def __init__(self, email):
        self.email = email
        user = db.find_user_by_email(self.email)
        if user is not None:
            # self.name = db.find_member_info(self.email)['first_name']
            self.user_id = user['id']
        else:
            self.name = 'no name'

        self.is_active = True
        self.is_authenticated = True

    def get_id(self):
        return self.email

    def __repr__(self):
        return "<User '{}' {} {}".format(self.email, self.is_authenticated, self.is_active)


# The form to create or update a user
class UserForm(FlaskForm):
    name = StringField('Name', validators=[Length(min=1, max=50)])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Save User')


# Allows an administrator to create a user
@app.route('/users/create', methods=['GET', 'POST'])
def create_user():
    user_form = UserForm()

    if user_form.validate_on_submit():
        user = db.find_user_by_email(user_form.email.data)

        if user is not None:
            flash("User {} already exists".format(user_form.email.data))
        else:
            rowcount = db.create_user(user_form.name.data,
                                      user_form.email.data,
                                      user_form.password.data,
                                      5.0,
                                      True)

            if rowcount == 1:
                flash("User {} created".format(user_form.email.data))
                return redirect(url_for('all_users'))
            else:
                flash("New user not created")

    return render_template('user-form.html', form=user_form, mode='create')


# Edit a post by a user's ID (primary key)
@app.route('/users/edit/<id>', methods=['GET', 'POST'])
def edit_user(id):
    row = db.find_user_by_id(id)

    if row is None:
        flash("User doesn't exist")
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
            flash("User '{}' updated".format(user_form.email.data))
            return redirect(url_for('all_users'))
        else:
            flash('User not updated')

    return render_template('user-form.html', form=user_form, mode='update')


# Disable a user by their ID (primary key)
@app.route('/users/disable/<id>')
def disable_user_by_id(id):
    # posts = db.posts_by_user(id)
    #
    # db.hide_favorite_by_user_id(id)
    #
    # for post in posts:
    #     db.hide_favorite_by_post_id(post[0])
    #     db.hide_post_by_user_id(id)

    db.disable_user_by_id(id)
    flash("User {} disabled".format(id))
    return redirect(url_for('all_users'))


# Disable a user by their ID (primary key)
@app.route('/users/enable/<id>')
def enable_user_by_id(id):
    # user = db.find_user_by_id(id)
    # posts = db.posts_by_user(id)

    # if user is None:
    #     flash("User doesn't exist")
    #     return redirect(url_for('all_users'))
    #
    # db.delete_favorite_by_user_id(id)
    #
    # for post in posts:
    #     db.delete_favorite_by_post_id(post[0])
    #     db.delete_post_by_user_id(id)

    db.enable_user_by_id(id)
    flash("User {} enabled".format(id))
    return redirect(url_for('all_users'))


# Gets a list of all the users in the database
@app.route('/users')
def all_users():
    return render_template('all-users.html', users=db.all_users())


# Testing page
@app.route('/test')
def test():
    return render_template("test.html")


# A user's profile
@app.route('/profile')
def profile():
    return render_template("profile.html")


# A list of the user's posts
@app.route('/posts/<user_id>')
def user_posts(user_id):
    user = db.find_user_by_id(user_id)
    if user is None:
        flash('No user with id {}'.format(user_id))
        posts = []
    else:
        posts = db.posts_by_user(user_id)
    return render_template('user-posts.html', user=user, posts=posts)


@app.route('/favorites/1')
def temp_user_favorites():
    favs = db.favorites_by_user(1)
    return render_template('favorites.html', user=1, favorites=favs)


# A list of the user's posts
# @app.route('/favorites/<user_id>')
# def user_favorites(user_id):
#     user = db.find_user_by_id(user_id)
#     if user is None:
#         flash('No user with id {}'.format(user_id))
#         favs = []
#     else:
#         favs = db.favorites_by_user(user_id)
#     return render_template('favorites.html', user=user, favorites=favs)


# Adds a post to favorites
# TODO: Update to use current user when authentication gets added
# TODO: Change if True to check for duplicates once users are working
@app.route('/favorites/add/<post_id>')
def add_to_favorites(post_id):
    if True:
        db.add_to_favorites(post_id)
        flash("Post {} added to favorites".format(post_id))
    # else:
    #     flash("Post {} already added to favorites".format(post_id))
    return redirect(url_for('all_posts'))


# A user's settings
@app.route('/settings')
def settings():
    return render_template("settings.html")
  

# The form to create or edit a post
class PostForm(FlaskForm):
    product = StringField('Product (ex. Strawberries)', validators=[Length(min=1, max=40, message='Product must be between 1 and 40 characters')])
    description = StringField('Description (<150 characters)', validators=[Length(min=1, max=150, message='Description must be between 1 and 150 characters')])
    price = FloatField('Price (ex. 5.99)', validators=[NumberRange(min=0.01, max=1000, message='Price must be between $0.01 and $1000')])
    quantity = IntegerField('Quantity (ex. 100)', validators=[NumberRange(min=1, max=1000, message='Quantity must be between 1 and 1000')])
    category = SelectField('Category', choices=[('Vegetables', 'Vegetables'),
                                                ('Fruits', 'Fruits'),
                                                ('Meat', 'Meat'),
                                                ('Dairy', 'Dairy'),
                                                ('Grains', 'Grains')])
    loc = StringField('Location (ex. Indianapolis)', validators=[Length(min=1, max=40, message='Location must be between 1 and 40 characters')])

    submit = SubmitField('Save Post')


# Create a post
@app.route('/posts/create', methods=['GET', 'POST'])
def create_post():
    post_form = PostForm()

    if post_form.validate_on_submit():
            rowcount = db.create_post(post_form.price.data,
                                      post_form.quantity.data,
                                      post_form.product.data,
                                      post_form.category.data,
                                      post_form.loc.data,
                                      post_form.description.data)

            if rowcount == 1:
                flash("Post added successfully")
                return redirect(url_for('all_posts'))
            else:
                flash("New post not created")

    for error in post_form.errors:
        for field_error in post_form.errors[error]:
            flash(field_error)
    return render_template('post-form.html', form=post_form, mode='create')


# Edit a post
@app.route('/posts/edit/<id>', methods=['GET', 'POST'])
def edit_post(id):
    row = db.find_post_by_id(id)

    if row is None:
        flash("Post doesn't exist")
        return redirect(url_for('index'))

    post_form = PostForm(price=row['price'],
                         quantity=row['quantity'],
                         product=row['product'],
                         loc=row['loc'],
                         description=row['description'])

    if post_form.validate_on_submit():
        rowcount = db.update_post(post_form.price.data,
                                  post_form.quantity.data,
                                  post_form.product.data,
                                  post_form.loc.data,
                                  post_form.description.data,
                                  id)

        if rowcount == 1:
            flash("Post '{}' updated".format(post_form.product.data))
            return redirect(url_for('index'))
        else:
            flash('Post not updated')

    return render_template('post-form.html', form=post_form, mode='update')


# All the posts in the database - also handles searching
@app.route('/posts', methods=['GET', 'POST'])
def all_posts():
    query = ProductSearchForm(request.form)

    if request.method == 'POST':
        query_list = query.search.data.lower().split(" ")
        results = db.search_products(query_list)

        if not results:
            flash('No Results Found')
            return render_template('all-posts.html', form=query, posts=db.all_posts())
        else:
            return render_template('results.html', form=query, results=results, query=query)
    return render_template('all-posts.html', form=query, posts=db.all_posts())


class ProductSearchForm(FlaskForm):
    search = StringField('Search', [DataRequired()])
    submit = SubmitField('Search')


# @app.route('/posts/delete/<id>')
# def delete_post_by_id(id):
#     post = db.find_post_by_id(id)
#     if post is None:
#         flash("Post doesn't exist")
#     else:
#         db.delete_post_by_id(id)
#         flash("Post deleted")
#         return redirect(url_for('all_posts'))


if __name__ == '__main__':
    app.run()
