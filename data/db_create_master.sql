Drop table if exists master;

Delete
from weather
where date_time in
      (select date_time
       from (SELECT date_time, count(*) as c
             FROM weather
             group by date_time
             having count(*) != 5) as x);

CREATE TABLE master
(
    date_time    timestamp,
    Bilbao       REAL,
    Valencia     REAL,
    Madrid       REAL,
    Seville      REAL,
    Barcelona    REAL,
    average_temp REAL,
    next_hour_load_diff REAL, -- this.load - next_hour.load
    load         REAL
);


INSERT INTO master (date_time)
SELECT date_time
FROM weather
group by date_time;



UPDATE
    master a
SET Bilbao = b.temp from weather b
where a.date_time = b.date_time and b.city_name = 'Bilbao';

UPDATE
    master a
SET Valencia = b.temp from weather b
where a.date_time = b.date_time and b.city_name = 'Valencia';

UPDATE
    master a
SET Madrid = b.temp from weather b
where a.date_time = b.date_time and b.city_name = 'Madrid';

UPDATE
    master a
SET Seville = b.temp from weather b
where a.date_time = b.date_time and b.city_name = 'Seville';

UPDATE
    master a
SET Barcelona = b.temp from weather b
where a.date_time = b.date_time and b.city_name = 'Barcelona';

UPDATE
    master a
SET load = b.total_load_actual from energy b
where a.date_time = b.date_time;


Delete
from master
where date_time in
      (select date_time
       from (SELECT date_time FROM master where load is NULL) as x);


Update master set average_temp = (Bilbao + Valencia + Madrid + Seville + Barcelona) / 5;


CREATE TEMP TABLE load_diffs AS
select
       a.date_time as  date_time,
       b.load - a.load as next_hour_load_diff
from master as a,
     master as b
where
      b.date_time = a.date_time + interval '1 hours';


update master a set
    next_hour_load_diff = b.next_hour_load_diff
from load_diffs b
where a.date_time = b.date_time;

delete from master  where next_hour_load_diff is NULL;