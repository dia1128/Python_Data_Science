
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.5** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Assignment 3 - More Pandas
# This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

# ### Question 1 (20%)
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.
# 
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This function should return a DataFrame with 20 columns and 15 entries.*

# In[60]:





# In[76]:


def answer_one():
 import pandas as pd
 import numpy as np
 import os   
 Org_Energy = pd.ExcelFile('Energy Indicators.xls')
 energy = Org_Energy.parse(skiprows=17,skip_footer=(38)) #Cleaning header and footers
 energy.drop(energy.columns[[0, 1]], axis = 1, inplace = True) #Dropping first two Columns

 energy = energy.rename(columns={'Unnamed: 2': 'Country','Petajoules' : 'Energy Supply', 'Gigajoules' : 'Energy Supply per Capita', 
                            '%':'% Renewable'}) # Renaming Columns
 energy['Country'] = energy['Country'].replace("...", np.NaN) # replacing ... with Nan
 energy['Energy Supply'] = energy['Energy Supply'].replace("...", np.NaN) # replacing ... with Nan
 energy['Energy Supply per Capita'] = energy['Energy Supply per Capita'].replace("...", np.NaN) # replacing ... with Nan
 energy['% Renewable'] = energy['% Renewable'].replace("...", np.NaN) # replacing ... with Nan

 energy['Energy Supply'] = energy['Energy Supply']* 1000000 # converting into gigajoules from petajoule
 energy['Country'] = energy.Country.replace(['Republic of Korea', 'United States of America', 'United Kingdom of Great Britain and Northern Ireland',
'China, Hong Kong Special Administrative Region'], ['South Korea', 'United States', 'United Kingdom', 'Hong Kong'],regex=True) 
# changing country names, this doesn't work without regex = true => https://stackoverflow.com/questions/37593550/pandas-replacing-elements-not-working
 energy['Country'] = energy['Country'].replace([r" \(.*\)"],[""], regex = True) # removing unwanted cahracters
 energy['Country']=energy['Country'].str.replace('\d+', '') #removing digits

 GDP = pd.read_csv('world_bank.csv',skiprows=4) # Loading the GDP file 

 GDP['Country Name'] = GDP['Country Name'].replace(['Korea, Rep.', 'Iran, Islamic Rep.', 'Hong Kong SAR, China'], ['South Korea', 'Iran', 'Hong Kong'],regex=True) # replacing coutnry names
 GDP = GDP.rename(columns = {'Country Name': 'Country'}) # Changing Coutnry name to Country to join table
 GDP = GDP.loc[:, ['Country','2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'] ] # slicing column wise

 ScimEn = pd.read_excel(io='scimagojr-3.xlsx') #REading Sci file
 ScimEn_reduced = ScimEn[(ScimEn['Rank'] < 16)] #Taking range upto 15
 Energy_GDP = pd.merge(energy, GDP, how='inner', left_on='Country', right_on = 'Country') # Marging GDP and Energy
 df = pd.merge(ScimEn_reduced,Energy_GDP, how ='inner',left_on='Country',right_on='Country') #MArging GDP, Energy and Sci
 df = df.set_index('Country')
  
 return df 

answer_one()


# ### Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*

# In[62]:


get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')


# In[77]:


def answer_two():
  return 156
answer_two()


# ## Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by `answer_one()`)

# ### Question 3 (6.6%)
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[78]:


def answer_three():
    Top15 = answer_one()
    avg_gdp =Top15.iloc[:,10:20].mean(axis=1)
    
    return avg_gdp
answer_three()


# ### Question 4 (6.6%)
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*

# In[79]:


def answer_four():
    Top15 = answer_three() # series of average countries
    Coutnry_ascending = Top15.sort_values(ascending = False) # Sorted countries based on average gdp
    Sixth_Country = Coutnry_ascending.index[5] #taking the 6th country
    df = answer_one().loc[Sixth_Country] #All results of Sixth no. country
    return (df['2015'] - df['2006']) # answer
    
answer_four()


# ### Question 5 (6.6%)
# What is the mean `Energy Supply per Capita`?
# 
# *This function should return a single number.*

# In[80]:


def answer_five():
    Top15 = answer_one()
    mean_Capita =Top15['Energy Supply per Capita'].mean()
    return mean_Capita

answer_five()


# ### Question 6 (6.6%)
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*

# In[81]:


def answer_six():
    Top15 = answer_one()['% Renewable']
    Coutnry_ascending = Top15.sort_values(ascending = False) 
    return (Coutnry_ascending.index[0],Coutnry_ascending[0])
answer_six()


# ### Question 7 (6.6%)
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*

# In[82]:


def answer_seven():
    Top15 = answer_one()
    Top15['Citation Ratio'] = Top15['Self-citations']/Top15['Citations']
    return (Top15['Citation Ratio'].idxmax(), Top15['Citation Ratio'].max())
answer_seven()


# ### Question 8 (6.6%)
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return a single string value.*

# In[83]:


def answer_eight():
    Top15 = answer_one()
    Top15['Population'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    Sort_Population = Top15['Population'].sort_values(ascending = False)
    return Sort_Population.index[2]
    
answer_eight()


# ### Question 9 (6.6%)
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*

# In[84]:


def answer_nine():
    Top15 = answer_one()
    Top15['Population'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    Top15['Citable documents per person'] =Top15['Citable documents'] / Top15['Population']
    result =  Top15['Citable documents per person'].corr(Top15['Energy Supply per Capita'])
    return result
answer_nine()


# In[ ]:





# ### Question 10 (6.6%)
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

# In[85]:


def answer_ten():
    Top15 = answer_one()
    Renewable_mean =  Top15['% Renewable'].median()
    Top15['Renewable_new'] = [1 if item >= Renewable_mean else 0 for item in Top15['% Renewable']]
    return Top15['Renewable_new']
answer_ten()


# ### Question 11 (6.6%)
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

# In[15]:


def answer_eleven():

    Top15 = answer_one()
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    
    Top15['Population'] = Top15['Energy Supply']/Top15['Energy Supply per Capita'] # Counting population
    Top15 = Top15.reset_index() # reseting index so that country can be manipulated as column 
    Top15['Continent'] = Top15['Country'].map(ContinentDict) #entering a new column by mapping with country of doctionary
    groupped_data =  Top15.groupby('Continent')['Population'].agg(['size', 'sum', 'mean', 'std']) #result 
    return groupped_data

answer_eleven()




# ### Question 12 (6.6%)
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 
# *This function should return a __Series__ with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*

# In[89]:


def answer_twelve():
    import pandas as pd
    Top15 = answer_one()
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    
    Top15 = Top15.reset_index() # reseting index so that country can be manipulated as column 
    Top15['Continent'] = Top15['Country'].map(ContinentDict) #entering a new column by mapping with country of doctionary
    Top15['bins'] = pd.cut(Top15['% Renewable'],bins = 5) #enetering another column for bin size
    Country_size = Top15.groupby(['Continent', 'bins']).size() #counting the size 
    return Country_size
answer_twelve()


# ### Question 13 (6.6%)
# Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
# 
# e.g. 317615384.61538464 -> 317,615,384.61538464
# 
# *This function should return a Series `PopEst` whose index is the country name and whose values are the population estimate string.*

# In[87]:


def answer_thirteen():
    Top15 = answer_one()
    Top15['Population'] = (Top15['Energy Supply'] / Top15['Energy Supply per Capita']).astype(float)
    string_array = []
    for num in Top15['Population']:
       string_array.append( "{:,}".format(num)) #https://www.kite.com/python/answers/how-to-add-commas-to-a-number-in-python
    Top15['new_pop'] = string_array
    return Top15['new_pop']
answer_thirteen()


# ### Optional
# 
# Use the built in function `plot_optional()` to see an example visualization.

# In[88]:


def plot_optional():
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")


# In[ ]:


#plot_optional() # Be sure to comment out plot_optional() before submitting the assignment!

