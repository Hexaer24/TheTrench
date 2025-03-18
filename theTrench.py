import requests
from selenium import webdriver
from selenium.common import NoSuchWindowException, ElementClickInterceptedException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Step 1: Set up the GeckoDriver for Firefox
# Replace 'path/to/geckodriver' with the actual path to your geckodriver executable
service = Service(r"E:\projects\tools\geckoDriver\geckodriver.exe")

# Step 2: Configure Firefox options (like headless mode if needed)
options = Options()
options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
options.headless = False  # Set to True for headless mode (invisible browser)

# Step 3: Create a WebDriver instance for Firefox
driver = webdriver.Firefox(service=service, options=options)

timelimit=999
def wait_click(xpath):
    try:
        WebDriverWait(driver, timelimit).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()
    except ElementClickInterceptedException:
        print(xpath, " unavailable")
        wait_click(xpath)

def wait_click_nice(xpath):
    try:
        WebDriverWait(driver, timelimit).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()
    except ElementClickInterceptedException:
        print(xpath, " unavailable")
        return False
try:
    # Step 4: Open the target website
    driver.get('https://www.projet-voltaire.fr/')  # Replace with your target URL
    wait_click("//*[@id='cmpbntnotxt']")
    wait_click("//*[@id='authenticateOption']")
    print("Authentification \nP.S: (Je suis même pas capable techniquement de voler un mot de passe)")
    wait_click("/html/body/div[4]/div/div/div[3]/button")
    wait_click("/html/body/div[7]/div/div/div[1]/a/span")
    wait_click("/html/body/div[5]/div[3]/div[2]/div/div[2]/div[6]/div/div[1]/div[3]")

    #Questions
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sentence")))
    sentence= driver.find_element(By.CLASS_NAME,"sentence")
    sentence_words=sentence.find_elements(By.XPATH,".//*")
    words=[]
    for word in sentence_words:
        words.append(word.text)
    print(words)
except NoSuchWindowException:
    print("window closed prematurely")
finally:
    # Step 6: Close the browser
    print("done")
    #driver.quit()