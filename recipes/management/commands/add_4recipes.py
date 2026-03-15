from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from recipes.models import Category, Recipe, Ingredient


class Command(BaseCommand):
    help = 'Dodaje faworki, tarte z jablkami, zupe tajska i koncentrat bulionu'

    def handle(self, *args, **options):
        user = User.objects.first()
        desery, _ = Category.objects.get_or_create(
            name='Desery i wypieki',
            defaults={'slug': 'desery-i-wypieki'},
        )
        dania, _ = Category.objects.get_or_create(
            name='Dania główne',
            defaults={'slug': 'dania-glowne'},
        )
        # Nowa kategoria dla koncentratu
        inne, _ = Category.objects.get_or_create(
            name='Inne',
            defaults={'slug': 'inne', 'description': 'Przetwory, koncentraty i inne'},
        )

        recipes = [
            {
                'title': 'Faworki',
                'category': desery,
                'description': 'Chrupiace faworki (chrusciki) smazone w glebokim oleju, oprószone cukrem pudrem. Klasyczny polski przysmak na tlusty czwartek.',
                'instructions': (
                    '1. Make pszenna (200 g) przesiac na stolnice.\n'
                    '2. Dodac 3 zoltka, kwasna smietane 18% (80 g), spirytus rektyfikowany 96% (1 lyzka), wodke (2 lyzki) i szczypte soli.\n'
                    '3. Zagniesc gladkie, elastyczne ciasto. Im dluzej wyrabiasz, tym lepsze faworki.\n'
                    '4. Ciasto rozwalkuj bardzo cienko (1-2 mm) na podsypanej maka stolnicy.\n'
                    '5. Pokroj na paski ok. 3-4 cm szerokosci i 10-12 cm dlugosci.\n'
                    '6. W srodku kazdego paska zrob naciecie i przeciagnij przez nie jeden koniec — powstanie charakterystyczny ksztalt.\n'
                    '7. Rozgrzej olej (min. 800 ml) do 170-180 stopni.\n'
                    '8. Smaz faworki po kilka sztuk na raz, ok. 30-40 sekund z kazdej strony az beda zlote.\n'
                    '9. Odkladaj na papierowy recznik.\n'
                    '10. Oprosz obficie cukrem pudrem. Smacznego!'
                ),
                'prep_time': 30,
                'cook_time': 20,
                'servings': 6,
                'difficulty': 'medium',
                'ingredients': [
                    ('Maka pszenna', '200', 'g'),
                    ('Zoltka', '3', 'szt.'),
                    ('Kwasna smietana 18%', '80', 'g'),
                    ('Spirytus rektyfikowany 96%', '1', 'lyzka'),
                    ('Wodka', '2', 'lyzki'),
                    ('Sol', '1', 'szczypta'),
                    ('Olej do glebokiego smazenia', '800', 'ml (min.)'),
                    ('Cukier puder', '', 'do oproszenia'),
                    ('Maka pszenna', '', 'do oproszenia'),
                ],
            },
            {
                'title': 'Tarta z jablkami',
                'category': desery,
                'description': 'Domowa tarta z jablkami na kruchym ciescie z budyniowa masa i rodzynkami. Przepis Kasi.',
                'instructions': (
                    '1. Make (1,5 szklanki) wymieszana z proszkiem do pieczenia przesiac na stolnice.\n'
                    '2. Posrodku zrobic wglebienie, wlac do niego ubite jajko, wsypac 5 lyzek cukru i dodac starta na wiorki Kasie (1 lyzke zostawic). Zimnymi rekami szybko zagniesc ciasto, owinac w folie i wlozyc na pol godziny do lodowki.\n'
                    '3. Rodzynki (10 dkg) przebrac, umyc, osaczyc, polac rumem (4 lyzki).\n'
                    '4. Jablka obrac, przekroic na polowki, wydrazyc gniazda nasienne.\n'
                    '5. Tortownice lub forme do tarty o srednicy 26 cm posmarowac Kasia.\n'
                    '6. Ciasto rozwalkować i wylepic nim forme, wysoko podwijajac brzegi.\n'
                    '7. Na ciescie ukladac ciasno obok siebie wydrazone polowki jablek. Ich srodki napelnic namoczonymi w rumie rodzynkami.\n'
                    '8. Budyn rozmieszac z 1/3 smietanki. Pozostala smietanke zagotowac razem z reszta cukru, cukrem wanilinowym i lyzka Kasi. Wlac budyn, ponownie zagotowac i od razu zalac jablka.\n'
                    '9. Piec 60-70 minut w piekarniku nagrzanym do 180 stopni.\n'
                    '10. Ciasto pozostawic w formie na 24 godziny.'
                ),
                'prep_time': 40,
                'cook_time': 70,
                'servings': 8,
                'difficulty': 'medium',
                'ingredients': [
                    ('Maka pszenna', '1,5', 'szklanki'),
                    ('Cukier', '1', 'szklanka (6 lyzek)'),
                    ('Maslo/margaryna (Kasia)', '9', 'lyzek'),
                    ('Smietanka kremowka', '0,5', 'litra'),
                    ('Budyn waniliowy', '1', 'opakowanie'),
                    ('Cukier wanilinowy', '1', 'opakowanie'),
                    ('Rum', '4', 'lyzki'),
                    ('Rodzynki', '10', 'dkg'),
                    ('Proszek do pieczenia', '1', 'lyzeczka'),
                    ('Jajko', '1', 'szt.'),
                    ('Jablka (male, slodkie)', '', 'kilka sztuk'),
                ],
            },
            {
                'title': 'Zupa tajska z batatami',
                'category': dania,
                'description': 'Aromatyczna zupa tajska z kurczakiem, batatami, mleczkiem kokosowym i pasta curry. Mozna dodac inne warzywa np. papryke, cebule, cukinie.',
                'instructions': (
                    '1. Kurczaka (500 g) pokroj na 1,5 cm kawalki.\n'
                    '2. Bataty (400 g) pokroj na 1,5-2 cm kawalki.\n'
                    '3. Do garnka wloz kurczaka, bataty, kolendre (20-25 g), paste curry (30-40 g), mleczko kokosowe (600 g), wode (100-150 g), sol (1-2 lyzeczki) i pieprz (3/4 - 1,5 lyzeczki).\n'
                    '4. Mozna dodac inne warzywa: papryke, cebule, cukinie.\n'
                    '5. Gotuj 20 minut na wolnym ogniu.\n'
                    '6. Podawaj od razu, udekorowana swieza kolendra. Smacznego!'
                ),
                'prep_time': 10,
                'cook_time': 20,
                'servings': 3,
                'difficulty': 'easy',
                'ingredients': [
                    ('Piers z kurczaka (bez kosci)', '500', 'g'),
                    ('Bataty', '400', 'g'),
                    ('Kolendra swieza', '20-25', 'g'),
                    ('Czerwona pasta curry', '30-40', 'g'),
                    ('Mleczko kokosowe', '600', 'g'),
                    ('Woda', '100-150', 'g'),
                    ('Sol', '1-2', 'lyzeczki'),
                    ('Pieprz czarny mielony', '3/4-1,5', 'lyzeczki'),
                    ('Warzywa (papryka, cebula, cukinia)', '', 'opcjonalnie'),
                ],
            },
            {
                'title': 'Koncentrat bulionu warzywnego',
                'category': inne,
                'description': 'Domowy koncentrat bulionu warzywnego — zdrowa alternatywa dla kostek bulionowych. Przechowywac w lodowce do 3 miesiecy lub zamrazac w kostkach do 6 miesiecy.',
                'instructions': (
                    '1. Seler naciowy (200 g), marchewke (250 g), cebule (100 g), pomidora (100 g), cukinie (150 g), zabek czosnku, grzyby (50 g), lisc laurowy, mieszane ziola (6 galazek bazylii, szalwii, rozmarynu — tylko liscie) i natke pietruszki (4 galazki) wlozyc do naczynia miksujacego.\n'
                    '2. Rozdrobnic przy pomocy kopystki 10 sekund. Skladniki zgarnac kopystka ze scianek na dno naczynia.\n'
                    '3. Dodac sol gruboziarnista (120 g), biale wino wytrawne (30 g) i oliwe z oliwek (1 lyzka).\n'
                    '4. Odparowywac 25-30 minut az koncentrat bedzie mial konsystencje gestej pasty.\n'
                    '5. Dodac rozdrobniony parmezan, zmiksowac 1 minute stopniowo zwiekszajac obroty.\n'
                    '6. Przelozyc do wyparzonego, szczelnie zamykanego sloika.\n'
                    '7. Pozostawic do ostygniecia lub schlodzic w lodowce.\n'
                    '8. Przechowywac w lodowce do 3 miesiecy lub przelozyc do foremki do lodu i zamrazac w kostkach do 6 miesiecy.'
                ),
                'prep_time': 15,
                'cook_time': 30,
                'servings': 20,
                'difficulty': 'easy',
                'ingredients': [
                    ('Seler naciowy', '200', 'g'),
                    ('Marchewka', '250', 'g'),
                    ('Cebula', '100', 'g'),
                    ('Pomidor', '100', 'g'),
                    ('Cukinia', '150', 'g'),
                    ('Czosnek', '1', 'zabek'),
                    ('Grzyby swieze', '50', 'g'),
                    ('Lisc laurowy suszony', '1', 'szt. (opcjonalnie)'),
                    ('Mieszane ziola swieze', '6', 'galazek'),
                    ('Natka pietruszki', '4', 'galazki'),
                    ('Sol gruboziarnista', '120', 'g'),
                    ('Biale wino wytrawne', '30', 'g'),
                    ('Oliwa z oliwek', '1', 'lyzka'),
                ],
            },
        ]

        for data in recipes:
            slug = slugify(data['title'])
            if Recipe.objects.filter(slug=slug).exists():
                self.stdout.write(f'  "{data["title"]}" juz istnieje, pomijam.')
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

        self.stdout.write(self.style.SUCCESS('Gotowe!'))
