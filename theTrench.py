from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class TheTrench(BaseCase):
    def test_the_trench(self):
        self.open("https://compte.groupe-voltaire.fr/login")
        while self.get_current_url()!="https://www.projet-voltaire.fr/choix-parcours/":
            self.sleep(0.5)
        self.click('#cmpbntnotxt')
        self.click('button:contains("compris")')
        self.click('span:contains("Orthographe")')

        self.click('.validation-activity-cell-rectangle')
        self.sleep(9999)


        """       
        self.type("#username", "demo_user")
        self.type("#password", "secret_pass")
        self.click('a:contains("Sign in")')
        self.assert_exact_text("Welcome!", "h1")
        self.assert_element("img#image1")
        self.highlight("#image1")
        self.sleep(2)
        self.click_link("Sign out")
        self.assert_text("signed out", "#top_message")
        self.sleep(9999)


service = Service(r"E:\projects\tools\geckoDriver\geckodriver.exe")

# Step 2: Configure Firefox options (like headless mode if needed)
options = Options()
options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
options.headless = False  # Set to True for headless mode (invisible browser)

# Step 3: Create a WebDriver instance for Firefox
driver = webdriver.Firefox(service=service, options=options)

timelimit=30
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
    wait_click("/html/body/div[5]/div[3]/div[2]/div/div[2]/div[7]/div/div[2]/div[2]/button")
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
    #driver.quit()"""