#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
from bs4 import BeautifulSoup


# In[4]:


URL = "https://www.scrapethissite.com/pages/simple/"
page = requests.get(URL)
print("\n**Page**")
print(page.text)
print("/n**END**")


# In[5]:


soup = BeautifulSoup(page.content,'html.parser')
print("/n** RESULTS **")
print(soup)
print("/n** END**")


# In[6]:


results = soup.find(id='page')
#print(results)
print(results.prettify())


# In[7]:


print("\n***Countries Information***")
country_elements = results.find_all('div', class_ = 'col-md-4 country')
for country_element in country_elements:
    country_name = country_element.find('h3',class_='country-name')
    country_capital = country_element.find('span', class_='country-capital')
    country_population = country_element.find('span', class_='country-population')
    country_area = country_element.find('span', class_= 'country-area')
    #print(country_name)
    #print(country_capital)
    #print(country_population)
    #print(country_area)
    print(country_name.text.strip())
    print(country_capital.text.strip())
    print(country_population.text.strip())
    print(country_area.text.strip())


# In[14]:


print ("\n***Countries with the word United in them.***")
united_countries = [
    h3 for h3 in results.find_all('h3')
    if 'united' in h3.get_text().lower()
]

print("Number of countries: ", len(united_countries))

united_countries_elements = [
    h3_element.parent for h3_element in united_countries
]
for country_element in united_countries_elements:
    country_name = country_element.find('h3',class_='country-name')
    country_capital = country_element.find('span', class_='country-capital')
    country_population = country_element.find('span', class_='country-population')
    country_area = country_element.find('span', class_= 'country-area')
    print('')
    print(f"Name of country: {country_name.text.strip()}")
    print(f"Capital of country: {country_capital.text.strip()}")
    print(f"Population: {country_population.text.strip()}")
    print(f"Area: {country_area.text.strip()}")
    print()
print("***END***")


# In[ ]:




