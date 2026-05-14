from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from recipes.models import Category, Recipe, Ingredient, Step


class Command(BaseCommand):
    help = 'Dodaje lub aktualizuje przepis: Drozdzowki z budyniem (wierzbicka_kinga)'

    def handle(self, *args, **options):
        user = User.objects.first()
        desery, _ = Category.objects.get_or_create(
            name='Desery i wypieki',
            defaults={'slug': 'desery-i-wypieki', 'description': 'Ciasta, desery i wypieki'},
        )

        title = 'Drozdzowki z budyniem'
        slug = slugify(title)

        defaults = dict(
            title=title,
            author=user,
            category=desery,
            description='Pulchne drozdzowki z gestym budyniem waniliowym i chrupiaca kruszonka. Wychodzi 8-9 sztuk. Przepis od @wierzbicka_kinga.',
            prep_time=40,
            cook_time=20,
            servings=9,
            difficulty='medium',
            is_published=True,
        )

        recipe, created = Recipe.objects.update_or_create(slug=slug, defaults=defaults)

        ingredients = [
            # --- Ciasto (8-9 sztuk) ---
            ('Cieple mleko (do ciasta)', '240', 'ml'),
            ('Smietana 18%', '2-3', 'lyzki'),
            ('Cukier (do ciasta)', '5', 'lyzek'),
            ('Sol', '', 'szczypta'),
            ('Swieze drozdze', '25', 'g'),
            ('Duze jajko (do ciasta)', '1', 'szt.'),
            ('Maka pszenna (do ciasta)', '450', 'g'),
            ('Roztopione maslo (lekko przestudzone)', '65', 'g'),
            ('Cukier waniliowy', '1', 'lyzeczka'),
            # --- Nadzienie budyniowe ---
            ('Budyn waniliowy (opakowanie)', '1', 'szt.'),
            ('Mleko (do budyniu)', '500', 'ml'),
            # --- Kruszonka ---
            ('Maka pszenna (kruszonka)', '50', 'g'),
            ('Cukier (kruszonka)', '30', 'g'),
            ('Maslo (kruszonka)', '30', 'g'),
            # --- Dodatkowo ---
            ('Jajko do posmarowania brzegow', '1', 'szt.'),
        ]

        steps = [
            (
                'Rozczyn\n'
                '- Do kubka wlej 5 lyzek cieplego mleka.\n'
                '- Dodaj: pokruszone drozdze, 1 lyzke cukru i 1 lyzke maki.\n'
                '- Wymieszaj i odstaw na 10-15 minut, az rozczyn zacznie sie pienic.'
            ),
            (
                'Ciasto drozdzowe\n'
                '- Do duzej miski wsyp make.\n'
                '- Dodaj: pozostale mleko, smietane, cukier, sol, cukier waniliowy, jajko, wyrosniety rozczyn.\n'
                '- Wyrabiaj przez kilka minut.\n'
                '- Dodaj roztopione maslo.\n'
                '- Wyrabiaj dalej 8-10 minut, az ciasto bedzie gladkie i elastyczne.'
            ),
            (
                'Wyrastanie\n'
                '- Przykryj miske sciereczka.\n'
                '- Odstaw w cieple miejsce na okolo 1 godzine, az ciasto podwoi objetosc.'
            ),
            (
                'Budyn\n'
                '- Ugotuj budyn zgodnie z instrukcja na opakowaniu, uzywajac tylko 500 ml mleka (zamiast 750 ml, by byl gestszy i nie wyplynal podczas pieczenia).\n'
                '- Odstaw do calkowitego przestudzenia.'
            ),
            (
                'Kruszonka\n'
                '- Polacz make, cukier i maslo.\n'
                '- Rozetrzyj palcami, az powstanie kruszonka.'
            ),
            (
                'Formowanie drozdzowek\n'
                '- Wyrosniete ciasto podziel na 8-9 rownych czesci.\n'
                '- Uformuj kulki i lekko je splaszcz.\n'
                '- Na srodku kazdej buleczki zrob wglebienie (np. dnem szklanki).\n'
                '- Boki posmaruj roztrzepanym jajkiem.\n'
                '- Naloz do srodka duza lyzke budyniu.\n'
                '- Posyp kruszonka.'
            ),
            (
                'Pieczenie\n'
                '- Piecz w piekarniku nagrzanym do 180 stopni (gora-dol).\n'
                '- Czas pieczenia: 18-20 minut, az drozdzowki beda zlociste.'
            ),
        ]

        # Mirror steps into the legacy `instructions` text field
        recipe.instructions = '\n\n'.join(
            f'{i}. {text}' for i, text in enumerate(steps, start=1)
        )
        recipe.save(update_fields=['instructions'])

        # Wipe old ingredients + steps, then recreate from spec (idempotent)
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
