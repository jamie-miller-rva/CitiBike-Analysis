#!/usr/bin/env python3
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE

def create_trips_raw(connection):
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE trips_raw (\
        trip_duration numeric,\
        start_timestamp timestamp without time zone,\
        stop_timestamp timestamp without time zone,\
        start_station_id text,\
        start_station_name text,\
        start_station_latitude numeric,\
        start_station_longitude numeric,\
        end_station_id text,\
        end_station_name text,\
        end_station_latitude numeric,\
        end_station_longitude numeric,\
        bike_id text,\
        user_type text,\
        birth_year text,\
        gender text\
        );')
    #record = cursor.fetchone()
    cursor.close()

def create_trips(connection):
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE trips (\
        id serial primary key,\
        start_date date,\
        stop_date date,	\
        start_time time,\
        stop_time time,\
        start_timestamp timestamp without time zone,\
        stop_timestamp timestamp without time zone,\
        trip_dur_sec numeric,\
        trip_dur_min numeric,	\
        start_station_id integer,\
        end_station_id integer,\
        bike_id integer,\
        user_type text,\
        birth_year integer,	\
        gender integer\
        );')

    #record = cursor.fetchone()
    cursor.close()

def create_temp_stations(connection):
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE temp_stations (\
        id serial primary key,\
        external_id integer not null,\
        name text,\
        latitude numeric,\
        longitude numeric\
        );')

    #record = cursor.fetchone()
    cursor.close()

def main():
    try:
        connection = psycopg2.connect(user = "fjwgbummysitcn",
                                    password = "5737578ea8836385ebf061369d160d689dc40b68bac0910ebbd5d8cf0fb11d4a",
                                    host = "ec2-184-73-169-163.compute-1.amazonaws.com",
                                    port = "5432",
                                    database = "dea4gdgm9cltlv")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE
        #create_trips_raw(connection)
        #create_trips(connection)
        
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):
                connection.close()
                print("PostgreSQL connection is closed")

main()