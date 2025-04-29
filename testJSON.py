import gzip
import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchWindowException
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration du driver ---
options = Options()
options.headless = False
options.add_argument("--disable-extensions")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(
    service=service,
    options=options,
    seleniumwire_options={}    # pas de proxy externe
)

def wait_click(xpath, timeout=20):
    try:
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        ).click()
    except Exception as e:
        print(f"Erreur wait_click({xpath}): {e}")

try:
    # 1) Navigation
    driver.get("https://www.projet-voltaire.fr/")
    wait_click("//*[@id='cmpbntnotxt']")
    wait_click("//*[@id='authenticateOption']")
    print("Authentification... done")
    time.sleep(5)
    wait_click("/html/body/div[4]/div/div/div[3]/button")
    wait_click("/html/body/div[7]/div/div/div[1]/a/span")
    wait_click("//*[@id='validationCellDiv_1']/div/div[1]/div[3]")

    # 2) Récupérer la phrase
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sentence"))
    )
    sentence = driver.find_element(By.CLASS_NAME, "sentence")
    sentence_words=sentence.find_elements(By.XPATH,".//*")
    words=[]
    for word in sentence_words:
        words.append(word.text)
    print(f"Phrase trouvée : {words}")

    word = [word for word in words if word.isalpha()]
    longest = max(word, key=len)

    # 3) Parcourir les requêtes capturées
    count = 0
    affiche = True
    for req in driver.requests:
        if req.response and "WolLearningContentWebService" in req.url :
            raw_bytes = req.response.body  
            # 4) Décompression gzip si nécessaire
            try:
                if raw_bytes.startswith(b'\x1f\x8b'):
                    raw = gzip.decompress(raw_bytes).decode("utf-8", errors="ignore")
                else:
                    raw = raw_bytes.decode("utf-8", errors="ignore")
            except Exception as e:
                print("Erreur lors de la décompression :", e)
                raw = raw_bytes.decode("utf-8", errors="ignore")
            count = count + 1
        if count==2 and affiche:
            affiche = False
            print(raw)
                



except NoSuchWindowException:
    print("La fenêtre a été fermée prématurément.")
except Exception as e:
    print("Erreur inattendue :", e)
finally:
    print("Terminé.")
    driver.quit()