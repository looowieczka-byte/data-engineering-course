
Module 3:
CREATE OR REPLACE EXTERNAL TABLE `zoomcamp_module3.yellow_taxi_trip_records_external_table`
OPTIONS (
  format = 'parquet',
  uris = ['gs://taxi-data-de-zoomcamp/yellow_tripdata_2024-*.parquet']
);
CREATE OR REPLACE TABLE `zoomcamp_module3.yellow_taxi_trip_records_external_table_non_partitioned` AS
SELECT * FROM `zoomcamp_module3.yellow_taxi_trip_records_external_table`;



SELECT COUNT( DISTINCT(PULocationID)) FROM `zoomcamp_module3.yellow_taxi_trip_records_external_table_non_partitioned`; #115.12mb
SELECT COUNT( DISTINCT(PULocationID)) FROM `zoomcamp_module3.yellow_taxi_trip_records_external_table`; #0B

Ex3:

SELECT PULocationID FROM `zoomcamp_module3.yellow_taxi_trip_records_external_table_non_partitioned`; #155.12
SELECT PULocationID,DOLocationID  FROM `zoomcamp_module3.yellow_taxi_trip_records_external_table_non_partitioned`; #310



Ex4:
SELECT COUNT(*) from `zoomcamp_module3.yellow_taxi_trip_records_external_table_non_partitioned` where fare_amount =0;

EX5:
CREATE OR REPLACE TABLE zoomcamp_module3.yellow_taxi_trip_records_partitioned_clustered
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS

EX6
SELECT * FROM zoomcamp_module3.yellow_taxi_trip_records_external_table_non_partitioned;
SELECT DISTINCT(VendorID) from `zoomcamp_module3.yellow_taxi_trip_records_external_table_non_partitioned` where tpep_dropoff_datetime >= '2024-03-01' and tpep_dropoff_datetime <='2024-03-15'; #310.24
SELECT DISTINCT(VendorID) from `zoomcamp_module3.yellow_taxi_trip_records_partitioned_clustered` where tpep_dropoff_datetime >= '2024-03-01' and tpep_dropoff_datetime <='2024-03-15'; #26.84
