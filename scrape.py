from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https://www.studentbeans.com/student-discount/us/all")
time.sleep(5)

# Scroll to load content
scroll_pause = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Extract discount information
discount_sections = driver.find_elements(By.TAG_NAME, "article")

for section in discount_sections:
    try:
        # Extract brand name
        brand = section.find_element(By.XPATH, ".//p[@data-testid='offer-tile-brand']").text.strip()

        # Extract discount details (title)
        discount_title = section.find_element(By.XPATH, ".//h4[@data-testid='offer-tile-title']").text.strip()

        # Try to extract expiration date
        try:
            expiry = section.find_element(By.XPATH, ".//span[@data-testid='offerBoostExpiry']").text.strip()
        except:
            expiry = "No expiration date available"

        # Display the brand and discount information
        print(f"Brand: {brand}")
        print(f"Discount: {discount_title}")
        print(f"Expires: {expiry}\n")
    except Exception as e:
        print(f"Error extracting information: {e}")
        # Optional: Print the inner HTML for debugging
        print(section.get_attribute('innerHTML'))

# Close the driver
driver.quit()
