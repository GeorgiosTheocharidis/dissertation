SQL_SELECT_TEMPS = """
select
    a.temp,
    floor(extract(dow from a.date_time))::integer as week_day,
    floor(extract(hour from a.date_time))::integer as hour,
    total_load_actual as load
from
    weather a,
    energy b
where
    a.date_time = b.date_time and
    a.city_name = 'Valencia'
"""

SQL_MASTER = """
select
    SIN (0.448 * extract(dow from date_time)) as week_day,
    SIN (0.130 * extract(hour from date_time)) as hour,
    (Bilbao + 
    Valencia + 
    Madrid +
    Seville +
    Barcelona)/5 as temp,
    load
from
    master
limit 10000
"""

SQL_INCLUDE_PREVIOUS = """
select
    SIN (0.448 * extract(dow from a.date_time)) as week_day,
    SIN (0.130 * extract(hour from a.date_time)) as hour,
    a.bilbao,
    a.valencia,
    a.madrid,
    a.seville,
    a.barcelona,
    ((avg(b.total_load_actual)  over (rows between 1 preceding and current row)) * 2 - b.total_load_actual) as previous,
    a.load
from 
    master a, energy b
where
    a.date_time = b.date_time
limit 20000
"""

SQL_INCLUDE_MOV_AVG_24 = """
select
    SIN (0.448 * extract(dow from a.date_time)) as week_day,
    SIN (0.130 * extract(hour from a.date_time)) as hour,
     (Bilbao + 
    Valencia + 
    Madrid +
    Seville +
    Barcelona)/5 as temp,
    (avg(b.total_load_actual)  over (rows between 2 preceding and current row)) as previous2,
    (avg(b.total_load_actual)  over (rows between 5 preceding and current row)) as previous5,
    (avg(b.total_load_actual)  over (rows between 12 preceding and current row)) as previous12,
    (avg(b.total_load_actual)  over (rows between 24 preceding and current row)) as previous24,
    a.load
from
    master a, energy b
where
    a.date_time = b.date_time 
limit 30000
"""

CONN_STR = "postgres://vagrant:test@localhost:5432/energy"
REAL_ESTATE_CONN_STR = "postgres://vagrant:test@localhost:5432/realestate"


SQL_TESTING = """
select
    a.temp,
    extract(dow from a.date_time) as week_day,
    floor(extract(hour from a.date_time)) ::integer as hour,
    total_load_actual
from
    weather a,
    energy b
where
    a.date_time = b.date_time and
    a.city_name = 'Valencia'
LIMIT 10;
"""

SQL_SELECT_NEXT_LOAD = """
select
    SIN (0.448 * extract(dow from a.date_time)) as week_day,
    SIN (0.130 * extract(hour from a.date_time)) as hour,
    (avg(a.load)  over (rows between 1 preceding and current row)) as previous1,
    (avg(a.load)  over (rows between 2 preceding and current row)) as previous2,
    (avg(a.load)  over (rows between 3 preceding and current row)) as previous3,
    (avg(a.load)  over (rows between 5 preceding and current row)) as previous5,
    (avg(a.load)  over (rows between 8 preceding and current row)) as previous8,
    (avg(a.load)  over (rows between 13 preceding and current row)) as previous13,
    (avg(a.load)  over (rows between 24 preceding and current row)) as previous24,
    a.average_temp,
    a.load,
    CASE
      WHEN (a.load < b.load) THEN 1
      ELSE 0
    END AS prediction
from
    master as a, master as b
where
    b.date_time = a.date_time + interval '1 hours'
"""


SQL_SELECT_NEXT_LOAD_2 = """
select
    SIN (0.448 * extract(dow from a.date_time)) as week_day,
    SIN (0.130 * extract(hour from a.date_time)) as hour,
    a.average_temp,
    a.load,
    (avg(a.load)  over (rows between 1 preceding and current row)) as previous1,
    (avg(a.load)  over (rows between 2 preceding and current row)) as previous2,
    (avg(a.load)  over (rows between 3 preceding and current row)) as previous3,
    (avg(a.load)  over (rows between 5 preceding and current row)) as previous5,
    (avg(a.load)  over (rows between 8 preceding and current row)) as previous8,
    (avg(a.load)  over (rows between 13 preceding and current row)) as previous13,
    (avg(a.load)  over (rows between 24 preceding and current row)) as previous24,
    CASE
      WHEN (a.load < b.load) THEN 1
      ELSE 0
    END AS prediction
from
    master as a, master as b
where
    b.date_time = a.date_time + interval '1 hours'
"""

SQL_HOUR_STATS = """
select 
    extract(hour FROM date_time) as hour,
    avg (next_hour_load_diff) as average,
    stddev(next_hour_load_diff) as standard_deviation
from 
    master 
group by extract(hour FROM date_time);
"""

SQL_INSERT_MEDIAN_DIFF_PER_HOUR = """
delete from diff_per_hour;

insert into diff_per_hour 
select  extract(hour from a.date_time), avg(a.next_hour_load_diff)
from master a, ensemble_data b 
where train=1 
and a.date_time = b.date_time
group by extract(hour from a.date_time);
"""
