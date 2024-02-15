'''
File: image_crawler.py
Work: Crawls the images fro google image search
'''

# Load the neccessary modules/frameworks
import os
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def create_folder(folder_name, count=0):
    '''
    work: creates the folder at given directory with series  
    '''
    # check, if true it's update the folder name with new name according to count
    if count > 0:
        new_folder_name = f"{folder_name}({count})"
    else:
        new_folder_name = folder_name

    # check, if true create the folder
    if not os.path.exists(new_folder_name):
        os.makedirs(new_folder_name)
        return new_folder_name
    # recall the self with updated count value
    else:
        return create_folder(folder_name, count+1)


# Crawler class
class Crawler:
    def __init__(self):
        # header information, so that there are no conflicts
        self.header = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.152 Safari/537.36"
        
        # add the header section to Chrome
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(self.header)
        
        # root url where scraping starts
        self.root_url = 'https://www.google.com'

        # create root folder where all scraped images store
        self.root_folder = 'raw_images'
        os.makedirs(self.root_folder, exist_ok=True)

    
    def scrape_img(self, query):
        # initilize the driver
        driver = webdriver.Chrome(options=self.options)
        
        # maximize the browser window, so that pages can load full
        driver.maximize_window()

        # open the root browser window 
        driver.get(url=self.root_url)

        # find the search bar
        search_bar = driver.find_element(By.ID, "APjFqb")

        # pass the query to search bar
        search_bar.send_keys(query)

        # hit the enter button
        search_bar.send_keys(Keys.ENTER)

        try:
            # click on images tab
            driver.find_element(By.XPATH, "//a[@class='LatpMc nPDzT T3FoJb'][1]").click()

            # scroll the page so that browser loads the more images
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                driver.implicitly_wait(20)

            # scrape all img tags from page
            images = driver.find_elements(By.XPATH, "//img[@class='rg_i Q4LuWd']")

             # make directory for storing images
            img_folder = os.path.join(self.root_folder, query)
            img_folder = create_folder(img_folder)

            # store the images into folder
            counter = 0
            # download the images one by one
            for image in images:
                # extract image link
                img_link = image.get_attribute('src')
                if img_link != None:
                    img_name = f"{counter}.jpg"
                    # download the img
                    urllib.request.urlretrieve(str(img_link), os.path.join(img_folder, img_name))
                counter += 1
        except Exception as e:
            print(e)
        finally:
            # close the driver/browser
            driver.close()
        
    
crawler = Crawler()
crawler.scrape_img(query="Dancing man")