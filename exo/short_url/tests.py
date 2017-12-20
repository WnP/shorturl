from django.test import TestCase

# from django.core.exceptions.ObjectDoesNotExist import DoesNotExist
from django.core.exceptions import ObjectDoesNotExist

from .models import URL
from .forms import URLForm


class URLTests(TestCase):
    def test_create_an_entry(self):
        """
        Create an entry in the db and test if it exists
        """
        new_url = URL(url_long="www.google.fr")
        new_url.save()
        url_in_db = URL.objects.get(url_long="www.google.fr")
        self.assertEqual(new_url, url_in_db)

    def test_create_duplicate_entry(self):
        """
        Create a duplicate entry
        """
        form = URLForm(data={'url_long': "http://www.conchita.com"})
        form.is_valid()
        form.save()
        duplicate = URLForm(data={'url_long': "http://www.conchita.com"})
        print("Is valid: {}".format(duplicate.is_valid()))
        # self.assertRaises(URL.DoesNotExist, duplicate.save)
        # self.assertRaises(URL.DoesNotExist, form.save, **{'url_long': "http://www.conchita.com"})
        # self.assertRaises(ObjectDoesNotExist, {'url_long': "http://www.conchita.com"})
        # try:
        #     form.save()
        # except(ObjectDoesNotExist):
        #     print("coin")

    def test_URLForm_is_valid(self):
        """
        Test if URLForm is valid with valid entry
        """
        form = URLForm(data={'url_long': "http://www.caramail.com"})
        self.assertTrue(form.is_valid())

    def test_URLForm_is_invalid(self):
        """
        Test if URLForm is invalid with invalid entry
        """
        form = URLForm(data={'url_long': ""})
        self.assertFalse(form.is_valid())

    def test_create_an_entry_with_URLForm(self):
        """
        Create an entry in the db with form and test if it exists and is equal
        with original
        """
        form = URLForm(data={'url_long': "http://www.google.fr"})
        form.is_valid()
        form.save()
        url_in_db = URL.objects.get(url_long="http://www.google.fr")
        self.assertEqual(url_in_db.url_long, "http://www.google.fr")
        self.assertIsNone(url_in_db.nickname)
        self.assertIsNotNone(url_in_db.url_short)
