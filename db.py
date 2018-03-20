from flask import g
import psycopg2
import psycopg2.extras

''' Uncomment your database before working on your code, and comment it out again when pushing '''
# data_source_name = 'host=faraday.cse.taylor.edu dbname=joeyferg user=joeyferg password=kavibeda'
# data_source_name = 'host=faraday.cse.taylor.edu dbname=joeschuette user=joeschuette password=kahilewo'
# data_source_name = 'host=faraday.cse.taylor.edu dbname=rrc4 user=rrc4 password=decisage'
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
        INSERT INTO "user" (first_name, last_name, email, phone, password, rating, active)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(phone)s, %(password)s, %(rating)s, %(active)s)
    '''
    g.cursor.execute(query, {'first_name': first_name, 'last_name': last_name, 'email': email,
                             'phone': phone, 'password': password, 'rating': rating, 'active': active})
    g.connection.commit()
    return g.cursor.rowcount


def find_user(email):
    g.cursor.execute('SELECT * FROM "user" WHERE email = %(email)s', {'email': email})
    return g.cursor.fetchone()


def all_users():
    query = '''
        SELECT * FROM "user" u
    '''
    g.cursor.execute(query)
    return g.cursor.fetchall()


def find_post(id):
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

