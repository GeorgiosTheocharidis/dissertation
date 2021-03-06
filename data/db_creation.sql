drop table if exists energy;
drop table if exists weather;

-- Build the energy table

CREATE TABLE energy
(
    date_time                                   timestamp,
    generation_biomass                          REAL,
    generation_fossil_brown_coal_lignite        REAL,
    generation_fossil_coal_derived_gas          REAL,
    generation_fossil_gas                       REAL,
    generation_fossil_hard_coal                 REAL,
    generation_fossil_oil                       REAL,
    generation_fossil_oil_shale                 REAL,
    generation_fossil_peat                      REAL,
    generation_geothermal                       REAL,
    generation_hydro_pumped_storage_aggregated  REAL,
    generation_hydro_pumped_storage_consumption REAL,
    generation_hydro_run_of_river_and_poundage  REAL,
    generation_hydro_water_reservoir            REAL,
    generation_marine                           REAL,
    generation_nuclear                          REAL,
    generation_other                            REAL,
    generation_other_renewable                  REAL,
    generation_solar                            REAL,
    generation_waste                            REAL,
    generation_wind_offshore                    REAL,
    generation_wind_onshore                     REAL,
    forecast_solar_day_ahead                    REAL,
    forecast_wind_offshore_eday_ahead           REAL,
    forecast_wind_onshore_day_ahead             REAL,
    total_load_forecast                         REAL,
    total_load_actual                           REAL,
    price_day_ahead                             REAL,
    price_actual                                REAL
);

\COPY energy FROM '/vagrant/data/energy_dataset.csv' DELIMITER ',' CSV HEADER;


CREATE TABLE weather
(
    date_time           timestamp,
    city_name           varchar(32),
    temp                real,
    temp_min            real,
    temp_max            real,
    pressure            real,
    humidity            real,
    wind_speed          real,
    wind_deg            real,
    rain_1h             real,
    rain_3h             real,
    snow_3h             real,
    clouds_all          real,
    weather_id          real,
    weather_main        varchar(32),
    weather_description varchar(32),
    weather_icon        varchar(32)
);

\COPY weather FROM '/vagrant/data/weather_features.csv' DELIMITER ',' CSV HEADER;

update weather set city_name = trim(city_name);
update weather set weather_main = trim(weather_main);
update weather set weather_description = trim(weather_description);


ALTER TABLE energy
    DROP COLUMN generation_fossil_coal_derived_gas,
    DROP COLUMN generation_fossil_oil_shale,
    DROP COLUMN generation_fossil_peat,
    DROP COLUMN generation_geothermal,
    DROP COLUMN generation_hydro_pumped_storage_aggregated,
    DROP COLUMN generation_marine,
    DROP COLUMN generation_wind_onshore,
    DROP COLUMN generation_wind_offshore,
    DROP COLUMN forecast_wind_offshore_eday_ahead;
