from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize WebDriver
driver = webdriver.Chrome()  # Or webdriver.Firefox() if using Firefox
driver.get("https://www.studentbeans.com/student-discount/us/all")
time.sleep(5)  # Wait for page to load fully

# Scroll down to load more content (if necessary)
scroll_pause = 2
while True:
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break

# Extract discount information
discount_sections = driver.find_elements(By.CLASS_NAME, "discount-card")  # Adjust class if necessary

for section in discount_sections:
    # Extract brand name and discount details
    try:
        brand = section.find_element(By.TAG_NAME, "h3").text.strip()
        discount_detail = section.find_element(By.TAG_NAME, "p").text.strip()
        print(f"Brand: {brand}")
        print(f"Discount Details: {discount_detail}\n")
    except Exception as e:
        print(f"Error extracting information: {e}")

# Close the driver
driver.quit()
