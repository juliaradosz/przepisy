from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Category, Tag, Ingredient, Comment


class Command(BaseCommand):
    help = 'Usuwa wszystkie przepisy i dodaje nowe'

    def handle(self, *args, **options):
        # Usuń wszystkie przepisy, składniki, komentarze
        Comment.objects.all().delete()
        Ingredient.objects.all().delete()
        Recipe.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()
        self.stdout.write('Usunięto wszystkie przepisy.')

        # Pobierz lub stwórz użytkownika
        user = User.objects.first()

        # Kategoria
        cat, _ = Category.objects.get_or_create(name='Desery i wypieki', slug='desery-i-wypieki')

        # Tagi
        tag1, _ = Tag.objects.get_or_create(name='gofry', slug='gofry')
        tag2, _ = Tag.objects.get_or_create(name='słodkie', slug='slodkie')

        # Przepis
        recipe = Recipe.objects.create(
            title='Chrupiące gofry',
            slug='chrupiace-gofry',
            author=user,
            category=cat,
            description='Przepis na chrupiące gofry - na 16 sztuk, wielkości 10 cm x 12 cm.',
            instructions=(
                '1. Zaczynamy od oddzielenia białek od żółtek.\n'
                '2. Następnie do dużej miski wsypujemy mąkę, proszek do pieczenia, sól, '
                'cukier. Dolewamy mleko i olej oraz dodajemy żółtka.\n'
                '3. Całość mieszamy, ale nie ubijamy. Składniki można wrzucić do blendera, '
                'można użyć również blendera ręcznego, ważne jest aby nie ubijać ciasta, '
                'a tylko je wymieszać.\n'
                '4. Jeśli nie macie blendera, ciasto można wymieszać ręcznie za pomocą '
                'trzepaczki lub np. widelca (będzie nieco trudniej, ale da się).\n'
                '5. Gdy ciasto będzie już gładkie i jednolite zaczynamy nagrzewać gofrownicę.\n'
                '6. W międzyczasie ubijamy jeszcze 2 białka (pozostałe z żółtek) na sztywną '
                'pianę i ubitą pianę z białek dodajemy do ciasta, delikatnie mieszając.\n'
                '7. Gdy ciasto jest gotowe nabieramy łyżką i wylewamy na rozgrzaną formę do gofrów.\n'
                '8. Gofry pieczemy przez 3 minuty (lub dłużej, w zależności od mocy gofrownicy).\n'
                '9. Po upieczeniu ostrożnie zdejmujemy na talerz i od razu zjadamy z ulubionymi dodatkami.'
            ),
            prep_time=15,
            cook_time=3,
            servings=16,
            difficulty='easy',
            is_published=True,
        )
        recipe.tags.add(tag1, tag2)

        # Składniki
        skladniki = [
            ('Mąka pszenna typu 500-550', '2', 'szklanki (300 g)'),
            ('Proszek do pieczenia', '1', 'łyżeczka (5 g)'),
            ('Sól', '1', 'szczypta (2 g)'),
            ('Mleko 2%', '2', 'szklanki (500 ml)'),
            ('Cukier', '1', 'pełna łyżka (20 g)'),
            ('Olej', '1/3', 'szklanki (70 g)'),
            ('Jajka duże', '2', 'szt. (białka i żółtka oddzielnie)'),
        ]
        for name, qty, unit in skladniki:
            Ingredient.objects.create(recipe=recipe, name=name, quantity=qty, unit=unit)

        self.stdout.write(self.style.SUCCESS('Dodano: Chrupiące gofry'))
