from django.test import TestCase, Client
from .models import Product
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class ProductTest(TestCase):
    fixtures = ['data.json', ]

    def setUp(self):
        self.client = Client()
        self.product = Product.objects.get(pk=13)
        self.user = User.objects.create_user(username='username', email='email@email.com', password='password')

    def test_get_product(self):
        """
        Open page with product.
        """
        response = self.client.get(reverse('product_slug', args=[self.product.slug]))
        # If loading page was success status_code will be 200.
        self.assertEqual(response.status_code, 200)

    def test_change_like_without_login(self):
        """
        Add like if user is not authenticated.
        """
        like_before = self.product.like_count
        data = {'product_id': self.product.id, 'slug': self.product.slug}
        self.client.post(reverse('like'), data, follow=True)
        like_after = Product.objects.get(pk=self.product.id).like_count
        # If user doesn't login like_before and like_after must be identical.
        self.assertEqual(like_before == like_after, True)

    def test_change_like_with_login(self):
        """
        Add like if user is not authenticated.
        """
        like_before = self.product.like_count
        self.client.login(username='username', password='password')
        data = {'product_id': self.product.id, 'slug': self.product.slug}
        self.client.post(reverse('like'), data, follow=True)
        like_after = Product.objects.get(pk=self.product.id).like_count
        # If user login like_before != like_after after response.
        self.assertEqual(like_before == like_after, False)

    def test_add_comment(self):
        """
        Add valid comment.
        """
        data = {'text': 'The test message', 'product_id': 13}
        # Try to add valid comment.
        response = self.client.post(reverse('add_comment'), data, follow=True)
        # response.context['comments'][0] return last added comment.
        self.assertEqual(response.context['comments'][0].text, data['text'])

    def test_add_empty_comment(self):
        """
        Add not valid comment.
        """
        data = {'text': '', 'product_id': 13}
        # Try to add not valid comment.
        response = self.client.post(reverse('add_comment'), data, follow=True)
        # If comment didn't add to db, response.context['comments'] will be empty.
        self.assertEqual(list(response.context['comments']), [])
