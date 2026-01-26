#!/usr/bin/env python
# coding: utf-8




import pandas as pd

get_ipython().system('uv add sqlalchemy')

get_ipython().system('uv add psycopg2-binary')

from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

from tqdm.auto import tqdm

pg_user = 'root'
pg_port = '5432'
pg_pass = 'root'

green_prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data/'
green = 'green_tripdata_2025-11.parquet'
zone_prefix= 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/'
zone = 'taxi_zone_lookup.csv'



df = pd.read_csv(
    zone_prefix + zone
)
df.head()



print(pd.io.sql.get_schema(df, name='zone_taxi_data', con=engine))



df.head(n=0).to_sql(name='zone_taxi_data', con=engine, if_exists='replace')



df_iter = pd.read_csv(
    zone_prefix + zone,
    iterator=True,
    chunksize=100000
)




for df_chunk in tqdm(df_iter):
    df_chunk.to_sql(name='zone_taxi_data', con=engine, if_exists='append')



df_green = pd.read_parquet(
    green_prefix + green
)
df_green.head()



green_csv = df_green.to_csv('green_tripdata_2025-11.csv', index=False)



df_green = pd.read_csv('green_tripdata_2025-11.csv')
df_green.head()



print(pd.io.sql.get_schema(df_green, name='green_taxi_data', con=engine))



df_green.head(n=0).to_sql(name='green_taxi_data', con=engine, if_exists='replace')




df_iter = pd.read_csv(
    'green_tripdata_2025-11.csv',
        iterator=True,
    chunksize=100000
)




for df_chunk in tqdm(df_iter):
    df_chunk.to_sql(name='green_taxi_data', con=engine, if_exists='append')





prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

df = pd.read_csv(
    prefix + 'yellow_tripdata_2021-01.csv.gz',
    dtype=dtype,
    parse_dates=parse_dates
)



df.head()


get_ipython().system('uv add sqlalchemy')


# In[7]:


get_ipython().system('uv add psycopg2-binary')


# In[10]:


from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')


# In[11]:


print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[12]:


df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[13]:


df_iter = pd.read_csv(
    prefix + 'yellow_tripdata_2021-01.csv.gz',
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000
)


# In[14]:


for df_chunk in df_iter:
    print(len(df_chunk))


# In[16]:


get_ipython().system('uv add tqdm')


# In[17]:


from tqdm.auto import tqdm


# In[18]:


for df_chunk in tqdm(df_iter):
    df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')






