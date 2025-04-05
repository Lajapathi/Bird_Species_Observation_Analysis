### libraries

# ! pip3 install pandas
# ! pip3 install numpy
# ! pip3 install openpyxl
# ! pip3 install sqlalchemy
# ! pip3 install psycopg2-binary

import pandas as pd
import numpy as np

### Sheet to dataframe

# file path

forest_info='/Library/guvi/Bird_Monitoring_Data_FOREST.xlsx'
grassland_info='/Library/guvi/Bird_Monitoring_Data_GRASSLAND.xlsx'

# excel data

forest_data=pd.ExcelFile(forest_info)
grassland_data=pd.ExcelFile(grassland_info)

# get sheet names

forest_Sname=forest_data.sheet_names

grassland_Sname=grassland_data.sheet_names

# sheet data to a dictionary

forest_Sdict={sheet:forest_data.parse(sheet) for sheet in forest_Sname}

grassland_Sdict={sheet : grassland_data.parse(sheet) for sheet in grassland_Sname}

# dataframe forest

forest_df=pd.concat(
    [df.assign(Sheet=sheet_name) for sheet_name , df in forest_Sdict.items()],ignore_index=True
)



# dataframe grassland

grassland_df= pd.concat(
    [df.assign(Sheet=sheet_name) for sheet_name, df in grassland_Sdict.items()],ignore_index=True
)

#forest_df.head()
#grassland_df.head()

forest_df.to_csv('forest_df.csv')
grassland_df.to_csv('grassland_df.csv')



### CSV to Dataframe

forest_df=pd.read_csv('forest_df.csv') 
grassland_df=pd.read_csv('grassland_df.csv')
forest_df.shape, grassland_df.shape

#checking null value combination with respect to other columns

result_f = forest_df[forest_df['ID_Method'].isna()]['Scientific_Name']
print(result_f)
filtered_rows = forest_df[forest_df['ID_Method'].isna()]

"""
   Missing column.   total_na.   na %.    alternative       reference for alternative

1. Sub_Unit_code     7824/8546   92%      'not having'            assumption
2. ID_Method         1/8546      <1%      'Singing'         from Observer,Distance,Scientific_Name
3. Distance          92/8546      1%       >=100 Meters            assumption
4. Sex               5183/8564   61%       Undetermined           Undetermined 98%
5. AcceptedTSN       9/8546      <1%       815358                 from Scientific_Name[(Haemor)hous mexicanus]

"""
## filling na values with alternatives

forest_df['Sub_Unit_Code']=forest_df['Sub_Unit_Code'].fillna('not having')
forest_df['ID_Method']=forest_df['ID_Method'].fillna('Singing')
forest_df['Distance']=forest_df['Distance'].fillna('>=100 Meters')
forest_df['Sex']=forest_df['Sex'].fillna('Undetermined')
forest_df['AcceptedTSN']=forest_df['AcceptedTSN'].fillna(815358)
forest_df['Distance'] = forest_df['Distance'].replace(r'\s+', '', regex=True)  # Remove spaces
forest_df['Distance'] = forest_df['Distance'].replace(r'[a-zA-Z]', '', regex=True) # Remove alphabets
forest_df.isna().sum()


#### grassland data
#checking null value combination with respect to other columns

result_g = grassland_df[grassland_df['Scientific_Name']=='Corvus caurinus']['Scientific_Name']
print(result_g.count())
filtered_rows = grassland_df[grassland_df['ID_Method'].isna()]
result_gs = grassland_df[grassland_df['TaxonCode'].isna()]['Scientific_Name']
print(result_gs)
"""
  Missing column.   total_na.   na %.    alternative       reference for alternative

1.Sub_Unit_Code.    8531/8531.  100.     'not having'.      assumption
2.ID_Method.        1/8531.      1%      'Visualization'    from Observer,Distance,Scientific_Name
3. Distance         1394/8546    16%       >=100 Meters     assumption
4. AcceptedTSN       9/8546      <1%       815358           from Scientific_Name[(Haemor)hous mexicanus]
5a. TaxonCode         1           <1%      35821            from Scientific_Name[(Corvu)s caurinus]
5b. TaxonCode         1           <1%      18435            from Scientific_Name[(Ardeo)la bacchus]

"""



## filling na values with alternatives
grassland_df['Sub_Unit_Code']=grassland_df['Sub_Unit_Code'].fillna('not having')
grassland_df['ID_Method']=grassland_df['ID_Method'].fillna('Visualization')
grassland_df['Distance']=grassland_df['Distance'].fillna('>=100 Meters')
grassland_df['AcceptedTSN']=grassland_df['AcceptedTSN'].fillna(815358)
grassland_df.loc[grassland_df['Scientific_Name'] == 'Corvus caurinus', 'TaxonCode'] = grassland_df.loc[grassland_df['Scientific_Name'] == 'Corvus caurinus', 'TaxonCode'].fillna(35821)
grassland_df.loc[grassland_df['Scientific_Name'] == 'Ardeola bacchus', 'TaxonCode'] = grassland_df.loc[grassland_df['Scientific_Name'] == 'Ardeola bacchus', 'TaxonCode'].fillna(18435)
grassland_df['Distance'] = grassland_df['Distance'].replace(r'\s+', '', regex=True)  # Remove spaces
grassland_df['Distance'] = grassland_df['Distance'].replace(r'[a-zA-Z]', '', regex=True) # Remove alphabets
grassland_df.isna().sum()


### Add season in dataframe
# coverting date column into datatime format

forest_df['Date'] = pd.to_datetime(forest_df['Date'], errors='coerce')
grassland_df['Date'] = pd.to_datetime(grassland_df['Date'], errors='coerce')
# function for getting season based on month

def get_season(month):
  if month in [12,1,2]:
    return 'Winter'
  elif month in [3,4,5]:
    return 'Spring'
  elif month in [6,7,8]:
    return 'Summer'
  else:
    return 'Fall'


# season for forest data
forest_df['Month']= forest_df['Date'].dt.month
forest_df['Season']=forest_df['Month'].apply(get_season)

# season for grassland data

grassland_df['Month']=grassland_df['Date'].dt.month
grassland_df['Season']=grassland_df['Month'].apply(get_season)


# Get distinct rows from the DataFrame
distinct_forest_df = forest_df.drop_duplicates()

# Display the distinct DataFrame
print(forest_df.shape)
forest_df.to_csv('forest_df_cleaned.csv') 
grassland_df.to_csv('grassland_df_cleaned.csv')


### Database actions

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float , Boolean, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


#### connection
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

#### create forest_data_check table
#create table for dataframe
# dtypes in forest_df bool(4), datetime64[ns](1), float64(3), int32(1), int64(3), object(20)

Base=declarative_base()

class forest(Base):
  __tablename__='forest_data_check'

  Sno=Column(Integer,primary_key=True,autoincrement=True)
  for column , dtype in forest_df.dtypes.items():
    if dtype=='object':
      column_type=String
    elif dtype=='bool':
      column_type=Boolean
    elif dtype=='datetime64[ns]':
      column_type=DateTime
    elif dtype=='float64':
      column_type=Float
    elif dtype=='int32':
      column_type=Integer
    elif dtype=='int64':
      column_type=Integer
    else:
      column_type=String

    locals()[column]=Column(column,column_type)

  def __repr__(self):
        # Create a dynamic string that includes all column names and their values
        columns = [f"{col}={getattr(self, col)}" for col in self.__table__.columns.keys()]
        return f"<User({', '.join(columns)})>"

Base.metadata.create_all(engine)
Session=sessionmaker(bind=engine)
session=Session()
session.commit()

#### create grassland_data_check table
#create table for dataframe
# dtypes in forest_df bool(4), datetime64[ns](1), float64(3), int32(1), int64(3), object(20)

Base=declarative_base()

class forest(Base):
  __tablename__='grassland_data_check'

  Sno=Column(Integer,primary_key=True,autoincrement=True)
  for column , dtype in grassland_df.dtypes.items():
    if dtype=='object':
      column_type=String
    elif dtype=='bool':
      column_type=Boolean
    elif dtype=='datetime64[ns]':
      column_type=DateTime
    elif dtype=='float64':
      column_type=Float
    elif dtype=='int32':
      column_type=Integer
    elif dtype=='int64':
      column_type=Integer
    else:
      column_type=String

    locals()[column]=Column(column,column_type)

  def __repr__(self):
        # Create a dynamic string that includes all column names and their values
        columns = [f"{col}={getattr(self, col)}" for col in self.__table__.columns.keys()]
        return f"<User({', '.join(columns)})>"
  
Base.metadata.create_all(engine)
Session=sessionmaker(bind=engine)
session=Session()
session.commit()

#### Database instertion #####
forest_df.columns = forest_df.columns.str.lower()
grassland_df.columns = grassland_df.columns.str.lower()
forest_df.to_sql('forest_data',engine,if_exists='replace',index=False)
grassland_df.to_sql('grassland_data',engine,if_exists='replace',index=False)
