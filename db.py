from flask import g
import psycopg2
import psycopg2.extras

data_source_name = 'host=faraday.cse.taylor.edu dbname=esmarrel user=esmarrel password=mowozate'


def open_db_connection():
    g.connection = psycopg2.connect(data_source_name)
    g.cursor = g.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


def close_db_connection():
    g.cursor.close()
    g.connection.close()
