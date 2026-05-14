from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from recipes.models import Category, Recipe, Ingredient, Step


class Command(BaseCommand):
    help = 'Dodaje przepis: Drozdzowki z budyniem (wierzbicka_kinga)'

    def handle(self, *args, **options):
        user = User.objects.first()
        desery, _ = Category.objects.get_or_create(
            name='Desery i wypieki',
            defaults={'slug': 'desery-i-wypieki', 'description': 'Ciasta, desery i wypieki'},
        )

        title = 'Drozdzowki z budyniem'
        slug = slugify(title)
        if Recipe.objects.filter(slug=slug).exists():
            self.stdout.write(f'{title} juz istnieje, pomijam.')
            return

        steps_text = [
            'Zaczyn: do kubka wlej 5 lyzek cieplego mleka.',
            'Dodaj drozdze, 1 lyzke cukru i 1 lyzke maki.',
            'Wymieszaj i odstaw na 10-15 minut, az zaczyn zacznie sie pienic.',
            'Ciasto: wszystkie pozostale skladniki (oprocz nadzienia i kruszonki) wraz z rozczynem wlej do miski. Wyrabiaj okolo 8-10 minut, az ciasto bedzie gladkie i elastyczne.',
            'Wyrastanie: przykryj miske sciereczka i odstaw w cieple miejsce na okolo 1 godzine, az ciasto podwoi objetosc.',
            'Budyn: ugotuj budyn z 500 ml mleka (zamiast 750 ml, zeby byl gesty). Odstaw do przestygniecia.',
            'Wyrosniete ciasto podziel na 8-9 kawalkow. Uformuj kulki i lekko je splaszcz.',
            'Na srodku kazdej kulki zrob wglebienie (np. dnem szklanki). Boki buleczek posmaruj roztrzepanym jajkiem.',
            'W kazde wglebienie naloz duza lyzke budyniu.',
            'Kruszonka: wymieszaj palcami 50 g maki pszennej, 30 g cukru i 30 g masla, az powstana grudki. Obsyp kruszonka drozdzowki.',
            'Piecz w 180 stopniach (gora-dol) okolo 18-20 minut, az beda zlociste.',
        ]

        instructions = '\n'.join(f'{i}. {t}' for i, t in enumerate(steps_text, start=1))

        recipe = Recipe.objects.create(
            title=title,
            slug=slug,
            author=user,
            category=desery,
            description='Pulchne drozdzowki z gestym budyniem waniliowym i chrupiaca kruszonka. Przepis od @wierzbicka_kinga.',
            instructions=instructions,
            prep_time=40,
            cook_time=20,
            servings=9,
            difficulty='medium',
            is_published=True,
        )

        ingredients = [
            # Ciasto
            ('Cieple mleko (do ciasta)', '240', 'ml'),
            ('Smietana 18%', '2-3', 'lyzki'),
            ('Cukier', '5', 'lyzek'),
            ('Sol', '', 'szczypta'),
            ('Swieze drozdze', '25', 'g'),
            ('Duze jajko', '1', 'szt.'),
            ('Maka pszenna', '450', 'g'),
            ('Roztopione maslo (lekko przestudzone)', '65', 'g'),
            ('Cukier waniliowy', '1', 'lyzeczka'),
            # Nadzienie
            ('Budyn waniliowy (opakowanie)', '1', 'szt.'),
            ('Mleko (do budyniu)', '500', 'ml'),
            # Kruszonka
            ('Maka pszenna (kruszonka)', '50', 'g'),
            ('Cukier (kruszonka)', '30', 'g'),
            ('Maslo (kruszonka)', '30', 'g'),
            # Do smarowania
            ('Roztrzepane jajko do smarowania', '', 'do smaku'),
        ]
        for name, qty, unit in ingredients:
            Ingredient.objects.create(recipe=recipe, name=name, quantity=qty, unit=unit)

        for order, text in enumerate(steps_text, start=1):
            Step.objects.create(recipe=recipe, order=order, text=text)

        self.stdout.write(self.style.SUCCESS(
            f'Dodano: {title} ({len(ingredients)} skladnikow, {len(steps_text)} krokow)'
        ))
