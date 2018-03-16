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


def create_post(price, quantity, product, loc):
    query = '''
        INSERT INTO post (price, quantity, product, loc)
        VALUES (%(price)s, %(quantity)s, %(product)s, %(loc)s)
    '''
    g.cursor.execute(query, {'price': price, 'quantity': quantity, 'product': product, 'loc': loc})
    g.connection.commit()
    return g.cursor.rowcount


def all_members():
    query = '''
        SELECT * FROM member m
    '''
    g.cursor.execute(query)
    return g.cursor.fetchall()


def all_posts():
    query = '''
        SELECT * FROM post p
    '''
    g.cursor.execute(query)
    return g.cursor.fetchall()
