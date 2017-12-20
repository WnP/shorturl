from django.test import TestCase

from .models import URL

# Créer une url avec un racourci
# Si url_long existe déjà
# Si url_short existe déjà

# Faire plusieurs insert dans la db et vérifier que j'ai bien la liste


# Écrire un test qui crée un enregistrement
class URLTests(TestCase):
    def create_an_entry(self):
        """
        Create an entry in the db and test if it exists
        """
        new_url = URL(url_long="www.google.fr")
        url_in_db = URL.objects.get(url_long="www.google.fr")
        self.assertEqual(new_url, url_in_db)
