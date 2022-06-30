import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """Loading data into staging tables.

    Args:
        cur (_type_): _description_
        conn (_type_): _description_
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """Inserts data into star schema tables.

    Args:
        cur (_type_): _description_
        conn (_type_): _description_
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """The main function that executes each step of the ETL job.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()

if __name__ == "__main__":
    main()