import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """Load data into staging tables.

    Args:
        cur (psycopg2.cursor): Allows Python code to execute PostgreSQL command in a database session.
        conn (psycopg2.connection): Handles the connection to a PostgreSQL database instance. It encapsulates a database session.
    """
    
    # Send copy queries to database to be executed
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """Insert data into star schema tables.

    Args:
        cur (psycopg2.cursor): Allows Python code to execute PostgreSQL command in a database session.
        conn (psycopg2.connection): Handles the connection to a PostgreSQL database instance. It encapsulates a database session.
    """
    
    # Send insert queries to database to be executed
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """Orchestrate each step of the ETL job.
    """
    # Get configuration information from file
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    # Connect to database
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    # Extract, Transform and Load data
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    # Close connection to database
    conn.close()

if __name__ == "__main__":
    main()