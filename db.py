from flask import g
import psycopg2
import psycopg2.extras

''' Uncomment your database before working on your code, and comment it out again when pushing '''
# data_source_name = 'host=faraday.cse.taylor.edu dbname=joeyferg user=joeyferg password=kavibeda'
# data_source_name = 'host=faraday.cse.taylor.edu dbname=joeschuette user=joeschuette password=kahilewo'
# data_source_name = 'host=faraday.cse.taylor.edu dbname=rrc4 user=rrc4 password=decisage'
# data_source_name = 'host=faraday.cse.taylor.edu dbname=esmarrel user=esmarrel password=mowozate'
# data_source_name = 'host=faraday.cse.taylor.edu dbname=harrisonvdn user=harrisonvdn password=mudojose'


# Open database connection
def open_db_connection():
    g.connection = psycopg2.connect(data_source_name)
    g.cursor = g.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


# Close database connection
def close_db_connection():
    g.cursor.close()
    g.connection.close()


# Create a user
def create_user(first_name, last_name, email, password, phone, rating, active):
    query = '''
        INSERT INTO "user" (first_name, last_name, email, password, phone, rating, active)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(phone)s, %(rating)s, %(active)s)
    '''
    g.cursor.execute(query, {'first_name': first_name, 'last_name': last_name, 'email': email,
                             'password': password, 'phone': phone, 'rating': rating, 'active': active})
    g.connection.commit()
    return g.cursor.rowcount


# Find a user by their email
def find_user_by_email(email):
    g.cursor.execute('SELECT * FROM "user" WHERE email = %(email)s', {'email': email})
    return g.cursor.fetchone()


# Find a user by name
def find_user_by_id(id):
    g.cursor.execute('SELECT * FROM "user" WHERE id = %(id)s', {'id': id})
    return g.cursor.fetchone()


# Returns a list of all users
def all_users():
    g.cursor.execute('SELECT * FROM "user"')
    return g.cursor.fetchall()


# Update a user
def update_user(first_name, last_name, email, password, phone, user_id):
    query = '''
        UPDATE "user"
        SET first_name = %(first_name)s, last_name = %(last_name)s, 
            email = %(email)s, password = %(password)s, phone = %(phone)s
        WHERE id = %(id)s
    '''
    g.cursor.execute(query, {'id': user_id, 'first_name': first_name, 'last_name': last_name,
                             'email': email, 'password': password, 'phone': phone})
    g.connection.commit()
    return g.cursor.rowcount


# Delete a user by their ID
def delete_user_by_id(user_id):
    g.cursor.execute('DELETE FROM "user" WHERE id = %(user_id)s', {'user_id': user_id})
    g.connection.commit()
    return g.cursor.rowcount


# Finds a post by it's ID
def find_post_by_id(id):
    g.cursor.execute('SELECT * FROM post WHERE id = %(id)s', {'id': id})
    return g.cursor.fetchone()


# Finds all posts by a user
def posts_by_user(user_id):
    g.cursor.execute('SELECT * FROM post WHERE user_id = %(user_id)s', {'user_id': user_id})
    g.connection.commit()
    return g.cursor.fetchall()


# Finds all favorites by a user
def favorites_by_user(user_id):
    query = '''
      SELECT * FROM favorite f
      INNER JOIN post p ON p.id = f.post_id
      INNER JOIN "user" u ON u.id = f.user_id 
      WHERE u.id = %(user_id)s
    '''
    g.cursor.execute(query, {'user_id': user_id})
    g.connection.commit()
    return g.cursor.fetchall()


# Deletes all favorites by a user's ID
def delete_favorite_by_user_id(user_id):
    g.cursor.execute('DELETE FROM favorite WHERE user_id = %(user_id)s', {'user_id': user_id})
    g.connection.commit()
    return g.cursor.rowcount


# Deletes all favorited posts with a certain post_id
def delete_favorite_by_post_id(post_id):
    g.cursor.execute('DELETE FROM favorite WHERE post_id = %(post_id)s', {'post_id': post_id})
    g.connection.commit()
    return g.cursor.rowcount


# Adds a post to favorites
# TODO: This will need to be updated when we get actual authentication (currently it just adds everything to user 1's favorites)
def add_to_favorites(post_id):
    query = '''
        INSERT INTO favorite (user_id, post_id) VALUES (1, %(post_id)s);
    '''
    g.cursor.execute(query, {'post_id': post_id})
    g.connection.commit()
    return g.cursor.rowcount


# Remove a post from favorites
def remove_from_favorites(post_id):
    g.cursor.execute('DELETE FROM favorite WHERE post_id = %(post_id)s', {'post_id': post_id})
    g.connection.commit()
    return g.cursor.fetchall()


# Creates a post
# TODO: This will need to be changed to create a post for the user signed in, not just user_id 1
def create_post(price, quantity, product, category, loc, description):
    query = '''
        INSERT INTO post (user_id, price, quantity, product, "category", loc, description)
        VALUES (1, %(price)s, %(quantity)s, %(product)s, %(category)s, %(loc)s, %(description)s)
    '''
    g.cursor.execute(query, {'price': price, 'quantity': quantity, 'product': product, 'category': category, 'loc': loc, 'description': description})
    g.connection.commit()
    return g.cursor.rowcount


# Returns the entire post table
def all_posts():
    g.cursor.execute('SELECT * FROM post')
    return g.cursor.fetchall()


# Updates/edits a post
def update_post(price, quantity, product, loc, description, post_id):
    query = '''
        UPDATE post 
        SET price = %(price)s, product = %(product)s, quantity = %(quantity)s, loc = %(loc)s, description = %(description)s
        WHERE id = %(id)s
    '''
    g.cursor.execute(query, {'id': post_id, 'price': price, 'quantity': quantity, 'product': product, 'loc': loc, 'description': description})
    g.connection.commit()
    return g.cursor.rowcount


# Deletes a single post by post ID
def delete_post_by_id(post_id):
    g.cursor.execute('DELETE FROM post WHERE id = %(post_id)s', {'post_id': post_id})
    g.connection.commit()
    return g.cursor.rowcount


# Deletes all posts by a user's ID
def delete_post_by_user_id(user_id):
    g.cursor.execute('DELETE FROM post WHERE user_id = %(user_id)s', {'user_id': user_id})
    g.connection.commit()
    return g.cursor.rowcount
