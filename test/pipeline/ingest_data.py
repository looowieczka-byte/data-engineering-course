#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import urllib.request





url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/'
filename = 'green_tripdata_2025-11.parquet'
urllib.request.urlretrieve(url, filename)


# In[2]:


prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'


# In[3]:


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


# In[4]:


df.head()


# In[5]:


len(df)


# In[6]:


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


# In[ ]:




