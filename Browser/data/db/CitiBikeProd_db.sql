-- Database: CitiBikeProd_db

-- DROP DATABASE "CitiBikeProd_db";

CREATE DATABASE "CitiBikeProd_db"
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
	
	CREATE TABLE trips_raw (
  trip_duration numeric,
  start_timestamp timestamp without time zone,
  stop_timestamp timestamp without time zone,
  start_station_id text,
  start_station_name text,
  start_station_latitude numeric,
  start_station_longitude numeric,
  end_station_id text,
  end_station_name text,
  end_station_latitude numeric,
  end_station_longitude numeric,
  bike_id text,
  user_type text,
  birth_year text,
  gender text
);  
	
CREATE TABLE trips (
  id serial primary key,
  start_date date,
  stop_date date,	
  start_time time,
  stop_time time,
  start_timestamp timestamp without time zone,
  stop_timestamp timestamp without time zone,
  trip_dur_sec numeric,
  trip_dur_min numeric,	
  start_station_id integer,
  end_station_id integer,
  bike_id integer,
  user_type text,
  birth_year integer,	
  gender integer
);



CREATE TABLE temp_stations (
  id serial primary key,
  external_id integer not null,
  name text,
  latitude numeric,
  longitude numeric
);

CREATE TABLE stations (
  id serial primary key,
  external_id integer not null,
  name text,
  latitude numeric,
  longitude numeric
);

CREATE TABLE weather (
  station_id text,
  station_name text,
  date date primary key,
  precipitation numeric,
  snow_depth numeric,
  snowfall numeric,
  max_temperature numeric,
  min_temperature numeric,
  average_wind_speed numeric
);

CREATE TABLE dates (
  date date primary key,
  month_num numeric,
  dofm numeric,
  day text,	
  week numeric,
  month text,
  mmm_yy text,
  quarter text,
  year numeric
);