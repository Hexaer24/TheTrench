import gzip

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
        count = 0
        affiche = True
        for req in self.driver.requests:
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
            if count == 2 and affiche:
                affiche = False
                print(raw)
        self.sleep(9999)