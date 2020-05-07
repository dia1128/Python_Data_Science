
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.2** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Assignment 2 - Pandas Introduction
# All questions are weighted the same in this assignment.
# ## Part 1
# The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on [All Time Olympic Games Medals](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table), and does some basic data cleaning. 
# 
# The columns are organized as # of Summer games, Summer medals, # of Winter games, Winter medals, total # number of games, total # of medals. Use this dataset to answer the questions below.

# In[1]:


import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()


# ### Question 0 (Example)
# 
# What is the first country in df?
# 
# *This function should return a Series.*

# In[2]:


# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value
def answer_zero():
      
    return df.iloc[0]

# You can examine what your function returns by calling it in the cell. If you have questions
# about the assignment formats, check out the discussion forums for any FAQs
answer_zero() 


# ### Question 1
# Which country has won the most gold medals in summer games?
# 
# *This function should return a single string value.*

# In[102]:


def answer_one():
         return df['Gold'].idxmax()

answer_one()


# In[5]:


def answer_two():
    return ((df['Gold'] - df['Gold.1']).idxmax())

answer_two()


# ### Question 2
# Which country had the biggest difference between their summer and winter gold medal counts?
# 
# *This function should return a single string value.*

# ### Question 3
# Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count? 
# 
# $$\frac{Summer~Gold - Winter~Gold}{Total~Gold}$$
# 
# Only include countries that have won at least 1 gold in both summer and winter.
# 
# *This function should return a single string value.*

# In[9]:


def answer_three():
   only_gold = df[(df['Gold'] > 0) & (df['Gold.1'] > 0)]
   
   Summer_Gold = only_gold['Gold']
   Winter_Gold = only_gold['Gold.1']
   Total_Gold = Summer_Gold + Winter_Gold
   difference = (abs((Summer_Gold - Winter_Gold))/Total_Gold).idxmax()
                    
   return difference  

   
answer_three() 

       
    


# ### Question 4
# Write a function that creates a Series called "Points" which is a weighted value where each gold medal (`Gold.2`) counts for 3 points, silver medals (`Silver.2`) for 2 points, and bronze medals (`Bronze.2`) for 1 point. The function should return only the column (a Series object) which you created, with the country names as indices.
# 
# *This function should return a Series named `Points` of length 146*

# In[10]:


def answer_four():
    Gold = df['Gold.2']*3
    Silver = df['Silver.2']*2
    Bronze = df['Bronze.2']
    df['Points'] = (Gold +Silver+Bronze)
    return df['Points']
    
                       
answer_four()


# ## Part 2
# For the next set of questions, we will be using census data from the [United States Census Bureau](http://www.census.gov). Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. [See this document](https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2010-2015/co-est2015-alldata.pdf) for a description of the variable names.
# 
# The census dataset (census.csv) should be loaded as census_df. Answer questions using this as appropriate.
# 
# ### Question 5
# Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
# 
# *This function should return a single string value.*

# In[12]:


census_df = pd.read_csv('census.csv')
census_df.head()


# In[13]:


def answer_five():
    State = census_df.groupby('STNAME')['COUNTY'].agg('sum') #https://jamesrledoux.com/code/group-by-aggregate-pandas
    Maximum = State.idxmax()
    return Maximum
answer_five()
   


# In[144]:


def answer_six():
    State_multiple = census_df.groupby('STNAME')['CENSUS2010POP'].agg('sum')
    State_Most_Three = State_multiple.nlargest(3).index.tolist()
    
    return State_Most_Three

answer_six() #https://stackoverflow.com/questions/40957458/the-first-three-max-value-in-a-column-in-python


# ### Question 7
# Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)
# 
# e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.
# 
# *This function should return a single string value.*

# In[119]:


def answer_seven():
    new_census = census_df[census_df['SUMLEV'] == 50][[9, 10, 11, 12, 13, 14]]

    minValuesObj =new_census.min(axis=1)
    maxValuesObj =new_census.max(axis=1)
    highest_difference = (maxValuesObj - minValuesObj).idxmax()
    return   census_df['CTYNAME'].iloc[highest_difference]

answer_seven()


# ### Question 8
# In this datafile, the United States is broken up into four regions using the "REGION" column. 
# 
# Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
# 
# *This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df (sorted ascending by index).*

# In[137]:


def answer_eight():

    Region =  census_df[((census_df['REGION'] == 1 ) | (census_df['REGION'] == 2 )) & (census_df['CTYNAME'].str.startswith("Washington")) & ((census_df['POPESTIMATE2015'])> (census_df['POPESTIMATE2014']) ) ]
    return Region[['STNAME', 'CTYNAME']]
answer_eight()


# In[ ]:




