from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from recipes.models import Category, Recipe, Ingredient, Step


class Command(BaseCommand):
    help = 'Dodaje lub aktualizuje przepis: Spaghetti carbonara (2 porcje, wg Anigotuje)'

    def handle(self, *args, **options):
        user = User.objects.first()
        category, _ = Category.objects.get_or_create(
            name='Makarony',
            defaults={'slug': 'makarony', 'description': 'Dania z makaronem'},
        )

        title = 'Spaghetti carbonara (2 porcje)'
        slug = slugify(title)

        defaults = dict(
            title=title,
            author=user,
            category=category,
            description=(
                'Klasyczna wloska carbonara w wersji na 2 porcje — proporcje przeskalowane '
                'z przepisu Anigotuje (500 g makaronu / 8 zoltek dla 6 porcji). Bez smietany, '
                'bez czosnku. Sos powstaje z zoltek i sera, a kremowosc daje skrobia z wody '
                'po makaronie. Klucz: dodawaj sos do makaronu z dala od ognia, zeby zoltka '
                'sie nie scieli.'
            ),
            prep_time=10,
            cook_time=15,
            servings=2,
            difficulty='medium',
            is_published=True,
        )

        recipe, created = Recipe.objects.update_or_create(slug=slug, defaults=defaults)

        # Skalowanie z 6 porcji (500 g makaronu) na 2 porcje: dzielimy przez 3.
        # 500/3 ~ 165-170 g; 300/3 = 100 g; 8/3 ~ 3 zoltka; 100/3 ~ 35 g sera.
        ingredients = [
            # --- Boczek ---
            ('Guanciale, pancetta lub surowy boczek', '100', 'g'),
            # --- Makaron ---
            ('Spaghetti (n.5)', '170', 'g'),
            ('Woda do gotowania makaronu', '~1.7', 'L'),
            ('Sol do wody', '', 'do smaku'),
            # --- Sos jajeczno-serowy ---
            ('Zoltka (lub 2 zoltka + 1 cale jajko)', '3', 'szt.'),
            ('Pecorino Romano lub Parmigiano Reggiano (drobno starty)', '35', 'g'),
            ('Swiezo zmielony czarny pieprz', '', 'do smaku'),
        ]

        steps = [
            (
                'Boczek\n'
                '- Pokroj guanciale/pancette/boczek w kosteczke (ok. 1 cm).\n'
                '- Wyloz na sucha, zimna patelnie i wlacz maly/sredni ogien.\n'
                '- Smaz powoli, az wytopi sie tluszcz, a kawalki sie zrumienia (ok. 10-15 min).\n'
                '- Zdejmij z ognia, zostaw na patelni razem z wytopionym tluszczem.'
            ),
            (
                'Sos jajeczno-serowy\n'
                '- W misce roztrzep 3 zoltka (lub 2 zoltka + 1 cale jajko).\n'
                '- Dodaj 35 g drobno startego pecorino/parmezanu i sporo swiezo zmielonego pieprzu.\n'
                '- Wymieszaj na gladka, gesta paste. Jesli boczek byl niesolony, dodaj szczypte soli.'
            ),
            (
                'Makaron\n'
                '- Zagotuj ok. 1.7 L wody, osol (ok. 1 plaska lyzka soli).\n'
                '- Wrzuc 170 g spaghetti, gotuj al dente wedlug czasu na opakowaniu (zwykle 8-10 min).\n'
                '- Przed odcedzeniem zachowaj 1 kubek (ok. 200 ml) wody z gotowania makaronu — bedzie potrzebna do emulsji.'
            ),
            (
                'Laczenie\n'
                '- Patelnia z boczkiem MUSI byc zdjeta z ognia (zoltka scinaja sie powyzej ~65 stopni).\n'
                '- Przelozyc odsaczony makaron na patelnie z boczkiem, energicznie wymieszaj, zeby ciagle nitki oblepily sie tluszczem.\n'
                '- Wlej sos jajeczno-serowy, dolej 2-3 lyzki goracej wody z makaronu i intensywnie mieszaj.\n'
                '- Dolewaj woda po lyzce, az sos zwiaze sie w jedwabista emulsje (a nie omlet).'
            ),
            (
                'Podanie\n'
                '- Naloz od razu na podgrzane talerze.\n'
                '- Posyp dodatkowo serem i grubo mielonym pieprzem.\n'
                '- Jedz natychmiast — carbonara nie czeka.'
            ),
        ]

        recipe.instructions = '\n\n'.join(
            f'{i}. {t}' for i, t in enumerate(steps, start=1)
        )
        recipe.save(update_fields=['instructions'])

        recipe.ingredients.all().delete()
        recipe.steps.all().delete()

        for name, qty, unit in ingredients:
            Ingredient.objects.create(recipe=recipe, name=name, quantity=qty, unit=unit)
        for order, text in enumerate(steps, start=1):
            Step.objects.create(recipe=recipe, order=order, text=text)

        verb = 'Dodano' if created else 'Zaktualizowano'
        self.stdout.write(self.style.SUCCESS(
            f'{verb}: {title} ({len(ingredients)} skladnikow, {len(steps)} krokow)'
        ))
