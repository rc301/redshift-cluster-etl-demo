import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')
DWH_ROLE_ARN = config.get("IAM_ROLE","ARN")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS tb_staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS tb_staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS tb_fact_songplays;"
user_table_drop = "DROP TABLE IF EXISTS tb_dim_users;"
song_table_drop = "DROP TABLE IF EXISTS tb_dim_songs;"
artist_table_drop = "DROP TABLE IF EXISTS tb_dim_artists;"
time_table_drop = "DROP TABLE IF EXISTS tb_dim_time;"

# CREATE TABLES

staging_events_table_create= ("""
create table tb_staging_events
(
    artist          VARCHAR(200),
    auth            VARCHAR(10),
    firstName       VARCHAR(50),
    gender          VARCHAR(1),
    itemInSession   INTEGER,
    lastName        VARCHAR(50),
    length          DOUBLE PRECISION,
    level           VARCHAR(5),
    location        VARCHAR(100),
    method          VARCHAR(4),
    page            VARCHAR(20),
    registration    DOUBLE PRECISION,
    sessionId       INTEGER,
    song            VARCHAR(200),
    status          INTEGER,
    ts              TIMESTAMP,
    userAgent       VARCHAR(150),
    userId          INTEGER
);
""")

staging_songs_table_create = ("""
create table tb_staging_songs
(
    artist_id           VARCHAR(20),
    artist_latitude     DOUBLE PRECISION,
    artist_location     VARCHAR(200),
    artist_longitude    DOUBLE PRECISION,
    artist_name         VARCHAR(200),
    duration            DOUBLE PRECISION,
    num_songs           SMALLINT,
    song_id             VARCHAR(20),
    title               VARCHAR(200),
    year                SMALLINT
);
""")

songplay_table_create = ("""
create table tb_fact_songplays
(
    songplay_id     INTEGER     IDENTITY(0,1) NOT NULL,
    start_time      TIMESTAMP   NOT NULL,
    user_id         INTEGER     NOT NULL,
    level           VARCHAR(10) NOT NULL, 
    song_id         VARCHAR(20) NOT NULL,
    artist_id       VARCHAR(20) NOT NULL,
    session_id      INTEGER     NOT NULL,
    location        VARCHAR(100) NOT NULL,
    user_agent      VARCHAR(150)     NOT NULL
);
""")

user_table_create = ("""
create table tb_dim_users
(
    user_id     INTEGER         NOT NULL,
    first_name  VARCHAR(50)     NOT NULL,
    last_name   VARCHAR(50)     NOT NULL,
    gender      VARCHAR(1)      NOT NULL,
    level       VARCHAR(5)      NOT NULL
);
""")

song_table_create = ("""
create table tb_dim_songs
(
    song_id     VARCHAR(20)         NOT NULL,
    title       VARCHAR(200)        NOT NULL,
    artist_id   VARCHAR(20)         NOT NULL,
    year        SMALLINT            NOT NULL,
    duration    DOUBLE PRECISION    NOT NULL
);
""")

artist_table_create = ("""
create table tb_dim_artists
(
    artist_id   VARCHAR(20)         NOT NULL,
    name        VARCHAR(200)        NOT NULL,
    location    VARCHAR(200)        ,
    latitude    DOUBLE PRECISION    ,
    longitude   DOUBLE PRECISION    
);
""")

time_table_create = ("""
create table tb_dim_time
(
    start_time  TIMESTAMP   NOT NULL,
    hour        SMALLINT    NOT NULL, 
    day         SMALLINT    NOT NULL, 
    week        SMALLINT    NOT NULL,
    month       SMALLINT    NOT NULL,
    year        SMALLINT    NOT NULL,
    weekday     SMALLINT    NOT NULL
);
""")

# STAGING TABLES

staging_events_copy = ("""
    copy tb_staging_events 
    from 's3://udacity-dend/log_data'
    credentials 'aws_iam_role={}'
    region 'us-west-2' 
    format as json 's3://udacity-dend/log_json_path.json'
    timeformat as 'epochmillisecs'
;
""").format(DWH_ROLE_ARN)

staging_songs_copy = ("""
    copy tb_staging_songs 
    from 's3://udacity-dend/song_data'
    credentials 'aws_iam_role={}'
    region 'us-west-2'
    format as json 'auto ignorecase';
""").format(DWH_ROLE_ARN)

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO tb_fact_songplays 
(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT
    a.ts            as start_time,      
    a.userId        as user_id,         
    a.level         as level,           
    b.song_id       as song_id,         
    b.artist_id     as artist_id,       
    a.sessionId     as session_id,      
    a.location      as location,        
    a.userAgent     as user_agent     
FROM tb_staging_events as a
JOIN tb_staging_songs as b
    on upper(trim(a.artist)) = upper(trim(b.artist_name))
    and upper(trim(a.song)) = upper(trim(b.title))
WHERE trim(a.page) = 'NextSong'
;
""")

user_table_insert = ("""
INSERT INTO tb_dim_users
(user_id, first_name, last_name, gender, level)
SELECT
    userId as user_id,     
    firstName as first_name,
    lastName as last_name,
    gender as gender,
    level as level
FROM tb_staging_events
WHERE trim(page) = 'NextSong'
;
""")

song_table_insert = ("""
INSERT INTO tb_dim_songs
(song_id, title, artist_id, year, duration)
SELECT
    song_id as song_id,  
    title as title,    
    artist_id as artist_id,
    year as year,     
    duration as duration 
FROM tb_staging_songs;
""")

artist_table_insert = ("""
INSERT INTO tb_dim_artists
(artist_id, name, location, latitude, longitude)
SELECT
    artist_id as artist_id,
    artist_name as name,     
    artist_location as location, 
    artist_latitude as latitude, 
    artist_longitude as longitude
FROM tb_staging_songs;
""")

time_table_insert = ("""
INSERT INTO tb_dim_time
(start_time, hour, day, week, month, year, weekday)
SELECT
    ts as start_time,
    EXTRACT(hour FROM ts) as hour,      
    EXTRACT(day FROM ts) as day,       
    EXTRACT(week FROM ts) as week,      
    EXTRACT(month FROM ts) as month,     
    EXTRACT(year FROM ts) as year,      
    EXTRACT(weekday FROM ts) as weekday   
FROM tb_staging_events;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
