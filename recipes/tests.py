from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, Tag, Recipe, Ingredient, Comment, UserProfile


class ModelTestCase(TestCase):
    """Testy modeli."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.category = Category.objects.create(name='Zupy', slug='zupy', description='Zupy testowe')
        self.tag = Tag.objects.create(name='szybkie', slug='szybkie')
        self.recipe = Recipe.objects.create(
            title='Testowa zupa', slug='testowa-zupa', author=self.user,
            category=self.category, description='Opis zupy',
            instructions='Gotuj 30 min', prep_time=10, cook_time=30, servings=4,
        )
        self.recipe.tags.add(self.tag)

    def test_recipe_str(self):
        self.assertEqual(str(self.recipe), 'Testowa zupa')

    def test_recipe_total_time(self):
        self.assertEqual(self.recipe.total_time, 40)

    def test_recipe_get_absolute_url(self):
        self.assertEqual(self.recipe.get_absolute_url(), '/przepis/testowa-zupa/')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Zupy')

    def test_ingredient_str(self):
        ingredient = Ingredient.objects.create(
            recipe=self.recipe, name='Marchew', quantity='3', unit='szt.',
        )
        self.assertEqual(str(ingredient), '3 szt. - Marchew')

    def test_ingredient_str_no_unit(self):
        ingredient = Ingredient.objects.create(
            recipe=self.recipe, name='Sól', quantity='1',
        )
        self.assertEqual(str(ingredient), '1 - Sól')

    def test_comment_str(self):
        comment = Comment.objects.create(
            recipe=self.recipe, author=self.user, content='Pyszna!', rating=5,
        )
        self.assertEqual(str(comment), 'Komentarz testuser do Testowa zupa')

    def test_average_rating(self):
        user2 = User.objects.create_user(username='user2', password='pass123')
        Comment.objects.create(recipe=self.recipe, author=self.user, content='Super', rating=5)
        Comment.objects.create(recipe=self.recipe, author=user2, content='OK', rating=3)
        self.assertEqual(self.recipe.average_rating, 4.0)

    def test_user_profile_str(self):
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(str(profile), 'Profil: testuser')


class ViewTestCase(TestCase):
    """Testy widoków."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.category = Category.objects.create(name='Zupy', slug='zupy')
        self.recipe = Recipe.objects.create(
            title='Testowa zupa', slug='testowa-zupa', author=self.user,
            category=self.category, description='Opis', instructions='Instrukcje',
            prep_time=10, cook_time=30, servings=4,
        )

    def test_home_view(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Przepisy Kulinarne')

    def test_recipe_list_view(self):
        response = self.client.get(reverse('recipes:recipe_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Testowa zupa')

    def test_recipe_detail_view(self):
        response = self.client.get(reverse('recipes:recipe_detail', kwargs={'slug': 'testowa-zupa'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Testowa zupa')

    def test_category_list_view(self):
        response = self.client.get(reverse('recipes:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Zupy')

    def test_category_detail_view(self):
        response = self.client.get(reverse('recipes:category_detail', kwargs={'slug': 'zupy'}))
        self.assertEqual(response.status_code, 200)

    def test_search_view(self):
        response = self.client.get(reverse('recipes:search'), {'query': 'zupa'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Testowa zupa')

    def test_search_empty(self):
        response = self.client.get(reverse('recipes:search'), {'query': 'pizza'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Testowa zupa')

    def test_recipe_create_requires_login(self):
        response = self.client.get(reverse('recipes:recipe_create'))
        self.assertEqual(response.status_code, 302)

    def test_recipe_create_logged_in(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('recipes:recipe_create'))
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        response = self.client.get(reverse('recipes:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_creates_user(self):
        response = self.client.post(reverse('recipes:register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'SuperSecret123!',
            'password2': 'SuperSecret123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view(self):
        response = self.client.post(reverse('recipes:login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)

    def test_profile_view(self):
        UserProfile.objects.create(user=self.user)
        response = self.client.get(reverse('recipes:profile', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_recipe_delete_requires_author(self):
        other_user = User.objects.create_user(username='other', password='pass123')
        self.client.login(username='other', password='pass123')
        response = self.client.post(reverse('recipes:recipe_delete', kwargs={'slug': 'testowa-zupa'}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Recipe.objects.filter(slug='testowa-zupa').exists())

    def test_comment_add(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('recipes:recipe_detail', kwargs={'slug': 'testowa-zupa'}),
            {'content': 'Pyszne!', 'rating': 5},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)
