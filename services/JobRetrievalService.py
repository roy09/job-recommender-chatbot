import pandas as pd

df_data = pd.read_csv('data/seek_australia.csv')

def retreiveJobs(job_title='Business Analyst', job_type='Full Time', city='Sydney'):
    searchResultDf = df[(df['city']=='Sydney') & (df['job_title']=="Business Analyst") & (df['job_type']=="Full Time")]
