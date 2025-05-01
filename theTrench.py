import gzip
import re
from seleniumbase import BaseCase


def extract_string(raw):
    start = raw.rfind('["')
    end = raw.rfind(']') + 1
    if start == -1 or end == -1:
        return []
    array_str = raw[start:end]
    return re.findall(r'"(.*?)"', array_str, flags=re.DOTALL)

def clean_words(words):
    clean = ''
    for char in words:
        if(char==''):
            char=' '
        clean+=char
    return clean

BaseCase.main(__name__, __file__)

class TheTrench(BaseCase):
    def test_the_trench(self):
        self.open("https://compte.groupe-voltaire.fr/login")
        target = "https://www.projet-voltaire.fr/choix-parcours/"
        while self.get_current_url() != target:
            self.sleep(0.5)
        self.click('#cmpbntnotxt')
        self.click('button:contains("compris")')
        self.click('span:contains("Orthographe")')
        self.click('.validation-activity-cell-rectangle')

        self.wait_for_element_present(".sentence", timeout=60)
        #On attend la phrase, ça assure que le JSON à chargé

        count = 0
        raw = ''
        for req in self.driver.requests:
            if req.response and "WolLearningContentWebService" in req.url:
                raw_bytes = req.response.body
                try:
                    if raw_bytes.startswith(b'\x1f\x8b'):
                        raw = gzip.decompress(raw_bytes).decode("utf-8", errors="ignore")
                    else:
                        raw = raw_bytes.decode("utf-8", errors="ignore")
                except Exception as e:
                    print("Erreur lors de la décompression :", e)
                    raw = raw_bytes.decode("utf-8", errors="ignore")
                count += 1
                if count == 2:
                    break
        print(extract_string(raw))

        #boucle while ici: on a besoin du JSON qu'une seule fois
        sentence = self.find_element(".sentence")
        sentence_words = sentence.find_elements("xpath", ".//*")
        words = [word.text for word in sentence_words]
        print(f"Phrase trouvée : {clean_words(words)}")





        self.sleep(9999)