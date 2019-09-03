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
	
	--load monthly csv files into trips_raw is currently manually executed via "imports" into trips_raw table
--load weather and dates via manual "import"

--once trip_raw table is populated, the following scripts load data into 
--the data tables

--first, you must process the station data

--load start station data
INSERT INTO temp_stations (external_id, name, latitude, longitude)
SELECT DISTINCT
  start_station_id,
  start_station_name,
  NULLIF(ROUND(start_station_latitude, 6), 0),
  NULLIF(ROUND(start_station_longitude, 6), 0)
FROM trips_raw
WHERE start_station_id IS NOT NULL

--load end station data
INSERT INTO temp_stations (external_id, name, latitude, longitude)
SELECT DISTINCT
  end_station_id,
  end_station_name,
  NULLIF(ROUND(end_station_latitude, 6), 0),
  NULLIF(ROUND(end_station_longitude, 6), 0)
FROM trips_raw
WHERE end_station_id IS NOT NULL

--load distinct stations into stations table from the temp_stations
INSERT INTO stations (external_id, name, latitude, longitude)
SELECT DISTINCT
  external_id, 
  name, 
  latitude, 
  longitude
FROM temp_stations

--load trips table
INSERT INTO trips
(start_date, stop_date, start_time, stop_time, start_timestamp, stop_timestamp, trip_dur_sec, trip_dur_min, start_station_id, end_station_id, bike_id, user_type, birth_year, gender)
SELECT
  date(start_timestamp) as start_date,
  date(stop_timestamp) as stop_date,
  cast(start_timestamp as time) as start_time,
  cast(stop_timestamp as time) as stop_time,
  start_timestamp,
  stop_timestamp,
  trip_duration as trip_dur_sec,
  round(trip_duration/60,2) as trip_dur_min,
  ss.id,
  es.id,
  bike_id,
  user_type,
  NULLIF(NULLIF(birth_year, ''), 'NULL')::int,
  NULLIF(NULLIF(gender, ''), 'NULL')::int
FROM trips_raw t
  INNER JOIN stations ss
    ON t.start_station_id = ss.external_id
    AND ROUND(t.start_station_longitude, 6) = ss.longitude
    AND ROUND(t.start_station_latitude, 6) = ss.latitude
  INNER JOIN stations es
    ON t.end_station_id = es.external_id
    AND ROUND(t.end_station_longitude, 6) = es.longitude
    AND ROUND(t.end_station_latitude, 6) = es.latitude
WHERE t.start_station_id IS NOT NULL
  AND t.end_station_id IS NOT NULL
ORDER BY start_timestamp  

--//////////////////////////
--misc queries
select count(*) from trips

select start_date, count(start_timestamp)
from trips
group by start_date

select * from trips

--creat view of consolidated data
CREATE VIEW all_data AS (
  SELECT
	d.*,
	d.year - t.birth_year as age,
    t.*,
    ss.name AS start_station_name,
    ss.latitude AS start_station_latitude,
    ss.longitude AS start_station_longitude,
    es.name AS end_station_name,
    es.latitude AS end_station_latitude,
    es.longitude AS end_station_longitude,
	w.precipitation as precip,
	w.snow_depth,
	w.snowfall,
	w.min_temperature as low_temp,
	w.max_temperature as high_temp,
	w.average_wind_speed as wind_speed
  FROM trips t
    INNER JOIN stations ss ON t.start_station_id = ss.id
    INNER JOIN stations es ON t.end_station_id = es.id
	LEFT OUTER JOIN dates d ON t.start_date = d.date
	LEFT OUTER JOIN weather w ON t.start_date = w.date
WHERE d.year = 2019  
ORDER BY t.start_timestamp	
);

--// other queries
select * from all_data
select * from dates

select count(*) from all_data