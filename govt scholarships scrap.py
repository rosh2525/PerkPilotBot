import requests
from bs4 import BeautifulSoup
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('student_discounts.db')
cursor = conn.cursor()

# Create a table for government scholarships
cursor.execute('''
CREATE TABLE IF NOT EXISTS govt_scholarships (
    id INTEGER PRIMARY KEY,
    title TEXT,
    scheme_details TEXT,
    link TEXT,
    expiry_dates TEXT
)
''')


def scrape_government_scholarships():
    url = "https://scholarships.gov.in/All-Scholarships"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        scholarship_blocks = soup.find_all('div', class_='row mb-4 border-1 border-bottom')

        for block in scholarship_blocks:
            try:
                # Extract the title of the scholarship
                title = block.find('h6').text.strip()

                # Extract expiry dates
                expiry_dates = ', '.join([span.text.strip() for span in block.find_all('span')])

                # Extract the specifications link
                link_tag = block.find('a', text="Specifications")
                link = f"https://scholarships.gov.in{link_tag['href']}" if link_tag else 'No link available'

                # Store the data in the database
                cursor.execute('''
                INSERT INTO govt_scholarships (title, scheme_details, link, expiry_dates) 
                VALUES (?, ?, ?, ?)''',
                               (title, "Details about the scheme are in the link", link, expiry_dates))

            except Exception as e:
                print(f"Error extracting information: {e}")


# Run the scraping function
scrape_government_scholarships()

# Commit changes and close the database connection
conn.commit()
conn.close()

print("Government scholarship data has been successfully scraped and saved to the database.")
