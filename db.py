from flask import g
import psycopg2
import psycopg2.extras

data_source_name = 'host=faraday.cse.taylor.edu dbname=joeyferg user=joeyferg password=kavibeda'


def open_db_connection():
    g.connection = psycopg2.connect(data_source_name)
    g.cursor = g.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


def close_db_connection():
    g.cursor.close()
    g.connection.close()


#def create_member(destination, year, semester):
 #   """Create a new member."""
 #   query = '''
#INSERT INTO trip (destination, year, semester)
#VALUES (%(destination)s, %(year)s, %(semester)s)
 #   '''
  #  g.cursor.execute(query, {'destination': destination, 'year': year, 'semester': semester})
   # g.connection.commit()
    #return g.cursor.rowcount
