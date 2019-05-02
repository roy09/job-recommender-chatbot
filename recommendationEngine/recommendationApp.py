import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
import re

data = pd.read_csv('cleaned.csv', delimiter = '\t', encoding = 'utf-8', usecols=['Title','Description','Requirements'], error_bad_lines=False, nrows = 10000)
nltk.download('stopwords')

data['Requirements'] = data.Requirements.str.replace('\r\n', '')
data['Requirements'] = data.Requirements.str.replace('\\r', '')

data = data[data.Requirements.notnull()]
data = data[data.Title.notnull()]
data = data[data.Description.notnull()]
data = data[data.Title != "TEST"]
data = data[data.Description != ","]

def text_scrubber(values):
    result = []
    for string in values:
        # Regex as explained above
        temp = re.sub('(\(.*\))', '', string)
        temp = re.sub('&#39;|\x92', '\'', temp)
        temp = re.sub(' &amp; |&amp;|\x95|:|;|&|\.|/| and ', ',', temp)
        temp = re.sub('\w*:\s+', ', ', temp)
        
        result.append(temp)
    return result


def tokenizer(data):
    # Custom stop words that come up very often but don't say much about the job title.
    stops = ['manager', 'responsibilities', 'used', 'skills', 'duties', 'work', 'worked', 'daily',
             'services', 'job', 'using', '.com', 'end', 'prepare', 'prepared', 'lead', 'requirements','#39'] + list(stopwords.words('english'))
    values, ids, resume_ids = [],[],[]
    count = 0
    for idx, row in data.iterrows():
        
        # Split on commas
        array = row['Requirements'].lower().split(',')
        for x in array:
            # make sure the value is not empty or all numeric values or in the stop words list
            if x != '' and not x.lstrip().rstrip() in stops and not x.lstrip().rstrip().isdigit():
                # make sure single character results are the letter 'C' (programming language)
                if len(x) > 1 or x == 'C':
                    # drop stuff > 4 gram
                    if len(x.split(' ')) <= 4:
                        # update lists
                        
                        values.append(x.lstrip().rstrip())
                        ids.append(count)
                        count+=1
    
    # New dataframe with updated values.
    result_df = pd.DataFrame()
    
    result_df['Requirements'] = values
    return result_df


data2= data.copy()
data2['Requirements'] = data2['Requirements'].astype(str)
data2['Requirements'] = text_scrubber(data2['Requirements'])
data2['Requirements'] = data2.Requirements.str.replace('\r\n', '')
data2['Requirements'] = data2.Requirements.str.replace('\\r', '')
test_data = tokenizer(data2)

voc = test_data['Requirements'].unique()


from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from scipy.cluster.hierarchy import dendrogram, ward
from sklearn.feature_extraction import text
from sklearn.metrics.pairwise import cosine_similarity

data2['Description'] = data2['Description'].astype(str)

data2['Description'] = [x.replace("&nbsp;"," ").replace("\x92"," ").replace("\x95"," ").replace('&amp;'," ") \
                             .replace('*'," ").replace("."," ").replace("co&#39;s","").replace("\xae&quot;","") \
                             .replace("&#39;s","").replace("&quot;","").replace("?","").replace("&#39;s","") \
                             .replace("@","").replace("\x96","")
                             for x in data2['Description']]

mine = ['manager', 'amp', 'nbsp', 'responsibilities', 'used', 'skills', 'duties', 'work', 'worked', 'daily',
       'services', 'job', 'using', 'com', 'end', 'prepare', 'prepared', 'lead', 'requirements']
vec = TfidfVectorizer(analyzer='word', ngram_range=(1,2), token_pattern='[a-zA-z]{3,50}', max_df=0.2, min_df=2,
                      max_features=10000, stop_words=text.ENGLISH_STOP_WORDS.union(mine), decode_error='ignore', vocabulary=None, binary=False)

description_matrix2 = vec.fit_transform(data2['Requirements']+data2['Description'])
description_matrix2 = pd.DataFrame(description_matrix2.todense())
description_matrix2.columns = vec.get_feature_names()

vec2 = TfidfVectorizer(vocabulary=voc, decode_error='ignore')
skills_matrix2 = vec2.fit_transform(data2['Requirements']+data2['Description'])
skills_matrix2 = pd.DataFrame(skills_matrix2.todense())
skills_matrix2.columns = vec2.get_feature_names()

jobtitle_matrix = pd.concat([skills_matrix2, description_matrix2], axis=1)

pca = PCA(n_components=100, random_state=42)
comps = pca.fit_transform(jobtitle_matrix)

print(jobtitle_matrix.head())

comps = pd.DataFrame(comps)

cltr = AgglomerativeClustering(n_clusters=6)
cltr.fit(comps)

# Add new column containing cluster number to sample, comps, and feature matrix dataframes
data['cluster_no'] = cltr.labels_

X = comps
y = data['cluster_no']


X_train, X_test, y_train, y_test = train_test_split(X,y, stratify=y, random_state=42)
lr = LogisticRegression(C=10, penalty='l2', multi_class='multinomial', solver='sag', max_iter=1000)
lr.fit(X_train, y_train)
lr.score(X_test, y_test)

lr.fit(X, y)

comps['cluster_no'] = y.values
comps.set_index('cluster_no', inplace=True)

def give_suggestions(resume_text):
    # Vectorize user's skills and job descriptions
    desc = pd.DataFrame(vec.transform([resume_text]).todense())
    desc.columns = vec.get_feature_names()
    skillz = pd.DataFrame(vec2.transform([resume_text]).todense())
    skillz.columns = vec2.get_feature_names()
    mat = pd.concat([skillz, desc], axis=1)

    # Tranform feature matrix with pca
    user_comps = pd.DataFrame(pca.transform(mat))

    # Predict cluster for user and print cluster number
    cluster = lr.predict(user_comps)[0]
    

    # Calculate cosine similarity
    cos_sim = pd.DataFrame(cosine_similarity(user_comps,comps[comps.index==cluster]))

    # Get job titles from sample2 to associate cosine similarity scores with jobs
    data_for_cluster = data[data['cluster_no']==cluster]
    cos_sim = cos_sim.T.set_index(data_for_cluster.index)
    cos_sim.columns = ['score']

    # Print the top ten suggested jobs for the user's cluster
    result = cos_sim.sort_values('score', ascending=False)[:5]
    return data.iloc[result.index]['Title']