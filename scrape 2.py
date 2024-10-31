import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sqlite3

# Step 1: Create and connect to SQLite database
conn = sqlite3.connect('student_discounts.db')
cursor = conn.cursor()

# Create a table for storing discounts
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

# Function to scrape discounts from MyUNIDAYS
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
                ('MyUNIDAYS', company_name, full_link, discount, 'N/A'))  # No expiry info from this source

# Step 2: Scrape discounts from Student Beans
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
            link = section.find_element(By.XPATH, ".//a").get_attribute("href")  # Extract link

            cursor.execute('''
            INSERT INTO discounts (source, company, link, discount, expiry) 
            VALUES (?, ?, ?, ?, ?)''',
            ('Student Beans', brand, link, discount_title, expiry))  # No logo info from this source
        except Exception as e:
            print(f"Error extracting information: {e}")

    driver.quit()

# Run the scraping functions
scrape_myunidays()
scrape_student_beans()

# Commit changes and close the database connection
conn.commit()
conn.close()

print("Data has been successfully scraped and saved to the database.")
