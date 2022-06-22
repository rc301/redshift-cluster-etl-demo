import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""

""")

staging_songs_table_create = ("""

""")

songplay_table_create = ("""
create table songplays
(
    songplay_id     INTEGER     IDENTITY(0,1) NOT NULL,
    start_time      TIMESTAMP   NOT NULL,
    user_id         INTEGER     NOT NULL,
    level           VARCHAR(10) NOT NULL, 
    song_id         INTEGER     NOT NULL,
    artist_id       INTEGER     NOT NULL,
    session_id      INTEGER     NOT NULL,
    location        VARCHAR     NOT NULL,
    user_agent      VARCHAR     NOT NULL
)
""")

user_table_create = ("""
create table users
(
    user_id     INTEGER     IDENTITY(0,1) NOT NULL,
    first_name  VARCHAR(50) NOT NULL,
    last_name   VARCHAR(50) NOT NULL,
    gender      VARCHAR()   NOT NULL,
    level       VARCHAR(50) NOT NULL
)
""")

song_table_create = ("""
create table songs
(
    song_id     INTEGER     IDENTITY(0,1) NOT NULL,
    title       VARCHAR()   NOT NULL,
    artist_id   INTEGER     NOT NULL,
    year        INTEGER     NOT NULL,
    duration    INTEGER     NOT NULL
)
""")

artist_table_create = ("""
create table artists
(
    artist_id   INTEGER             IDENTITY(0,1) NOT NULL,
    name        VARCHAR()           NOT NULL,
    location    VARCHAR()           NOT NULL,
    latitude    DOUBLE PRECISION    NOT NULL,
    longitude   FLOAT               NOT NULL
)
""")

time_table_create = ("""
create table time
(
    start_time  TIMESTAMP   NOT NULL,
    hour        SMALLINT    NOT NULL, 
    day         SMALLINT    NOT NULL, 
    week        SMALLINT    NOT NULL,
    month       SMALLINT    NOT NULL,
    year        SMALLINT    NOT NULL,
    weekday     SMALLINT    NOT NULL
)
""")

# STAGING TABLES

staging_events_copy = ("""
""").format()

staging_songs_copy = ("""
""").format()

# FINAL TABLES

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
