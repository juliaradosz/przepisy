from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from recipes.models import Category, Recipe, Ingredient


class Command(BaseCommand):
    help = 'Dodaje sernik baskijski'

    def handle(self, *args, **options):
        user = User.objects.first()
        desery, _ = Category.objects.get_or_create(
            name='Desery i wypieki',
            defaults={'slug': 'desery-i-wypieki', 'description': 'Ciasta, desery i wypieki'},
        )

        slug = slugify('Sernik baskijski')
        if Recipe.objects.filter(slug=slug).exists():
            self.stdout.write('Sernik baskijski juz istnieje, pomijam.')
            return

        recipe = Recipe.objects.create(
            title='Sernik baskijski',
            slug=slug,
            author=user,
            category=desery,
            description='Kremowy sernik baskijski z ciasteczkowym spodem — przypalony z wierzchu, w srodku jak jedwab. Minimum 10 godzin w lodowce przed podaniem.',
            instructions=(
                'Spod ciasteczkowy:\n'
                '1. Herbatniki maslane (130 g) blendujemy na pyl za pomoca blendera recznego.\n'
                '2. Maslo (50 g) roztapiamy i odstawiamy do lekkiego przestygniecia.\n'
                '3. Mieszamy herbatniki z maslem do powstania konsystencji mokrego piasku.\n'
                '4. Wykladamy spodem tortownice (24 cm) z natluszczonymi bokami i dnem wylozonym papierem do pieczenia. Dociskamy lyzka.\n\n'
                'Masa serowa:\n'
                '5. Nastawiamy piekarnik na 220 stopni, grzanie gora-dol.\n'
                '6. Skladniki powinny miec temperature pokojowa (ale 15-20 min z lodowki tez wystarczy).\n'
                '7. Do miski dodajemy serki Philadelphia (750-800 g), serki puszyste (300 g), cukier bialy (190 g), cukier z prawdziwa wanilia (1 plaska lyzka) i sol (1 dosc plaska lyzeczka).\n'
                '8. Miksujemy przez minute do polaczenia sie skladnikow.\n'
                '9. Dodajemy po jednym jajku (5 sztuk). Miksujemy po dodaniu kazdego przez okolo 15 sekund.\n'
                '10. Wlewamy smietanke kremowke 30% (400 ml) i miksujemy przez 10-20 sekund.\n\n'
                'Pieczenie:\n'
                '11. Mase serowa wylewamy na ciasteczkowy spod.\n'
                '12. Pieczemy przez okolo 35 minut w 220 stopniach.\n'
                '13. Po tym czasie zostawiamy sernik w zamknietym, wylaczonym piekarniku przez 15 minut.\n'
                '14. Studzimy przy uchylonych drzwiczkach (lub od razu wyciagamy z piekarnika).\n'
                '15. Z wierzchu moze byc przypalony — to normalne dla sernika baskijskiego.\n'
                '16. Po wyjciu z piekarnika moze wygladac jakby byl niedopieczony i telepac sie jak galareta — tak ma byc.\n'
                '17. Po calkowitym wystygnieciu wkladamy do lodowki na minimum 10 godzin.\n'
                '18. Dopiero wtedy sernik nabiera odpowiedniej konsystencji i mozemy go pokroic. Smacznego!'
            ),
            prep_time=20,
            cook_time=35,
            servings=10,
            difficulty='medium',
        )

        ingredients = [
            ('Herbatniki maslane', '130', 'g'),
            ('Maslo (do spodu)', '50', 'g'),
            ('Serki Philadelphia', '750-800', 'g'),
            ('Serki puszyste (np. Almette, Delikate)', '300', 'g'),
            ('Cukier', '190', 'g'),
            ('Cukier z prawdziwa wanilia', '1', 'lyzka'),
            ('Sol', '1', 'lyzeczka (plaska)'),
            ('Smietanka kremowka 30%', '400', 'ml'),
            ('Jajka (duze)', '5', 'szt.'),
        ]

        for name, qty, unit in ingredients:
            Ingredient.objects.create(recipe=recipe, name=name, quantity=qty, unit=unit)

        self.stdout.write(self.style.SUCCESS('Dodano: Sernik baskijski'))
