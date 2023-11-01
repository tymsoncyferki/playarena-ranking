import unittest
from scraper import *


class TestScraper(unittest.TestCase):

    def test_remove_quotes(self):
        url = remove_quotes("'/uf/media/images_full/389266-0ac00115-8c29-6bf8.jpg'")
        self.assertEqual(url, "/uf/media/images_full/389266-0ac00115-8c29-6bf8.jpg")

    def test_get_image_url(self):
        html = '<div class="pull-left" id="user_avatar" data-update-progresbar="false" data-show-popover="false" +' \
                  ' data-container="body" data-toggle="popover" data-placement="bottom" data-content="Dodaj swoje' \
                  ' zdjęcie profilowe. Poprawnie wypełniony profil zawodnika musi posiadać wyraźne zdjęcie twarzy."> ' \
                  '<span class="img358"> <i id="user_avatar_image" ' \
                  'style="background-image:url(/uf/media/images_full/389266-0ac00115-8c29-6bf8.jpg)"></i> </span>' \
                  ' </div>'
        content = BeautifulSoup(html, 'html.parser')
        url = get_image_url(content)
        self.assertEqual(url, 'https://playarena.pl/uf/media/images_full/389266-0ac00115-8c29-6bf8.jpg')


if __name__ == "__main__":
    unittest.main()
