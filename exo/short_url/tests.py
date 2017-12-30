from django.test import TestCase
from django.urls import reverse

from .models import URL
from .forms import URLForm


class URLFormTests(TestCase):
    # Useless test for duplicate entry
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
        self.assertFalse(duplicate.is_valid())

        # J'aurai pu faire ceci (même si c'est moins bien)
        # from django.db.utils import IntegrityError
        # self.assertRaises(IntegrityError, form.save)

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

    def test_hash_collision(self):
        """
        Create 2 entries in the db with the same hash. Verify if django raise an
        exception and load short_url/error.html template with error on the web
        page
        """
        url = "http://www.perdu.com"
        nickname = ""
        # pdb.set_trace()

        form = URLForm(data={'url_long': url, 'nickname': nickname})
        if form.is_valid():
            form.set
            test = form.save(commit=False)
            test.url_short = 'auie'
            print(test)
            test.save()


def create_new_url(url, nickname):
    """
    Create a new url in database with or without nickname
    """
    form = URLForm(data={'url_long': url, 'nickname': nickname})
    form.is_valid()
    form.save()
    # return URL.objects.create(url_long=url, nickname=nickname)


class URLFormViewTests(TestCase):
    def test_get_form_create_short_url(self):
        """
        Test if form page existed.
        """
        response = self.client.get(reverse('create_short_url'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_to_url_list_after_create_a_valid_url(self):
        """
        Create an entry and check if redirect on url_list view
        """
        response = self.client.post(
            reverse('create_short_url'),
            {
                'url_long': "http://www.caramail.com",
                'nickname': '',
            }
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('url_list'))
        self.assertQuerysetEqual(response.context['urls'],
                                 ['<URL: http://www.caramail.com>'])


class URLListViewTests(TestCase):

    def test_get_url_list(self):
        """
        Test if url_list page existed and if there are no url, displayed an
        appropriate message.
        """
        response = self.client.get(reverse('url_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No url are available.")
        self.assertQuerysetEqual(response.context['urls'], [])

    def test_url_without_nickname(self):
        """
        Create an url without a nickname
        """
        create_new_url(url="http://www.perdu.com", nickname="")
        response = self.client.get(reverse('url_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['urls'],
                                 ['<URL: http://www.perdu.com>'])
        for url in response.context['urls']:
            self.assertEqual(url.nickname, None)

    def test_url_with_nickname(self):
        """
        Create an url with a nickname
        """
        create_new_url(url="http://www.django.org", nickname="django")
        response = self.client.get(reverse('url_list'))
        self.assertEqual(response.status_code, 200)
        for url in response.context['urls']:
            self.assertEqual(url.nickname, "django")

    def test_get_two_past_url(self):
        """
        Create 2 urls
        """
        create_new_url(url="http://www.perdu.com", nickname="")
        create_new_url(url="http://www.djangoproject.com", nickname="django")
        response = self.client.get(reverse('url_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['urls'],
            [
                '<URL: http://www.perdu.com>',
                '<URL: http://www.djangoproject.com>'
            ]
        )

    def test_redirect_number(self):
        """
        Create an url, redirect and test if url.redirect_number == 1
        """
        create_new_url(url="http://www.perdu.com", nickname="")
        response = self.client.get(reverse('url_list'))
        url = response.context['urls'][0]
        self.client.get(reverse('redirect_to_long_url', args=(url.pk,)))
        url = URL.objects.get(pk=url.pk)
        self.assertEqual(url.redirect_number, 1)
