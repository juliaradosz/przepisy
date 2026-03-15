from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Ingredient, Category
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Import 7 missing recipes from PythonAnywhere site'

    def handle(self, *args, **options):
        user = User.objects.first()

        recipes_data = [
            {
                'title': 'Krówka',
                'category': 'Desery i wypieki',
                'description': '',
                'instructions': (
                    '1. Mleko skondensowane slodzone gotowac 3h.\n'
                    '2. Zoltka, cukier i maslo utrzec.\n'
                    '3. Dodac make z proszkiem do pieczenia.\n'
                    '4. Podzielic na 2 rowne czesci.\n'
                    '5. Piec kazda z nich ~ 15 min.\n'
                    '6. Po wystygnięciu jedna czesc posmarowac polowa mleka.\n'
                    '7. Ubic 1/2 litra kremowki + 3 lyzeczki zelatyny + cukier.\n'
                    '8. Polozyc na ciasto, na to druga czesc ciasta + reszte mleka.\n'
                    '9. Posypac drobno posiekanymi orzechami wloskimi.'
                ),
                'ingredients': [
                    {'name': 'Mleko skondensowane slodzone', 'quantity': '', 'unit': ''},
                    {'name': 'Zoltka', 'quantity': '5', 'unit': 'szt.'},
                    {'name': 'Maka tortowa', 'quantity': '3', 'unit': 'szklanki'},
                    {'name': 'Maslo', 'quantity': '1', 'unit': 'szt.'},
                    {'name': 'Proszek do pieczenia', 'quantity': '2', 'unit': 'lyzeczki'},
                    {'name': 'Cukier puder', 'quantity': '1/2', 'unit': 'szklanki'},
                    {'name': 'Zelatyna', 'quantity': '3', 'unit': 'lyzeczki'},
                ],
            },
            {
                'title': 'Salatka warstwowa',
                'category': 'Salatki',
                'description': '',
                'instructions': '',
                'ingredients': [
                    {'name': 'Kukurydza', 'quantity': '1', 'unit': 'puszka'},
                    {'name': 'Szynka', 'quantity': '', 'unit': ''},
                    {'name': 'Jajka', 'quantity': '', 'unit': ''},
                    {'name': 'Ananasy', 'quantity': '', 'unit': ''},
                    {'name': 'Seler w sloiku', 'quantity': '', 'unit': ''},
                    {'name': 'Majonez', 'quantity': '', 'unit': ''},
                    {'name': 'Por', 'quantity': '', 'unit': ''},
                    {'name': 'Musztarda', 'quantity': '', 'unit': ''},
                ],
            },
            {
                'title': 'Sernik pieczony',
                'category': 'Desery i wypieki',
                'description': '',
                'instructions': (
                    '1. Ser, maslo, cukier i zoltka razem do miksera.\n'
                    '2. Dodac 2 budynie i ubita piane z bialek.\n'
                    '3. Piec 50 min w 180 stopniach.'
                ),
                'ingredients': [
                    {'name': 'Twarog', 'quantity': '', 'unit': ''},
                    {'name': 'Cukier', 'quantity': '', 'unit': ''},
                    {'name': 'Maslo', 'quantity': '', 'unit': ''},
                    {'name': 'Budyn', 'quantity': '2', 'unit': 'szt.'},
                    {'name': 'Jajka', 'quantity': '', 'unit': ''},
                ],
            },
            {
                'title': 'Ciastka owsiane',
                'category': 'Ciastka',
                'description': '',
                'instructions': '',
                'ingredients': [
                    {'name': 'Maka pszenna razowa', 'quantity': '120', 'unit': 'g'},
                    {'name': 'Maka pszenna', 'quantity': '80', 'unit': 'g'},
                    {'name': 'Maslo', 'quantity': '100', 'unit': 'g'},
                    {'name': 'Mielone orzechy wloskie', 'quantity': '50', 'unit': 'g'},
                    {'name': 'Brazowy cukier', 'quantity': '75', 'unit': 'g'},
                    {'name': 'Soda oczyszczona', 'quantity': '1/4', 'unit': 'lyzeczki'},
                    {'name': 'Proszek do pieczenia', 'quantity': '1/4', 'unit': 'lyzeczki'},
                    {'name': 'Jajko', 'quantity': '1', 'unit': 'szt.'},
                    {'name': 'Sol', 'quantity': '', 'unit': 'szczypta'},
                ],
            },
            {
                'title': 'Makaron z pieczonym sosem pomidorowym',
                'category': 'Dania główne',
                'description': 'Spaghetti z pieczonym sosem pomidorowym z serkiem wiejskim i parmezanem. Proste, zdrowe i pyszne!',
                'servings': 3,
                'instructions': (
                    '1. Pomidorki koktajlowe umyj, a cebule pokroj na kilka kawalkow. Wyloz warzywa na blaszke wylozoną papierem do pieczenia.\n'
                    '2. Polej calosc oliwa. Z czosnku utnij gore, aby zabki sie odslonily. Polej go rowniez oliwa i wyloz obok warzyw. Posyp calosc sola i pieprzem. Wstaw do piekarnika rozgrzanego do 180 stopni, na 30-40 minut (termoobieg).\n'
                    '3. Gdy warzywa sie pieka, ugotuj makaron wedlug instrukcji na opakowaniu.\n'
                    '4. Po upieczeniu warzyw, w blenderze umiesc pomidory, czosnek, cebule, serek wiejski, starty parmezan, sol oraz pieprz. Zblenduj na jednolita mase. Sprobuj i dopraw ewentualnie do smaku sola/pieprzem.\n'
                    '5. Sos wylej na patelnie i wymieszaj z makaronem. Posyp (najlepiej swiezym) pieprzem.'
                ),
                'ingredients': [
                    {'name': 'Pomidorki koktajlowe', 'quantity': '500', 'unit': 'g'},
                    {'name': 'Cebula', 'quantity': '1', 'unit': 'szt. (100-120 g)'},
                    {'name': 'Czosnek', 'quantity': '1', 'unit': 'glowka'},
                    {'name': 'Oliwa z oliwek', 'quantity': '15', 'unit': 'g'},
                    {'name': 'Parmezan', 'quantity': '60', 'unit': 'g'},
                    {'name': 'Sol', 'quantity': '2-3', 'unit': 'szczypty'},
                    {'name': 'Pieprz', 'quantity': '2-3', 'unit': 'szczypty'},
                    {'name': 'Serek wiejski (naturalny)', 'quantity': '200', 'unit': 'g'},
                    {'name': 'Makaron spaghetti', 'quantity': '240', 'unit': 'g'},
                ],
            },
            {
                'title': 'Cynamonki',
                'category': 'Desery i wypieki',
                'description': 'Pyszne drozdzowe buleczki cynamonowe z nadzieniem z brazowego cukru i cynamonu, polane kremem smietankowym.',
                'servings': 12,
                'instructions': (
                    'Ciasto:\n'
                    '1. Z podanych skladnikow odejmujemy 50 ml cieplego mleka, 2 lyzki maki, lyzke cukru i drozdze - wszystko mieszamy i odstawiamy az rozczyn zacznie pracowac (10 min).\n'
                    '2. Pozostale skladniki wkladamy do duzej miski, dodajemy rozczyn i wszystko wyrabiamy robotem planetarnym badz recznie przez 10 min.\n'
                    '3. Ciasto moze sie troche kleic - nie martw sie, bedzie dobrze :)\n'
                    '4. Odstawiamy na godzine w cieple miejsce.\n\n'
                    'Nadzienie:\n'
                    '5. W tym czasie robimy nadzienie: maslo, cynamon, cukier z wanilia i brazowy cukier - wszystko rozcieramy widelcem na gladka mase.\n\n'
                    'Formowanie:\n'
                    '6. Gdy ciasto wyrosnie, walkujemy je na prostokat. Nakladamy nadzienie, zwijamy w rulon, dzielimy na 9 wiekszych lub 12 mniejszych rolsow. Najlepiej przy pomocy nitki.\n'
                    '7. Buleczki ukladamy na blaszce, polewamy ciepla smietanka 30% i wstawiamy do piekarnika 180 stopni gora-dol na jakies 25 min (az zrobia sie rumiane).\n\n'
                    'Krem smietankowy (opcjonalnie):\n'
                    '8. Maslo z cukrem pudru ubijamy az zrobi sie puszyste, dodajemy serek kanapkowy i sok z limonki, wszystko miksujemy na gladka mase.\n'
                    '9. Po wystudzeniu buleczek smarujemy kremem smietankowym.'
                ),
                'ingredients': [
                    {'name': 'Maka pszenna', 'quantity': '550', 'unit': 'g'},
                    {'name': 'Cieple mleko', 'quantity': '200', 'unit': 'ml'},
                    {'name': 'Drozdze', 'quantity': '20', 'unit': 'g'},
                    {'name': 'Roztopione maslo', 'quantity': '90', 'unit': 'g'},
                    {'name': 'Kwasna smietana 18%', 'quantity': '120', 'unit': 'g'},
                    {'name': 'Jaja', 'quantity': '2', 'unit': 'szt.'},
                    {'name': 'Cukier', 'quantity': '60', 'unit': 'g'},
                    {'name': 'Smietanka 30% (do polania)', 'quantity': '100', 'unit': 'ml'},
                    {'name': 'Miekkie maslo (nadzienie)', 'quantity': '100', 'unit': 'g'},
                    {'name': 'Cynamon', 'quantity': '2', 'unit': 'kopiaste lyzki'},
                    {'name': 'Cukier z wanilia', 'quantity': '1', 'unit': 'lyzka'},
                    {'name': 'Brazowy cukier', 'quantity': '80', 'unit': 'g'},
                    {'name': 'Serek kanapkowy smietankowy (krem)', 'quantity': '200', 'unit': 'g'},
                    {'name': 'Miekkie maslo (krem)', 'quantity': '70', 'unit': 'g'},
                    {'name': 'Cukier pudru (krem)', 'quantity': '50', 'unit': 'g'},
                    {'name': 'Sok z limonki (krem)', 'quantity': '2', 'unit': 'lyzki'},
                ],
            },
            {
                'title': 'Chrupiące gofry',
                'category': 'Desery i wypieki',
                'description': 'Przepis na chrupiace gofry - na 16 sztuk, wielkosci 10 cm x 12 cm.',
                'servings': 16,
                'instructions': (
                    '1. Zaczynamy od oddzielenia bialek od zoltek.\n'
                    '2. Nastepnie do duzej miski wsypujemy make, proszek do pieczenia, sol, cukier. Dolewamy mleko i olej oraz dodajemy zoltka.\n'
                    '3. Calosc mieszamy, ale nie ubijamy. Skladniki mozna wrzucic do blendera, mozna uzyc rowniez blendera recznego, wazne jest aby nie ubijac ciasta, a tylko je wymieszac.\n'
                    '4. Jesli nie macie blendera, ciasto mozna wymieszac recznie za pomoca trzepaczki lub np. widelca (bedzie nieco trudniej, ale da sie).\n'
                    '5. Gdy ciasto bedzie juz gladkie i jednolite zaczynamy nagrzewac gofrownice.\n'
                    '6. W miedzyczasie ubijamy jeszcze 2 bialka (pozostale z zoltek) na sztywna piane i ubita piane z bialek dodajemy do ciasta, delikatnie mieszajac.\n'
                    '7. Gdy ciasto jest gotowe nabieramy lyzka i wylewamy na rozgrzana forme do gofrow.\n'
                    '8. Gofry pieczemy przez 3 minuty (lub dluzej, w zaleznosci od mocy gofrownicy).\n'
                    '9. Po upieczeniu ostroznie zdejmujemy na talerz i od razu zjadamy z ulubionymi dodatkami.'
                ),
                'ingredients': [
                    {'name': 'Maka pszenna typu 500-550', 'quantity': '300', 'unit': 'g'},
                    {'name': 'Proszek do pieczenia', 'quantity': '5', 'unit': 'g'},
                    {'name': 'Sol', 'quantity': '2', 'unit': 'g'},
                    {'name': 'Mleko 2%', 'quantity': '500', 'unit': 'ml'},
                    {'name': 'Cukier', 'quantity': '20', 'unit': 'g'},
                    {'name': 'Olej', 'quantity': '70', 'unit': 'g'},
                    {'name': 'Jajka duze', 'quantity': '2', 'unit': 'szt.'},
                ],
            },
        ]

        added = 0
        for data in recipes_data:
            title = data['title']
            if Recipe.objects.filter(title=title).exists():
                self.stdout.write(f'  Pomijam (juz istnieje): {title}')
                continue

            cat_name = data['category']
            category, _ = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name)}
            )

            slug = slugify(title) or 'przepis'
            base_slug = slug
            counter = 1
            while Recipe.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1

            recipe = Recipe.objects.create(
                title=title,
                slug=slug,
                author=user,
                category=category,
                description=data.get('description', ''),
                instructions=data.get('instructions', ''),
                servings=data.get('servings'),
                is_published=True,
            )

            for ing in data.get('ingredients', []):
                Ingredient.objects.create(
                    recipe=recipe,
                    name=ing['name'],
                    quantity=ing.get('quantity', ''),
                    unit=ing.get('unit', ''),
                )

            added += 1
            self.stdout.write(f'  Dodano: {title}')

        self.stdout.write(self.style.SUCCESS(f'\nGotowe! Dodano {added} przepisow.'))
