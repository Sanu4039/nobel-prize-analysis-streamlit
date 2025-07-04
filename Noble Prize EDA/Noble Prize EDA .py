#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Imports & Configuration
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

pd.options.display.float_format = '{:,.2f}'.format
get_ipython().run_line_magic('matplotlib', 'inline')


# In[26]:


# Data Exploration & Cleaning

# **Challenge**: Preliminary data exploration. 
# * What is the shape of `df_data`? How many rows and columns?
# * What are the column names?
# * In which year was the Nobel prize first awarded?
# * Which year is the latest year included in the dataset?


# In[22]:


# Load Data
df_data = pd.read_csv('nobel_prize_data.csv')
df_data.shape


# In[24]:


df_data.head()


# In[28]:


df_data.tail()


# In[ ]:


# **Challange**: 
# * Are there any duplicate values in the dataset?
# * Are there NaN values in the dataset?
# * Which columns tend to have NaN values?
# * How many NaN values are there per column? 
# * Why do these columns have NaN values?  


# In[4]:


# Basic Checks
print(f'Any duplicates? {df_data.duplicated().values.any()}')
print(f'Any NaN values among the data? {df_data.isna().values.any()}')
df_data.isna().sum()


# In[29]:


#Why are there NaN values for birth dates? 


# In[31]:


# Nan values for birth dates are all organisations
col_subset = ['year','category', 'laureate_type', 'birth_date','full_name', 'organization_name']
df_data.loc[df_data.birth_date.isna()][col_subset]


# In[ ]:


# NaN values for organisation_name

col_subset = ['year','category', 'laureate_type','full_name', 'organization_name']
df_data.loc[df_data.organization_name.isna()][col_subset]


# #**Some prizes are given to Organisations rather than individuals!**

# ### Type Conversions
# 
# **Challenge**: 
# * Convert the `birth_date` column to Pandas `Datetime` objects
# * Add a Column called `share_pct` which has the laureates' share as a percentage in the form of a floating-point number.

# #### Convert Year and Birth Date to Datetime

# In[33]:


df_data.birth_date = pd.to_datetime(df_data.birth_date)


# #### Add a Column with the Prize Share as a Percentage

# In[35]:


separated_values = df_data.prize_share.str.split('/', expand=True)
numerator = pd.to_numeric(separated_values[0])
denomenator = pd.to_numeric(separated_values[1])
df_data['share_pct'] = numerator / denomenator


# In[36]:


df_data.info()


# # Plotly Donut Chart: Percentage of Male vs. Female Laureates

# **Challenge**: Create a [donut chart using plotly](https://plotly.com/python/pie-charts/) which shows how many prizes went to men compared to how many prizes went to women. What percentage of all the prizes went to women?

# In[38]:


# Gender Distribution
biology = df_data.sex.value_counts()
fig = px.pie(labels=biology.index, 
             values=biology.values,
             title="Percentage of Male vs. Female Winners",
             names=biology.index,
             hole=0.4,)

fig.update_traces(textposition='inside', textfont_size=15, textinfo='percent')

fig.show()


# # Who were the first 3 Women to Win the Nobel Prize?
# 
# **Challenge**: 
# * What are the names of the first 3 female Nobel laureates? 
# * What did the win the prize for? 
# * What do you see in their `birth_country`? Were they part of an organisation?

# In[39]:


# First Female laureates
df_data[df_data.sex == 'Female'].sort_values('year').head(3)


# # Find the Repeat Winners
# 
# **Challenge**: Did some people get a Nobel Prize more than once? If so, who were they? 

# In[40]:


# Multiple prize winners
is_winner = df_data.duplicated(subset=['full_name'], keep=False)
multiple_winners = df_data[is_winner]
print(f'There are {multiple_winners.full_name.nunique()} winners who were awarded the prize more than once.')


# In[41]:


#Alternatives
multiple_winners = df_data.groupby(by='full_name').filter(lambda x: x['year'].count() >= 2)


# In[42]:


col_subset = ['year', 'category', 'laureate_type', 'full_name']
multiple_winners[col_subset]


# # Number of Prizes per Category
# 
# **Challenge**: 
# * In how many categories are prizes awarded? 
# * Create a plotly bar chart with the number of prizes awarded by category. 
# * Use the color scale called `Aggrnyl` to colour the chart, but don't show a color axis.
# * Which category has the most number of prizes awarded? 
# * Which category has the fewest number of prizes awarded? 

# In[43]:


df_data.category.nunique()


# In[44]:


# Prizes per category
prizes_per_category = df_data.category.value_counts()

v_bar = px.bar(x=prizes_per_category.index,
               y=prizes_per_category.values,
               color=prizes_per_category.values,
               color_continuous_scale='Aggrnyl',
               title='Number of Prizes Awarded per Category')
v_bar.update_layout(xaxis_title='Nobel Prize Category', 
                    yaxis_title='Number of Prizes',
                    coloraxis_showscale=False)
v_bar.show()


# **Challenge**: 
# * When was the first prize in the field of Economics awarded?
# * Who did the prize go to?

# In[45]:


df_data[df_data.category == 'Economics'].sort_values('year')[:3]


# # Male and Female Winners by Category
# 
# **Challenge**: Create a [plotly bar chart](https://plotly.com/python/bar-charts/) that shows the split between men and women by category. 
# * Hover over the bar chart. How many prizes went to women in Literature compared to Physics?
# 
# 

# In[46]:


# Gender split by category
cat_men_women = df_data.groupby(['category', 'sex'], as_index=False).agg({'prize': pd.Series.count})
cat_men_women.sort_values('prize', ascending=False, inplace=True)

cat_men_women


# In[47]:


v_bar_split = px.bar(x=cat_men_women.category,
                     y=cat_men_women.prize,
                     color=cat_men_women.sex,
                     title='Number of Prizes Awarded per Category split by Men and Women')
v_bar_split.update_layout(xaxis_title='Nobel Prize Category', yaxis_title='Number of Prizes')
v_bar_split.show()


# # Number of Prizes Awarded Over Time
# 
# **Challenge**: Are more prizes awarded recently than when the prize was first created? Show the trend in awards visually. 
# * Count the number of prizes awarded every year. 
# * Create a 5 year rolling average of the number of prizes ( see previous lessons analysing Google Trends).
# * Using Matplotlib superimpose the rolling average on a scatter plot.
# * Show a tick mark on the x-axis for every 5 years from 1900 to 2020. ( will need to use NumPy). 
# 
# 
# * Use the [named colours](https://matplotlib.org/3.1.0/gallery/color/named_colors.html) to draw the data points in `dogerblue` while the rolling average is coloured in `crimson`. 
# 
# 
# * Looking at the chart, did the first and second world wars have an impact on the number of prizes being given out? 
# * What could be the reason for the trend in the chart?
# 

# In[49]:


# Pizes over time with moving Average
prize_per_year = df_data.groupby(by='year').count().prize


# In[50]:


moving_average = prize_per_year.rolling(window=5).mean()


# In[52]:


plt.scatter(x=prize_per_year.index, 
           y=prize_per_year.values, 
           c='dodgerblue',
           alpha=0.7,
           s=100,)

plt.plot(prize_per_year.index, 
        moving_average.values, 
        c='crimson', 
        linewidth=3,)

plt.show()


# In[53]:


plt.figure(figsize=(16,8), dpi=200)
plt.title('Number of Nobel Prizes Awarded per Year', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(ticks=np.arange(1900, 2021, step=5), 
           fontsize=14, 
           rotation=45)

ax = plt.gca()
ax.set_xlim(1900, 2020)

ax.scatter(x=prize_per_year.index, 
           y=prize_per_year.values, 
           c='dodgerblue',
           alpha=0.7,
           s=100,)

ax.plot(prize_per_year.index, 
        moving_average.values, 
        c='crimson', 
        linewidth=3,)

plt.show()


# # Are More Prizes Shared Than Before?
# 
# **Challenge**: Investigate if more prizes are shared than before. 
# 
# * Calculate the average prize share of the winners on a year by year basis.
# * Calculate the 5 year rolling average of the percentage share.
# * Copy-paste the cell from the chart you created above.
# * Modify the code to add a secondary axis to your Matplotlib chart.
# * Plot the rolling average of the prize share on this chart. 
# * See if you can invert the secondary y-axis to make the relationship even more clear. 

# In[60]:


# Prize share and count on dual Y - axis 
yearly_avg_share = df_data.groupby(by='year').agg({'share_pct': pd.Series.mean})
share_moving_average = yearly_avg_share.rolling(window=5).mean()


# In[61]:


plt.figure(figsize=(16, 8), dpi=200)
plt.title('Number of Nobel Prizes and Share Percentage per Year', fontsize=18)
plt.xticks(ticks=np.arange(1900, 2021, 5), fontsize=14, rotation=45)
plt.yticks(fontsize=14)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.scatter(prize_per_year.index, prize_per_year.values, c='dodgerblue', alpha=0.7, s=100)
ax1.plot(prize_per_year.index, moving_average.values, c='crimson', linewidth=3)
ax2.plot(prize_per_year.index, share_moving_average.values, c='grey', linewidth=3)
plt.show()


# In[62]:


plt.figure(figsize=(16,8), dpi=200)
plt.title('Number of Nobel Prizes Awarded per Year', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(ticks=np.arange(1900, 2021, step=5), 
           fontsize=14, 
           rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()
ax1.set_xlim(1900, 2020)

# Can invert axis
ax2.invert_yaxis()

ax1.scatter(x=prize_per_year.index, 
           y=prize_per_year.values, 
           c='dodgerblue',
           alpha=0.7,
           s=100,)

ax1.plot(prize_per_year.index, 
        moving_average.values, 
        c='crimson', 
        linewidth=3,)

ax2.plot(prize_per_year.index, 
        share_moving_average.values, 
        c='grey', 
        linewidth=3,)

plt.show()


# # The Countries with the Most Nobel Prizes
# **Challenge**: 
# * Create a Pandas DataFrame called `top20_countries` that has the two columns. The `prize` column should contain the total number of prizes won. 
# 
# 
# * Is it best to use `birth_country`, `birth_country_current` or `organization_country`? 
# * What are some potential problems when using `birth_country` or any of the others? Which column is the least problematic? 
# * Then use plotly to create a horizontal bar chart showing the number of prizes won by each country. Here's what you're after:
# 
# 
# * What is the ranking for the top 20 countries in terms of the number of prizes?

# In[63]:


top_countries = df_data.groupby(['birth_country_current'], 
                                  as_index=False).agg({'prize': pd.Series.count})

top_countries.sort_values(by='prize', inplace=True)
top20_countries = top_countries[-20:]
top20_countries


# In[64]:


h_bar = px.bar(x=top20_countries.prize,
               y=top20_countries.birth_country_current,
               orientation='h',
               color=top20_countries.prize,
               color_continuous_scale='Viridis',
               title='Top 20 Countries by Number of Prizes')
h_bar.update_layout(xaxis_title='Number of Prizes', yaxis_title='Country', coloraxis_showscale=False)
h_bar.show()


# # Use a Choropleth Map to Show the Number of Prizes Won by Country
# 
# * Create this choropleth map using [the plotly documentation](https://plotly.com/python/choropleth-maps/):
# 
# 
# * Experiment with [plotly's available colours](https://plotly.com/python/builtin-colorscales/). I quite like the sequential colour `matter` on this map. 
# 
# You'll need to use a 3 letter country code for each country. 
# 

# In[65]:


df_countries = df_data.groupby(['birth_country_current', 'ISO'], 
                               as_index=False).agg({'prize': pd.Series.count})
df_countries.sort_values('prize', ascending=False)


# In[66]:


world_map = px.choropleth(df_countries,
                          locations='ISO',
                          color='prize', 
                          hover_name='birth_country_current', 
                          color_continuous_scale=px.colors.sequential.matter)

world_map.update_layout(coloraxis_showscale=True,)

world_map.show()


# # In Which Categories are the Different Countries Winning Prizes? 
# 
# **Challenge**: See if you can divide up the plotly bar chart you created above to show the which categories made up the total number of prizes. Here's what you're aiming for:
# 
# 
# * In which category are Germany and Japan the weakest compared to the United States?
# * In which category does Germany have more prizes than the UK?
# * In which categories does France have more prizes than Germany?
# * Which category makes up most of Australia's nobel prizes?
# * Which category makes up half of the prizes in the Netherlands?
# * Does the United States have more prizes in Economics than all of France? What about in Physics or Medicine?
# 
# 
# The hard part is preparing the data for this chart! 
# 
# 
# Take a two-step approach. The first step is grouping the data by country and category. Then you can create a DataFrame that looks something like this:
# 
# 

# In[67]:


cat_country = df_data.groupby(['birth_country_current', 'category'], 
                               as_index=False).agg({'prize': pd.Series.count})
cat_country.sort_values(by='prize', ascending=False, inplace=True)
cat_country


# In[68]:


merged_df = pd.merge(cat_country, top20_countries, on='birth_country_current')
# change column names
merged_df.columns = ['birth_country_current', 'category', 'cat_prize', 'total_prize'] 
merged_df.sort_values(by='total_prize', inplace=True)
merged_df


# In[69]:


cat_cntry_bar = px.bar(x=merged_df.cat_prize,
                       y=merged_df.birth_country_current,
                       color=merged_df.category,
                       orientation='h',
                       title='Top 20 Countries by Number of Prizes and Category')

cat_cntry_bar.update_layout(xaxis_title='Number of Prizes', 
                            yaxis_title='Country')
cat_cntry_bar.show()


# ### Number of Prizes Won by Each Country Over Time
# 
# * When did the United States eclipse every other country in terms of the number of prizes won? 
# * Which country or countries were leading previously?
# * Calculate the cumulative number of prizes won by each country in every year. Again, use the `birth_country_current` of the winner to calculate this. 
# * Create a [plotly line chart](https://plotly.com/python/line-charts/) where each country is a coloured line. 

# In[70]:


prize_by_year = df_data.groupby(by=['birth_country_current', 'year'], as_index=False).count()
prize_by_year = prize_by_year.sort_values('year')[['year', 'birth_country_current', 'prize']]
prize_by_year


# In[71]:


cumulative_prizes = prize_by_year.groupby(by=['birth_country_current',
                                              'year']).sum().groupby(level=[0]).cumsum()
cumulative_prizes.reset_index(inplace=True)


# In[72]:


l_chart = px.line(cumulative_prizes,
                  x='year', 
                  y='prize',
                  color='birth_country_current',
                  hover_name='birth_country_current')

l_chart.update_layout(xaxis_title='Year',
                      yaxis_title='Number of Prizes')

l_chart.show()


# # What are the Top Research Organisations?
# 
# **Challenge**: Create a bar chart showing the organisations affiliated with the Nobel laureates. It should looks something like this:
# 
# * Which organisations make up the top 20?
# * How many Nobel prize winners are affiliated with the University of Chicago and Harvard University?

# In[73]:


top20_orgs = df_data.organization_name.value_counts()[:20]
top20_orgs.sort_values(ascending=True, inplace=True)


# In[74]:


org_bar = px.bar(x = top20_orgs.values,
                 y = top20_orgs.index,
                 orientation='h',
                 color=top20_orgs.values,
                 color_continuous_scale=px.colors.sequential.haline,
                 title='Top 20 Research Institutions by Number of Prizes')

org_bar.update_layout(xaxis_title='Number of Prizes', 
                      yaxis_title='Institution',
                      coloraxis_showscale=False)
org_bar.show()


# # Which Cities Make the Most Discoveries? 
# 
# Where do major discoveries take place?  
# 
# **Challenge**: 
# * Create another plotly bar chart graphing the top 20 organisation cities of the research institutions associated with a Nobel laureate. 
# * Where is the number one hotspot for discoveries in the world?
# * Which city in Europe has had the most discoveries?

# In[75]:


top20_org_cities = df_data.organization_city.value_counts()[:20]
top20_org_cities.sort_values(ascending=True, inplace=True)
city_bar2 = px.bar(x = top20_org_cities.values,
                  y = top20_org_cities.index,
                  orientation='h',
                  color=top20_org_cities.values,
                  color_continuous_scale=px.colors.sequential.Plasma,
                  title='Which Cities Do the Most Research?')

city_bar2.update_layout(xaxis_title='Number of Prizes', 
                       yaxis_title='City',
                       coloraxis_showscale=False)
city_bar2.show()


# # Where are Nobel Laureates Born? Chart the Laureate Birth Cities 
# 
# **Challenge**: 
# * Create a plotly bar chart graphing the top 20 birth cities of Nobel laureates. 
# * Use a named colour scale called `Plasma` for the chart.
# * What percentage of the United States prizes came from Nobel laureates born in New York? 
# * How many Nobel laureates were born in London, Paris and Vienna? 
# * Out of the top 5 cities, how many are in the United States?
# 

# In[76]:


top20_cities = df_data.birth_city.value_counts()[:20]
top20_cities.sort_values(ascending=True, inplace=True)
city_bar = px.bar(x=top20_cities.values,
                  y=top20_cities.index,
                  orientation='h',
                  color=top20_cities.values,
                  color_continuous_scale=px.colors.sequential.Plasma,
                  title='Where were the Nobel Laureates Born?')

city_bar.update_layout(xaxis_title='Number of Prizes', 
                       yaxis_title='City of Birth',
                       coloraxis_showscale=False)
city_bar.show()


# # Plotly Sunburst Chart: Combine Country, City, and Organisation
# 
# **Challenge**: 
# 
# * Create a DataFrame that groups the number of prizes by organisation. 
# * Then use the [plotly documentation to create a sunburst chart](https://plotly.com/python/sunburst-charts/)
# * Click around in your chart, what do you notice about Germany and France
# 

# In[77]:


country_city_org = df_data.groupby(by=['organization_country', 
                                       'organization_city', 
                                       'organization_name'], as_index=False).agg({'prize': pd.Series.count})

country_city_org = country_city_org.sort_values('prize', ascending=False)
country_city_org


# In[78]:


burst = px.sunburst(country_city_org, 
                    path=['organization_country', 'organization_city', 'organization_name'], 
                    values='prize',
                    title='Where do Discoveries Take Place?',
                   )

burst.update_layout(xaxis_title='Number of Prizes', 
                    yaxis_title='City',
                    coloraxis_showscale=False)

burst.show()


# # Patterns in the Laureate Age at the Time of the Award
# 
# How Old Are the Laureates When the Win the Prize?
# 
# **Challenge**: Calculate the age of the laureate in the year of the ceremony and add this as a column called `winning_age` to the `df_data` DataFrame. 
# you can use [this](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.dt.html) 
# 
# 

# In[79]:


# Use Datetime object
birth_years = df_data.birth_date.dt.year
birth_years


# In[80]:


df_data['winning_age'] = df_data.year - birth_years
df_data.winning_age


# ### Who were the oldest and youngest winners?
# 
# **Challenge**: 
# * What are the names of the youngest and oldest Nobel laureate? 
# * What did they win the prize for?
# * What is the average age of a winner?
# * 75% of laureates are younger than what age when they receive the prize?
# * Use Seaborn to [create histogram](https://seaborn.pydata.org/generated/seaborn.histplot.html) to visualise the distribution of laureate age at the time of winning. Experiment with the number of `bins` to see how the visualisation changes.

# In[81]:


display(df_data.nlargest(n=1, columns='winning_age'))
display(df_data.nsmallest(n=1, columns='winning_age'))


# ### Descriptive Statistics for the Laureate Age at Time of Award
# 
# * Calculate the descriptive statistics for the age at the time of the award. 
# * Then visualise the distribution in the form of a histogram using [Seaborn's .histplot() function](https://seaborn.pydata.org/generated/seaborn.histplot.html).
# * Experiment with the `bin` size. Try 10, 20, 30, and 50.  

# In[82]:


df_data.winning_age.describe()


# In[83]:


plt.figure(figsize=(8, 4), dpi=200)
sns.histplot(data=df_data,
             x=df_data.winning_age,
             bins=30)
plt.xlabel('Age')
plt.title('Distribution of Age on Receipt of Prize')
plt.show()


# ### Age at Time of Award throughout History
# 
# Are Nobel laureates being nominated later in life than before? Have the ages of laureates at the time of the award increased or decreased over time?
# 
# **Challenge**
# 
# * Use Seaborn to [create a .regplot](https://seaborn.pydata.org/generated/seaborn.regplot.html?highlight=regplot#seaborn.regplot) with a trendline.
# * Set the `lowess` parameter to `True` to show a moving average of the linear fit.
# * According to the best fit line, how old were Nobel laureates in the years 1900-1940 when they were awarded the prize?
# * According to the best fit line, what age would it predict for a Nobel laureate in 2020?
# 

# In[85]:


plt.figure(figsize=(8,4), dpi=200)
with sns.axes_style("whitegrid"):
    sns.regplot(data=df_data,
                x='year',
                y='winning_age',
                lowess=True, 
                scatter_kws = {'alpha': 0.4},
                line_kws={'color': 'black'})

plt.show()


# ### Winning Age Across the Nobel Prize Categories
# 
# How does the age of laureates vary by category? 
# 
# * Use Seaborn's [`.boxplot()`](https://seaborn.pydata.org/generated/seaborn.boxplot.html?highlight=boxplot#seaborn.boxplot) to show how the mean, quartiles, max, and minimum values vary across categories. Which category has the longest "whiskers"? 
# * In which prize category are the average winners the oldest?
# * In which prize category are the average winners the youngest?

# In[86]:


plt.figure(figsize=(8,4), dpi=200)
with sns.axes_style("whitegrid"):
    sns.boxplot(data=df_data,
                x='category',
                y='winning_age')

plt.show()


# In[87]:


# Box plot using plotly instead
box = px.box(df_data, 
             x='category', 
             y='winning_age',
             title='How old are the Winners?')

box.update_layout(xaxis_title='Category',
                  yaxis_title='Age at time of Award',
                  xaxis={'categoryorder':'mean ascending'},)

box.show()


# **Challenge**
# * Now use Seaborn's [`.lmplot()`](https://seaborn.pydata.org/generated/seaborn.lmplot.html?highlight=lmplot#seaborn.lmplot) and the `row` parameter to create 6 separate charts for each prize category. Again set `lowess` to `True`.
# * What are the winning age trends in each category? 
# * Which category has the age trending up and which category has the age trending down? 
# * Is this `.lmplot()` telling a different story from the `.boxplot()`?
# * Create another chart with Seaborn. This time use `.lmplot()` to put all 6 categories on the same chart using the `hue` parameter. 
# 

# In[89]:


with sns.axes_style('whitegrid'):
    sns.lmplot(data=df_data,
               x='year', 
               y='winning_age',
               row = 'category',
               lowess=True, 
               aspect=2,
               scatter_kws = {'alpha': 0.6},
               line_kws = {'color': 'black'},)

plt.show()


# In[90]:


with sns.axes_style("whitegrid"):
    sns.lmplot(data=df_data,
               x='year',
               y='winning_age',
               hue='category',
               lowess=True, 
               aspect=2,
               scatter_kws={'alpha': 0.5},
               line_kws={'linewidth': 5})

plt.show()


# In[ ]:





# In[ ]:




