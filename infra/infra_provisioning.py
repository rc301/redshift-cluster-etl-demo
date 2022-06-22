import configparser
import psycopg2


def drop_tables(cur, conn):
    pass

def create_tables(cur, conn):
    pass


def main():
    config = configparser.ConfigParser()
    config.read('dwh_infra.cfg')



if __name__ == "__main__":
    main()