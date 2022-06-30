import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """Drop tables in the database

    Args:
        cur (_type_): _description_
        conn (_type_): _description_
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """Create tables in the database

    Args:
        cur (_type_): _description_
        conn (_type_): _description_
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """The main function that executes the drop and create tables statements in the database
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()