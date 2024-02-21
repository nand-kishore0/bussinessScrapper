from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import csv

csv_file = "data.csv"
output_csv_file = "updated_data.csv"

def perform_automation(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(1)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    address_element = soup.find('address', class_='qhkvMe')
    if address_element:
        address_lines = address_element.find_all('div')
        address = "\n".join([line.get_text(strip=True) for line in address_lines])
        print(f"Address: {address}")
    else:
        print("Address not found.")
        address = ""

    phone_numbers = []
    phone_link = soup.find('a', class_='PDvGL q8cvFf')
    if phone_link:
        phone_numbers.append(phone_link['href'].replace('tel:', ''))
        print(f"Phone Numbers: {phone_numbers}")

    phone_list_items = soup.find('ul', class_='R7Di0e')
    if phone_list_items:
        phone_numbers.extend([item.get_text(strip=True) for item in phone_list_items.find_all('li')])

    print(f"Updated Phone Numbers: {phone_numbers}")

    time.sleep(4)
    driver.quit()

    return address, phone_numbers


if __name__ == "__main__":
    with open(csv_file, 'r', encoding='utf-8') as file, open(output_csv_file, 'w', newline='', encoding='utf-8') as output_file:
        csv_reader = csv.reader(file)
        csv_writer = csv.writer(output_file)

        header = next(csv_reader)
        header.extend(["Address", "Phone Numbers"])
        csv_writer.writerow(header)

        for row in csv_reader:
            url = row[0]
            print(f"Processing URL: {url}")
            address, phone_numbers = perform_automation(url)
            
            row.extend([address, ", ".join(phone_numbers)])
            csv_writer.writerow(row)

            time.sleep(3)
