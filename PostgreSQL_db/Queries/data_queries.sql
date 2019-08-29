--special summarizations

--// trips per date
SELECT
	start_date,
	count(start_station_id),
  	count(end_station_id)
FROM all_data
GROUP BY start_date
ORDER by start_date

--// trips per month
SELECT
	mmm_yy,
	count(start_station_id),
  	count(end_station_id)
FROM all_data
GROUP BY mmm_yy
ORDER by mmm_yy

--// trips per hour --- work in process
SELECT
	DATEPART(hour,start_timestamp) as Hour,
	count(start_station_id)
FROM all_data


--// min/max duration by date
SELECT
	start_date,
	min(trip_dur_min) as min,
	round(avg(trip_dur_min),2) as avg,
  	max(trip_dur_min) as max
FROM all_data
GROUP BY start_date
ORDER by start_date

--//  bike_id counts per day
SELECT
	start_date,
	day,
	bike_id,
	count(*)
FROM all_data
GROUP BY start_date, day, bike_id

--//////////
ORDER BY start_date
ORDER by start_date