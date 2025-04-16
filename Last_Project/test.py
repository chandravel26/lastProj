from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time

# Setup WebDriver
service = Service(r"C:\Users\ChandravelMK\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe")
# options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Run in headless mode
# options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service)

# Open the website with infinite scroll
driver.get("https://www.vmc.com/")  # Sample site with infinite scroll

# Scroll and collect data
quotes = set()
scroll_pause_time = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)

    # Extract quote texts
    quote_elements = driver.find_elements(By.CLASS_NAME, "quote")
    for quote in quote_elements:
        quotes.add(quote.text)

    # Check if we've reached the bottom
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Done
driver.quit()

# Print all quotes
for i, quote in enumerate(quotes, start=1):
    print(f"{i}. {quote}")
