import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from multiprocessing import Process
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service as ChromeService
import csv
from datetime import datetime

base_url = "https://www.google.com/search?q=site%3A*business.site&oq=site%3A*business.site&gs_lcrp=EgZjaHJvbWUqBggAEEUYOzIGCAAQRRg7MgYIARBFGDrSAQc4ODJqMGo3qAIAsAIA&client=ubuntu-chr&sourceid=chrome&ie=UTF-8#ip=1"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--start-maximized')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.get(base_url)
time.sleep(150)
driver.implicitly_wait(10)
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')
time.sleep(2)
with open('output.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))

file_path = "output.html"
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Create a BeautifulSoup object

business_site_elements = soup.find_all('a', href=lambda href: href and 'business.site' in href)

    # Extract the URLs from the elements
business_site_urls = [element['href'] for element in business_site_elements if '/translate?' not in element['href']]


# Print the extracted URLs
with open("data.csv", 'w', encoding='utf-8') as csv_file:
    # Print the extracted URLs
    for url in business_site_urls:
        if "business.site" in url:
            print(url)
            
            # Write each URL on a new line in the CSV file
            csv_file.write(url + '\n')

    

