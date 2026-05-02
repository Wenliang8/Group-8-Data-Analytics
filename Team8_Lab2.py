#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


# 1. Load dataset
df = pd.read_csv("WorldEnergy.csv")


# In[3]:


df.head()          # preview first rows


# In[4]:


df.info()          # data types and non-null counts


# In[5]:


df.columns         # list all columns


# In[6]:


df.describe()


# In[7]:


df.isnull().sum()  # count missing values


# In[8]:


df['country'].unique()


# In[9]:


# 1. Remove non-country entries (regions, aggregates, income groups)
exclude_keywords = [
    "World", "income", "OECD", "OPEC", "EIA", "EI",
    "Asia", "Europe", "Africa", "Oceania", "America",
    "Union", "Pacific", "USSR", "Ember"
]

df_cleaned = df[~df["country"].str.contains("|".join(exclude_keywords),
                                            case=False, na=False)]

# 2. Remove rows where country is missing
df_cleaned = df_cleaned.dropna(subset=['country'])

# 3. Remove rows where year is missing
df_cleaned = df_cleaned.dropna(subset=['year'])

# 4. Convert year to integer (if needed)
df_cleaned['year'] = df_cleaned['year'].astype(int)

# 5. Optional: filter unrealistic years (keep 1900–2024)
df_cleaned = df_cleaned[(df_cleaned['year'] >= 1900) & (df_cleaned['year'] <= 2024)]

# 6. Reset index
df_cleaned = df_cleaned.reset_index(drop=True)

# 7. Show cleaned dataset structure
df_cleaned.info()

df_cleaned.to_csv("cleaned_energy_data.csv", index=False)


# In[10]:


numeric_df = df_cleaned.select_dtypes(include=['number'])

plt.figure(figsize=(12,8))
sns.heatmap(numeric_df.corr(), cmap='coolwarm')
plt.title("Correlation Heatmap of Numeric Features", fontsize=16)
plt.show()


# In[11]:


cols = [
    'population',
    'primary_energy_consumption',
    'oil_consumption',
    'fossil_share_energy',
    'renewables_share_energy'
]

plt.figure(figsize=(8,6))
sns.heatmap(df_cleaned[cols].corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Focused Correlation Heatmap (Key Variables)")
plt.show()


# In[12]:


plt.figure(figsize=(10,6))
sns.scatterplot(
    data=df_cleaned,
    x='oil_consumption',
    y='primary_energy_consumption',
    alpha=0.6
)

plt.xscale('log')
plt.yscale('log')

plt.title("Oil Consumption vs Primary Energy Consumption (Log-Scale)")
plt.xlabel("Oil Consumption (log scale)")
plt.ylabel("Primary Energy Consumption (log scale)")
plt.show()


# In[13]:


top20_oil = df_cleaned.groupby('country')['oil_consumption'].sum().nlargest(20)

plt.figure(figsize=(10,8))
top20_oil.sort_values().plot(kind='barh', color='steelblue')

plt.title("Top 20 Countries by Oil Consumption")
plt.xlabel("Oil Consumption")
plt.ylabel("Country")
plt.show()


# In[14]:


oil_trend = df_cleaned.groupby('year')['oil_consumption'].sum()

plt.figure(figsize=(10,6))
plt.plot(oil_trend.index, oil_trend.values, marker='o', color='darkred')

plt.title("Global Oil Consumption Over Time")
plt.xlabel("Year")
plt.ylabel("Total Oil Consumption")
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()


# In[15]:


# Filter data from 1980 onwards
df_recent = df_cleaned[df_cleaned['year'] >= 1980]

# Identify top 5 oil-consuming countries
top5_countries = df_recent.groupby('country')['oil_consumption'].sum().nlargest(5).index

plt.figure(figsize=(12,7))

# Plot each country's trend
for country in top5_countries:
    country_data = df_recent[df_recent['country'] == country]
    yearly_oil = country_data.groupby('year')['oil_consumption'].sum()
    plt.plot(yearly_oil.index, yearly_oil.values, marker='o', label=country)

plt.title("Oil Consumption Over Time for Top 5 Countries (1980–2024)")
plt.xlabel("Year")
plt.ylabel("Oil Consumption")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()


# In[16]:


plt.figure(figsize=(10,6))
sns.scatterplot(
    data=df_cleaned,
    x='fossil_share_energy',
    y='renewables_share_energy',
    alpha=0.6
)

plt.title("Fossil Share vs Renewable Share of Energy")
plt.xlabel("Fossil Share of Energy (%)")
plt.ylabel("Renewable Share of Energy (%)")
plt.show()


# In[17]:


country = "United States"
subset = df_cleaned[df_cleaned['country'] == country]

plt.figure(figsize=(12,6))
plt.plot(subset['year'], subset['fossil_share_energy'], label='Fossil Share')
plt.plot(subset['year'], subset['renewables_share_energy'], label='Renewable Share')
plt.title(f"Fossil vs Renewable Energy Share in {country}")
plt.legend()
plt.show()

