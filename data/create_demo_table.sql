Drop table if exists demo;

CREATE TABLE demo
(
    hour    int,
    value1  REAL,
    value2  REAL
);

\COPY demo FROM '/vagrant/data/demo.csv' DELIMITER ',' CSV HEADER;
