import pandas as pd
from sqlalchemy import create_engine


#Database credential
host='localhost'
port='5432'
username='postgres'
password='laja1103'
database='Bird_Monitoring'

# connection string
connection_string=f"postgresql://{username}:{password}@{host}:{port}/{database}"

#creating engine
engine=create_engine(connection_string)

#qurey 
forest_query='''SELECT * FROM forest_data'''
grassland_query='''SELECT * FROM grassland_data'''

def rawdata():
    forest_df=pd.read_sql_query(forest_query,engine)
    grassland_df=pd.read_sql(grassland_query,engine)
    forest_df["date"] = pd.to_datetime(forest_df["date"]).dt.date  
    grassland_df["date"] = pd.to_datetime(grassland_df["date"]).dt.date  

    return(forest_df,grassland_df)

