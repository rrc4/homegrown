from flask import g
import psycopg2
import psycopg2.extras

''' Uncomment your database before working on your code, and comment it out again when pushing '''
# data_source_name = 'host=faraday.cse.taylor.edu dbname=joeyferg user=joeyferg password=kavibeda'
# data_source_name = 'host=faraday.cse.taylor.edu dbname=joeschuette user=joeschuette password=kahilewo'
data_source_name = 'host=faraday.cse.taylor.edu dbname=rrc4 user=rrc4 password=decisage'
# data_source_name = 'host=faraday.cse.taylor.edu dbname=esmarrel user=esmarrel password=mowozate'
# data_source_name = 'host=faraday.cse.taylor.edu dbname=harrisonvdn user=harrisonvdn password=mudojose'


def open_db_connection():
    g.connection = psycopg2.connect(data_source_name)
    g.cursor = g.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


def close_db_connection():
    g.cursor.close()
    g.connection.close()


def create_user(first_name, last_name, email, password, phone, rating, active):
    query = '''
        INSERT INTO "user" (first_name, last_name, email, password, phone, rating, active)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(phone)s, %(rating)s, %(active)s)
    '''
    g.cursor.execute(query, {'first_name': first_name, 'last_name': last_name, 'email': email,
                             'password': password, 'phone': phone, 'rating': rating, 'active': active})
    g.connection.commit()
    return g.cursor.rowcount


def find_user_by_email(email):
    g.cursor.execute('SELECT * FROM "user" WHERE email = %(email)s', {'email': email})
    return g.cursor.fetchone()


def find_user_by_id(id):
    g.cursor.execute('SELECT * FROM "user" WHERE id = %(id)s', {'id': id})
    return g.cursor.fetchone()


def all_users():
    query = '''
        SELECT * FROM "user" u
    '''
    g.cursor.execute(query)
    return g.cursor.fetchall()


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


def delete_user_by_id(user_id):
    g.cursor.execute('DELETE FROM "user" WHERE id = %(user_id)s', {'user_id': user_id})
    g.connection.commit()
    return g.cursor.rowcount


def find_post_by_id(id):
    g.cursor.execute('SELECT * FROM post WHERE id = %(id)s', {'id': id})
    return g.cursor.fetchone()


def create_post(price, quantity, product, loc, description):
    query = '''
        INSERT INTO post (price, quantity, product, loc, description)
        VALUES (%(price)s, %(quantity)s, %(product)s, %(loc)s, %(description)s)
    '''
    g.cursor.execute(query, {'price': price, 'quantity': quantity, 'product': product, 'loc': loc, 'description': description})
    g.connection.commit()
    return g.cursor.rowcount


def all_posts():
    query = '''
        SELECT * FROM post p
    '''
    g.cursor.execute(query)
    return g.cursor.fetchall()


def update_post(price, quantity, product, loc, description, post_id):
    query = '''
        UPDATE post 
        SET price = %(price)s, product = %(product)s, quantity = %(quantity)s, loc = %(loc)s, description = %(description)s
        WHERE id = %(id)s
    '''
    g.cursor.execute(query, {'id': post_id, 'price': price, 'quantity': quantity, 'product': product, 'loc': loc, 'description': description})
    g.connection.commit()
    return g.cursor.rowcount


def delete_post_by_id(post_id):
    g.cursor.execute('DELETE FROM post WHERE id = %(post_id)s', {'post_id': post_id})
    g.connection.commit()
    return g.cursor.rowcount


def posts_by_user(user_id):
    g.cursor.execute('SELECT * FROM post WHERE user_id = %(user_id)s', {'user_id': user_id})
    g.connection.commit()
    return g.cursor.fetchall()
