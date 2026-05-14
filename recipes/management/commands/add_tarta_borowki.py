from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from recipes.models import Category, Recipe, Ingredient, Step


class Command(BaseCommand):
    help = 'Dodaje lub aktualizuje przepis: Tarta z borowkami i mascarpone'

    def handle(self, *args, **options):
        user = User.objects.first()
        desery, _ = Category.objects.get_or_create(
            name='Desery i wypieki',
            defaults={'slug': 'desery-i-wypieki', 'description': 'Ciasta, desery i wypieki'},
        )

        title = 'Tarta z borowkami i mascarpone'
        slug = slugify(title)

        defaults = dict(
            title=title,
            author=user,
            category=desery,
            description=(
                'Kruche ciasto, jedwabisty krem z mascarpone i bialej czekolady z musem '
                'z borowek, na wierzchu garsc swiezych owocow. Forma 24-26 cm. '
                'Po zlozeniu schladza sie minimum 3 godziny (najlepiej cala noc).'
            ),
            prep_time=30,
            cook_time=25,
            servings=8,
            difficulty='medium',
            is_published=True,
        )

        recipe, created = Recipe.objects.update_or_create(slug=slug, defaults=defaults)

        # Etapy nie wspoldziela skladnikow (mus borowkowy 200 g i borowki do dekoracji
        # 100-150 g sa wskazane jako osobne ilosci, tak samo cukier puder spod vs krem).
        ingredients = [
            # --- Kruche ciasto (spod) ---
            ('Maka pszenna (spod)', '200', 'g'),
            ('Zimne maslo (spod)', '100', 'g'),
            ('Cukier pudru (spod)', '50', 'g'),
            ('Zoltko (spod)', '1', 'szt.'),
            ('Zimna woda (spod)', '1-2', 'lyzki (~15-30 ml)'),
            # --- Krem ---
            ('Mascarpone (krem)', '250', 'g'),
            ('Biala czekolada (krem)', '100', 'g'),
            ('Smietanka 30% lub 36% (krem)', '200', 'ml'),
            ('Borowki na mus (krem)', '200', 'g'),
            ('Cukier pudru (krem, opcjonalnie)', '1-2', 'lyzki (~12-24 g)'),
            # --- Dekoracja ---
            ('Swieze borowki (dekoracja)', '100-150', 'g'),
        ]

        steps = [
            (
                'Spod\n'
                '- Zagniec szybko ciasto z maki, masla, cukru pudru, zoltka i wody.\n'
                '- Schlodz 30 minut w lodowce.\n'
                '- Wylep forme do tarty (24-26 cm).\n'
                '- Naklusz widelcem.\n'
                '- Piecz 20-25 minut w 180 stopniach, az spod bedzie zloty.\n'
                '- Wystudz.'
            ),
            (
                'Borowki\n'
                '- 200 g borowek zmiksuj na gladki mus.\n'
                '- Opcjonalnie przetrzyj przez sitko, jesli chcesz idealnie gladki krem.'
            ),
            (
                'Biala czekolada\n'
                '- Rozpusc biala czekolade w kapieli wodnej lub w mikrofalowce.\n'
                '- Odstaw do lekkiego przestudzenia.'
            ),
            (
                'Krem\n'
                '- Ubij smietanke na polsztywno.\n'
                '- Dodaj mascarpone i krotko zmiksuj.\n'
                '- Wlej roztopiona biala czekolade.\n'
                '- Dodaj mus z borowek (opcjonalnie z cukrem pudrem).\n'
                '- Delikatnie wymieszaj do uzyskania gladkiej masy.'
            ),
            (
                'Skladanie\n'
                '- Krem wyloz na wystudzony spod.\n'
                '- Udekoruj swiezymi borowkami.\n'
                '- Schladzaj minimum 3 godziny, najlepiej cala noc.'
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
