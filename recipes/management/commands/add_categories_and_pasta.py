"""
Dodaje nowe kategorie i przepis na spaghetti z pieczonym sosem pomidorowym.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from recipes.models import Category, Recipe, Ingredient


class Command(BaseCommand):
    help = 'Dodaje kategorie i spaghetti z pieczonym sosem'

    def handle(self, *args, **options):
        user = User.objects.first()

        # Nowe kategorie
        categories_data = [
            ('Dania główne', 'Obiadowe dania główne'),
            ('Desery i wypieki', 'Słodkie wypieki i desery'),
            ('Makarony', 'Dania z makaronem'),
            ('Śniadanie', 'Przepisy na śniadanie'),
            ('Kolacja', 'Lekkie dania na kolację'),
            ('Zupy', 'Ciepłe i sycące zupy'),
            ('Sałatki', 'Świeże i zdrowe sałatki'),
            ('Przekąski', 'Szybkie przekąski'),
        ]
        for name, desc in categories_data:
            cat, created = Category.objects.get_or_create(
                name=name,
                defaults={'slug': slugify(name), 'description': desc},
            )
            if created:
                self.stdout.write(f'  Dodano kategorię: {name}')

        makarony = Category.objects.get(name='Makarony')

        # Przepis
        title = 'Spaghetti z pieczonym sosem pomidorowym'
        slug = slugify(title)
        if Recipe.objects.filter(slug=slug).exists():
            self.stdout.write(f'  Przepis "{title}" już istnieje, pomijam.')
        else:
            recipe = Recipe.objects.create(
                title=title,
                slug=slug,
                author=user,
                category=makarony,
                description='Spaghetti z pieczonym sosem pomidorowym z serkiem wiejskim i parmezanem. Proste, zdrowe i pyszne!',
                instructions=(
                    '1. Pomidorki koktajlowe umyj, a cebulę pokrój na kilka kawałków. '
                    'Wyłóż warzywa na blaszkę wyłożoną papierem do pieczenia.\n'
                    '2. Polej całość oliwą. Z czosnku utnij górę, aby ząbki się odsłoniły. '
                    'Polej go również oliwą i wyłóż obok warzyw. Posyp całość solą i pieprzem. '
                    'Wstaw do piekarnika rozgrzanego do 180 stopni, na 30-40 minut (termoobieg).\n'
                    '3. Gdy warzywa się pieką, ugotuj makaron według instrukcji na opakowaniu.\n'
                    '4. Po upieczeniu warzyw, w blenderze umieść pomidory, czosnek, cebulę, '
                    'serek wiejski, starty parmezan, sól oraz pieprz. Zblenduj na jednolitą masę. '
                    'Spróbuj i dopraw ewentualnie do smaku solą/pieprzem.\n'
                    '5. Sos wylej na patelnię i wymieszaj z makaronem. Posyp (najlepiej świeżym) pieprzem.'
                ),
                servings=3,
            )
            ingredients_data = [
                ('Pomidorki koktajlowe', '500', 'g'),
                ('Cebula', '1', 'szt. (100-120 g)'),
                ('Czosnek', '1', 'główka'),
                ('Oliwa z oliwek', '15', 'g'),
                ('Parmezan', '60', 'g'),
                ('Sól', '2-3', 'szczypty'),
                ('Pieprz', '2-3', 'szczypty'),
                ('Serek wiejski (naturalny)', '200', 'g'),
                ('Makaron spaghetti', '240', 'g'),
            ]
            for name, qty, unit in ingredients_data:
                Ingredient.objects.create(recipe=recipe, name=name, quantity=qty, unit=unit)
            self.stdout.write(f'  Dodano: {title}')

        self.stdout.write(self.style.SUCCESS('Gotowe!'))
