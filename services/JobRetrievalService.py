import pandas as pd

data = pd.read_csv('data/cleaned.csv', delimiter = '\t', encoding = 'utf-8', usecols=['Title'], error_bad_lines=False, nrows = 10000)

def retreiveJobs(job_title='Data Analyst'):
    return data[data['Title']==job_title]