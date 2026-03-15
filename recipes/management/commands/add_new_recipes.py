"""
Dodaje nowe przepisy: lazania, makaron z kurczakiem, makaron z boczkiem.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from recipes.models import Category, Tag, Recipe, Ingredient


class Command(BaseCommand):
    help = 'Dodaje lazanię, makaron z kurczakiem i makaron z boczkiem'

    def handle(self, *args, **options):
        user = User.objects.first()

        # Kategorie
        dania, _ = Category.objects.get_or_create(
            name='Dania główne',
            defaults={'slug': 'dania-glowne', 'description': 'Obiadowe dania główne'},
        )
        makarony, _ = Category.objects.get_or_create(
            name='Makarony',
            defaults={'slug': 'makarony', 'description': 'Dania z makaronem'},
        )

        recipes_data = [
            {
                'title': 'Lazania',
                'category': dania,
                'description': 'Klasyczna lazania z sosem mięsnym, mozzarellą i śmietanką — przepis z aniagotuje.pl.',
                'instructions': (
                    '1. Zmielone mięso (700 g łopatki wieprzowej) wymieszaj z przyprawami: '
                    'po płaskiej łyżce majeranku i ziół prowansalskich, po płaskiej łyżeczce soli, pieprzu i słodkiej papryki.\n'
                    '2. Posiekaj 2 cebule i 6 ząbków czosnku, pokrój 200 g pieczarek.\n'
                    '3. Na 4 łyżkach oleju podsmażaj warzywa przez 5 minut, dodaj mięso i smaż rozdrabniając łyżką.\n'
                    '4. Wlej 330 g przecieru pomidorowego i 200 g koncentratu pomidorowego, wymieszaj i duś chwilę aż powstanie gęsty sos.\n'
                    '5. Zanurz płaty makaronu do lazanii we wrzątku na ok. 60 sekund i wyłów szczypcami.\n'
                    '6. W naczyniu żaroodpornym (30x22x6 cm) układaj warstwami: makaron, farsz mięsny, tarty ser. Powtórz 4 razy.\n'
                    '7. Na wierzch polej mieszanką 100 g śmietanki 30% i 80 ml mleka, posyp resztą sera.\n'
                    '8. Piecz 50 minut w 180°C (góra/dół, środkowa półka) aż ser się zarumieni.'
                ),
                'prep_time': 30,
                'cook_time': 50,
                'servings': 6,
                'difficulty': 'medium',
                'ingredients': [
                    ('Łopatka wieprzowa (mielona)', '700', 'g'),
                    ('Cebula', '2', 'szt. (200 g)'),
                    ('Czosnek', '6', 'ząbków'),
                    ('Pieczarki', '200', 'g'),
                    ('Przecier pomidorowy', '330', 'g'),
                    ('Koncentrat pomidorowy', '200', 'g'),
                    ('Olej roślinny', '4', 'łyżki'),
                    ('Majeranek', '1', 'łyżka'),
                    ('Zioła prowansalskie', '1', 'łyżka'),
                    ('Sól', '1', 'łyżeczka'),
                    ('Pieprz', '1', 'łyżeczka'),
                    ('Papryka słodka', '1', 'łyżeczka'),
                    ('Płaty makaronu lasagne', '215', 'g (12 szt.)'),
                    ('Ser mozzarella', '250', 'g'),
                    ('Ser żółty', '250', 'g'),
                    ('Śmietanka 30%', '100', 'g'),
                    ('Mleko', '80', 'ml'),
                ],
            },
            {
                'title': 'Makaron z kurczakiem w sosie serowym',
                'category': makarony,
                'description': 'Szybki makaron z kurczakiem w kremowym sosie z parmezanu. Łatwe i smaczne!',
                'instructions': (
                    '1. Do kurczaka dodaj czosnek granulowany, paprykę wędzoną oraz sól.\n'
                    '2. Smaż kurczaka na oliwie z oliwek aż będzie złoty.\n'
                    '3. Ugotuj makaron al dente.\n'
                    '4. Usmażonego kurczaka przełóż na inne naczynie.\n'
                    '5. Na tej samej patelni rozpuść masło, dodaj łyżeczkę mąki.\n'
                    '6. Wlej mleko (jeżeli myślisz, że dałeś dużo to znaczy, że dałeś idealnie).\n'
                    '7. Można dodać czosnek świeży.\n'
                    '8. Na koniec dodaj parmezan/grana padano i wszystko wymieszaj aż ser się roztopi.\n'
                    '9. Dodaj makaron i kurczaka do sosu, wymieszaj.'
                ),
                'prep_time': 10,
                'cook_time': 20,
                'servings': 2,
                'difficulty': 'easy',
                'ingredients': [
                    ('Pierś z kurczaka', '300', 'g'),
                    ('Makaron (np. penne)', '200', 'g'),
                    ('Masło', '1', 'łyżka'),
                    ('Mąka', '1', 'łyżeczka'),
                    ('Mleko', '200', 'ml'),
                    ('Parmezan / Grana Padano', '50', 'g'),
                    ('Oliwa z oliwek', '2', 'łyżki'),
                    ('Czosnek granulowany', '1', 'łyżeczka'),
                    ('Papryka wędzona', '1', 'łyżeczka'),
                    ('Sól', '', 'do smaku'),
                ],
            },
            {
                'title': 'Makaron z boczkiem w sosie serowym',
                'category': makarony,
                'description': 'Makaron z boczkiem w kremowym sosie z parmezanu. Wersja z boczkiem zamiast kurczaka.',
                'instructions': (
                    '1. Boczek pokrój w paski, dodaj czosnek granulowany, paprykę wędzoną oraz sól.\n'
                    '2. Smaż boczek na oliwie z oliwek aż będzie chrupiący.\n'
                    '3. Ugotuj makaron al dente.\n'
                    '4. Usmażony boczek przełóż na inne naczynie.\n'
                    '5. Na tej samej patelni rozpuść masło, dodaj łyżeczkę mąki.\n'
                    '6. Wlej mleko (jeżeli myślisz, że dałeś dużo to znaczy, że dałeś idealnie).\n'
                    '7. Można dodać czosnek świeży.\n'
                    '8. Na koniec dodaj parmezan/grana padano i wszystko wymieszaj aż ser się roztopi.\n'
                    '9. Dodaj makaron i boczek do sosu, wymieszaj.'
                ),
                'prep_time': 10,
                'cook_time': 20,
                'servings': 2,
                'difficulty': 'easy',
                'ingredients': [
                    ('Boczek', '200', 'g'),
                    ('Makaron (np. penne)', '200', 'g'),
                    ('Masło', '1', 'łyżka'),
                    ('Mąka', '1', 'łyżeczka'),
                    ('Mleko', '200', 'ml'),
                    ('Parmezan / Grana Padano', '50', 'g'),
                    ('Oliwa z oliwek', '2', 'łyżki'),
                    ('Czosnek granulowany', '1', 'łyżeczka'),
                    ('Papryka wędzona', '1', 'łyżeczka'),
                    ('Sól', '', 'do smaku'),
                ],
            },
        ]

        for data in recipes_data:
            slug = slugify(data['title'])
            if Recipe.objects.filter(slug=slug).exists():
                self.stdout.write(f'  Przepis "{data["title"]}" już istnieje, pomijam.')
                continue

            recipe = Recipe.objects.create(
                title=data['title'],
                slug=slug,
                author=user,
                category=data['category'],
                description=data['description'],
                instructions=data['instructions'],
                prep_time=data['prep_time'],
                cook_time=data['cook_time'],
                servings=data['servings'],
                difficulty=data['difficulty'],
            )

            for name, qty, unit in data['ingredients']:
                Ingredient.objects.create(recipe=recipe, name=name, quantity=qty, unit=unit)

            self.stdout.write(f'  Dodano: {data["title"]}')

        self.stdout.write(self.style.SUCCESS('Nowe przepisy zostały dodane!'))
