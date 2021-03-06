cd data/zip-files
unzip energy_dataset.csv.zip energy_dataset.csv
unzip weather_features.csv.zip weather_features.csv

mv energy_dataset.csv ..
mv weather_features.csv ..

createdb energy;
cd ..
psql energy -f db_creation.sql
psql energy -f db_create_master.sql


sudo -u postgres bash -c "psql -c \"grant all privileges on database energy to vagrant;\""
