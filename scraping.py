# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt


def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemisphere_images": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p




# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[10]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[11]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[12]:


# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[13]:


# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### 3. Mars Facts

# In[14]:


df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# ### Mars Weather 

# In[15]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[16]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[17]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# In[18]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[19]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
html_hemis = browser.html 

# parse HTML object with beautiful soup
hemis_soup = soup(html_hemis, 'html.parser')
#slide_elem = hemis_soup.select_one('ul.item_list li.slide')


# In[20]:


# find all items that have Mars hemispheres info 
hemis_items = hemis_soup.find_all('div', class_='item')


# In[21]:


# Find the relative image url
hemis_url_rel = hemis_soup.find('a', class_='itemLink product-item')['href']
hemis_url_rel


# In[22]:


# Use the base URL to create an absolute URL
hemis_url = 'https://astrogeology.usgs.gov'
hemis_url


# In[23]:


# 3. Write code to retrieve the image urls and titles for each hemisphere.
for h in hemis_items: 
    
    hemi_title = h.find('h3').text
    
  
    # visit link  
    # Find the relative image url
    hemis_url_rel = hemis_soup.find('a', class_='itemLink product-item')['href']

    browser.visit(hemis_url + hemis_url_rel)
    
    # parse HTML with Beautiful Soup 
    html = browser.html 
    
    hemi_soup = soup(html, 'html.parser')
    
    # Find the relative image url
    hemis_url_rel = hemis_soup.find('a', class_='itemLink product-item')['href']
    
    image_link = hemi_soup.find('div', class_='downloads')
    image_url = hemi_soup.find('li').a['href']
                    
    # create a dictionary and store the url & title info
    hemispheres = {} 
    hemispheres['title'] = hemi_title 
    hemispheres['img_url'] = image_url 
    
    # add title and url to hemispheres dictionary 
    hemisphere_image_urls.append({'title': hemi_title, 'img_url': img_url})
    


# In[24]:


print(hemisphere_image_urls) 


# In[25]:


browser.quit() 


# In[ ]:




