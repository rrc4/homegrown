from flask import g
import psycopg2
import psycopg2.extras

# Database Utilities ########################################

data_source_name = 'host=faraday.cse.taylor.edu dbname=rrc4 user=rrc4 password=decisage'

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
