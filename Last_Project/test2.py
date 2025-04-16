from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Setup Chrome with SSL errors ignored
options = Options()
options.add_argument("--headless")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-blink-features=AutomationControlled")

# Path to your matching ChromeDriver
service = Service(r"C:\Users\ChandravelMK\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# Open a sample infinite scroll page (you can test this safely)
driver.get("https://www.vmc.com/")
try:
    accept_button = driver.find_element(By.CLASS_NAME, "accept")
    accept_button.click()
    print("✅ Accept button clicked!")
except Exception as e:
    print(f"❌ Couldn't click accept button: {e}")

# Scroll and extract post titles
scroll_pause_time = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)
    
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Example extraction: grabbing all paragraphs
paragraphs = driver.find_elements(By.TAG_NAME, "p")
for i, p in enumerate(paragraphs, 1):
    print(f"{i}. {p.text.strip()}")

driver.quit()
