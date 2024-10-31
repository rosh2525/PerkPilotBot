import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sqlite3

conn = sqlite3.connect('student_discounts.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS discounts (
    id INTEGER PRIMARY KEY,
    source TEXT,
    company TEXT,
    link TEXT,
    discount TEXT,
    expiry TEXT
)
''')

def scrape_myunidays():
    url = "https://www.myunidays.com/IN/en-IN/list/all/AtoZ"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article', class_='tile')

        for article in articles:
            discount_tag = article.find('p', class_='tile__discount')
            discount = discount_tag.text.strip() if discount_tag else 'No discount information available'
            company_name = article.get('data-customer-name')
            link = article.find('a')['href'] if article.find('a') else 'No link found'
            full_link = f"https://www.myunidays.com{link}" if link != 'No link found' else 'No link available'

            if company_name:
                cursor.execute('''
                INSERT INTO discounts (source, company, link, discount, expiry) 
                VALUES (?, ?, ?, ?, ?)''',
                ('MyUNIDAYS', company_name, full_link, discount, 'N/A'))

def scrape_student_beans():
    driver = webdriver.Chrome()
    driver.get("https://www.studentbeans.com/student-discount/us/all")
    time.sleep(5)

    scroll_pause = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    discount_sections = driver.find_elements(By.TAG_NAME, "article")

    for section in discount_sections:
        try:
            brand = section.find_element(By.XPATH, ".//p[@data-testid='offer-tile-brand']").text.strip()
            discount_title = section.find_element(By.XPATH, ".//h4[@data-testid='offer-tile-title']").text.strip()
            try:
                expiry = section.find_element(By.XPATH, ".//span[@data-testid='offerBoostExpiry']").text.strip()
            except:
                expiry = "No expiration date available"
            link = section.find_element(By.XPATH, ".//a").get_attribute("href")

            cursor.execute('''
            INSERT INTO discounts (source, company, link, discount, expiry) 
            VALUES (?, ?, ?, ?, ?)''',
            ('Student Beans', brand, link, discount_title, expiry))
        except Exception as e:
            print(f"Error extracting information: {e}")

    driver.quit()

scrape_myunidays()
scrape_student_beans()

conn.commit()
conn.close()

print("Data has been successfully scraped and saved to the database.")
