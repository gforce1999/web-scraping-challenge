# Start by converting your Jupyter notebook into a Python script called scrape_mars.py
# with a function called scrape that will execute all of your scraping code from above
# and return one Python dictionary containing all of the scraped data.

# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# scrape() definition - returns single python dictionary of all scraped data
def scrape():

    # create dictionary to hold scraped data
    mars_dict = {}
    # setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    ##### NASA Mars News Scraping
    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # get title and news article
    news_title = soup.find('div',class_="content_title").get_text()
    news_p = soup.find('div',class_='article_teaser_body').get_text() 
    # store latest news title and paragraph text in mars_dict
    mars_dict['news_title'] = news_title
    mars_dict['news_p'] = news_p 
    
    ##### JPL Mars Space Images - Featured Image
    # URL of page to be scraped
    image_url = 'https://spaceimages-mars.com/' 
    browser.visit(image_url)
    # Create BeautifulSoup object; parse with'html.parser'
    html1 = browser.html
    soup1 = BeautifulSoup(html1, 'html.parser')
    # retrieve image url for the featured image
    images = soup1.find_all('div', class_='floating_text_area')
    # iterate through each
    for image in images:
        link = image.find('a')
        href = link['href']
    # save featured image link in a variable
    featured_image_url = 'https://spaceimages-mars.com/' + href    
    # store featured image link into mars_dict
    mars_dict['featured_image_url'] = featured_image_url

    ##### Mars Facts
    # url to scrape
    url ='https://galaxyfacts-mars.com/'
    # read_html to scrape tabular data
    tables = pd.read_html(url)
    # save dataframe
    mars_earth_df = tables[0]
    # adjust column headers
    new_header = mars_earth_df.iloc[0] #grab the first row for the header
    mars_earth_df = mars_earth_df[1:] #take the data less the header row
    mars_earth_df.columns = new_header #set the header row as the df header
    mars_earth_df.rename(columns=mars_earth_df.iloc[0])
    # set_index to 'mars-earth comparison column'
    mars_earth_df.set_index('Mars - Earth Comparison', inplace=True)
    mars_facts = mars_earth_df.to_html(justify='left')
    # store to mars dict
    mars_dict['table_data'] = mars_facts

    ##### Mars Hemispheres
    # URL of page to be scraped
    image_url = 'https://marshemispheres.com/' 
    browser.visit(image_url)
    # Iterate through all pages
    # HTML object
    html2 = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html2, 'html.parser')
    # Retrieve all elements that contain image link information
    hemispheres = soup.find_all('div', class_='description')
    # list of links for hemisphere pages
    hemispheres_list=[]  
    # Iterate through each book

    for hemisphere in hemispheres:
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        link = hemisphere.find('a')
        href = link['href']
        hemispheres_list.append('https://marshemispheres.com/' + href)

    # list of dictioinaries of hemisphere image urls 
    hemisphere_image_urls=[]
    # get image url and titles

    for hemisphere in hemispheres_list:
        # URL of page to be scraped
        browser.visit(hemisphere)
        #HTML object
        html3 = browser.html
        #Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html3, 'html.parser')
        # Retrieve all elements that contain image link information
        results = soup.find_all('div', class_='cover')      
        for result in results:
            title = result.find('h2',class_='title').get_text()
        # get the image url and title
        images = soup.find_all('div', class_ ='downloads')

        for image in images:
            ul = image.find('ul')
            li = ul.find('li')
            link = li.find('a')
            href1 = link['href']
            img_url = 'https://marshemispheres.com/' + href1        
            post = {
                'title': title,
                'img_url': img_url,
                }
            hemisphere_image_urls.append(post)
            print("hemisphere_image_urls")
            print(hemisphere_image_urls)
        # store hemisphere image links into mars_dict
    mars_dict['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_dict

        


    






