from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Setup Chrome with SSL errors ignored
options = Options()
options.add_argument("--ignore-certificate-errors")  # Ignore SSL certificate errors
options.add_argument("--disable-blink-features=AutomationControlled")  # Hide automation flags
#options.add_argument("--headless")  # Optional: Run in headless mode
options.add_argument("--allow-insecure-localhost")  # Allow insecure localhost connections
options.add_argument("--disable-features=RendererCodeIntegrity")  # Disable integrity checks
options.add_argument("--disable-gpu")  # Disable GPU (useful for headless mode)
options.add_argument("--no-sandbox")  # Disable sandbox (useful for Docker or CI)
options.add_argument("--incognito")  # Run in incognito mode to avoid cache issues
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")


# Force TLS 1.2 usage
options.add_argument("--ssl-version-max=tls1.2")

# Path to your matching ChromeDriver
service = Service(r"C:\Users\ChandravelMK\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# Open a sample infinite scroll page (you can test this safely)
driver.get("https://www.vanrenterghemenco.be/")
time.sleep(10)  # Wait for the page to load
# Click the "Accept" button https://www.vanrenterghemenco.be


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
# paragraphs = driver.find_elements(By.TAG_NAME, "p")
elements = driver.find_elements(By.XPATH, "//*")
all_text = [element.text for element in elements if element.text.strip() != ""]
# for i, text in enumerate(all_text, 1):
#     print(f"{i}. {text.strip()}")
print(all_text)
print("ok")
# for i, p in enumerate(paragraphs, 1):
#     print(f"{i}. {p.text.strip()}")

#driver.quit()
