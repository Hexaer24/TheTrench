import gzip
import re
import string

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

def extrait_phrase(raw,phrase):
    # start correspond à l'indice de début de la zone de recherche dans le JSON
    start = 0
    # end correspond à l'indice de fin de la zone de recherche dans le JSON
    end = len(raw)
    # on début un maximum d'itérations afin d'etre sur de ne pas avoir une boucle infinie en cas d'erreurs
    max_iterations = 50
    iterations = 0

    # retourne le mot le plus long de la phrase (On prends ce mot car c'est celui qui a le plus de chance d'etre unique a la phrase et donc de ne pas etre présent dans d'autre phrase)
    mot = mot_le_plus_long(phrase)
    print(mot)
    # retourne la taille de la phrase
    taille = taille_totale(phrase)

    while iterations < max_iterations:
        try:
            # on sélectionne l'indice du mot le plus long dans la réponse JSON
            index_mot = raw.index(mot, start, end)
            print(index_mot,mot)
        except ValueError:
            print("Mot non trouvé dans le texte.")
            return None

        # on sélectionne ensuite à partir de cette indice les caractères présédents (taille de la phrase *2 afin d'etre sur de sélectionner la phrase entière)
        # on sélectionne également les caractères suivant (taille de la phrase*4 car on sélectionne le token(13AFF39BB245131BF1A55F6ED997202582F72BD2014 par exemple) + la phrase corigé  )
        trouve = raw[max(0, index_mot - 2 * taille): index_mot + 4 * taille]

        # cette boucle vérifie si tout les mots de la phrase sont présent dans ce qu'on vient de sélectionner si c'est le cas c'est la bonne réponse JSON
        bonne_phrase = True
        for mots in phrase:
            if mots and mots not in "'":
                if mots not in trouve:
                    bonne_phrase = False
                    break

        if bonne_phrase:

            # on sélectionne le premier mot de la phrase
            premier = phrase[0]
            # on sélectionne le deuxième mot de la phrase
            dernier = phrase[-1]

            # pattern correspond a ce qu'on cherche ici le premier mot de la phrase précédé d'une apostrophe
            debut_token = f"'{premier}"
            # et il faut que ce mot ne soit pas suivi par une autre l'etre de l'alpahbet sinon ('Je') pourrais etre sélectionné alors qu'on cherche ('J')
            pattern = re.compile(rf"'{premier}(?![a-zA-Z])")

            # On cherche donc ce patterne dans ce qu'on sélectionne de la réponse JSON
            debut_match = pattern.search(trouve)
            if not debut_match:
                print("Début non trouvé.")
                return None

            # indice dans la réponse JSON de premier mot de la phrase
            debut_index = debut_match.start()

            # fin_token correspond a ce qu'on cherche ici le dernier mot de la phrase suivi d'une apostrophe
            fin_token = f"{dernier}'"
            fin_index = trouve.rfind(fin_token)
            # si l'indice est différent de -1 c'est qu'on l'a trouvé
            if fin_index == -1:
                print("Fin non trouvée.")
                return None

            # fin_index correspond a l'indice du début du dernier mot, on ajoutte donc la taille du dernier mot pour l'avoir en entier
            fin_index += len(fin_token)

            # on extrait ensuite la phrase de réponse JSON a partir du premier et dernier mot de la phrase
            extrait = trouve[debut_index:fin_index]
            return extrait
        else:
            # si ce n'était pas la bonne phrase on recommence mais cette fois en cherchant après l'indice du mot le plus long qu'on vient de regarder
            # on va donc chercher la deuxième occurence du mot le plus long
            start = index_mot + 1
            iterations += 1

    print("Limite d'itérations atteinte sans trouver la phrase.")
    return None


# retourne le mot le plus long de la phrase
def mot_le_plus_long(mots):
    mots_valides = [mot for mot in mots if mot and mot not in string.punctuation]
    if not mots_valides:
        return None
    return max(mots_valides, key=len)

# retourne la taille totale de la phrase
def taille_totale(phrase):
    return sum(len(mot) for mot in phrase)

# extrait le mot entre \x3CB\x3E
def extraire_faute(raw_string):

    raw_string = raw_string.replace(r'\x3CB\x3E', '<B>').replace(r'\x3C/B\x3E', '</B>')


    pattern = r"<B>(.*?)</B>"
    matches = re.findall(pattern, raw_string)

    if matches:
        return matches
    else:
        return None

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
        #On enlève ce que l'on n'a pas besoin
        raw=extract_string(raw)

        #Permet de garder le JSON du dernier essai dans un fichier au lieu qu'il prenne la vue du terminal
        with open("json.txt", "w") as text_file:
            text_file.write("".join(raw))

        #boucle while ici: on a besoin du JSON qu'une seule fois
        sentence = self.find_element(".sentence")
        sentence_words = sentence.find_elements("xpath", ".//*")
        words = [word.text for word in sentence_words]
        print(f"Phrase trouvée : {clean_words(words)}")
        bloc_string = extrait_phrase(raw, words)
        print(bloc_string)

        # Si un mot est entouré par \x3CB\x3E on le return
        faute = extraire_faute(bloc_string)
        print(f"Faute : {faute}")
        self.sleep(9999)

def find_sentence(sentence,json):
    filtered_sentence=filter_sentence(sentence)
    points=0

#Enlève la ponctuation de la phrase
def filter_sentence(s):
    translator = str.maketrans('', '', string.punctuation)
    return s.translate(translator)