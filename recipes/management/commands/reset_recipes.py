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

        user = User.objects.first()

        # Kategorie
        cat_wypieki, _ = Category.objects.get_or_create(name='Desery i wypieki', slug='desery-i-wypieki')

        # Tagi
        tag_gofry, _ = Tag.objects.get_or_create(name='gofry', slug='gofry')
        tag_slodkie, _ = Tag.objects.get_or_create(name='słodkie', slug='slodkie')
        tag_cynamon, _ = Tag.objects.get_or_create(name='cynamon', slug='cynamon')
        tag_drozdzowe, _ = Tag.objects.get_or_create(name='drożdżowe', slug='drozdzowe')

        # === Chrupiące gofry ===
        gofry = Recipe.objects.create(
            title='Chrupiące gofry',
            slug='chrupiace-gofry',
            author=user,
            category=cat_wypieki,
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
        gofry.tags.add(tag_gofry, tag_slodkie)
        for name, qty, unit in [
            ('Mąka pszenna typu 500-550', '2', 'szklanki (300 g)'),
            ('Proszek do pieczenia', '1', 'łyżeczka (5 g)'),
            ('Sól', '1', 'szczypta (2 g)'),
            ('Mleko 2%', '2', 'szklanki (500 ml)'),
            ('Cukier', '1', 'pełna łyżka (20 g)'),
            ('Olej', '1/3', 'szklanki (70 g)'),
            ('Jajka duże', '2', 'szt. (białka i żółtka oddzielnie)'),
        ]:
            Ingredient.objects.create(recipe=gofry, name=name, quantity=qty, unit=unit)
        self.stdout.write(self.style.SUCCESS('Dodano: Chrupiące gofry'))

        # === Cynamonki ===
        cynamonki = Recipe.objects.create(
            title='Cynamonki',
            slug='cynamonki',
            author=user,
            category=cat_wypieki,
            description='Pyszne drożdżowe bułeczki cynamonowe z nadzieniem z brązowego cukru i cynamonu, polane kremem śmietankowym.',
            instructions=(
                'Ciasto:\n'
                '1. Z podanych składników odejmujemy 50 ml ciepłego mleka, 2 łyżki mąki, łyżkę cukru i drożdże '
                '- wszystko mieszamy i odstawiamy aż rozczyn zacznie pracować (10 min).\n'
                '2. Pozostałe składniki wkładamy do dużej miski, dodajemy rozczyn i wszystko wyrabiamy '
                'robotem planetarnym bądź ręcznie przez 10 min.\n'
                '3. Ciasto może się trochę kleić - nie martw się, będzie dobrze :)\n'
                '4. Odstawiamy na godzinę w ciepłe miejsce.\n\n'
                'Nadzienie:\n'
                '5. W tym czasie robimy nadzienie: masło, cynamon, cukier z wanilią i brązowy cukier '
                '- wszystko rozcieramy widelcem na gładką masę.\n\n'
                'Formowanie:\n'
                '6. Gdy ciasto wyrośnie, wałkujemy je na prostokąt. Nakładamy nadzienie, '
                'zwijamy w rulon, dzielimy na 9 większych lub 12 mniejszych rolsów. '
                'Najlepiej przy pomocy nitki.\n'
                '7. Bułeczki układamy na blaszce, polewamy ciepłą śmietanką 30% i wstawiamy '
                'do piekarnika 180 stopni góra-dół na jakieś 25 min (aż zrobią się rumiane).\n\n'
                'Krem śmietankowy (opcjonalnie):\n'
                '8. Masło z cukrem pudru ubijamy aż zrobi się puszyste, dodajemy serek kanapkowy '
                'i sok z limonki, wszystko miksujemy na gładką masę.\n'
                '9. Po wystudzeniu bułeczek smarujemy kremem śmietankowym.'
            ),
            prep_time=90,
            cook_time=25,
            servings=12,
            difficulty='medium',
            is_published=True,
        )
        cynamonki.tags.add(tag_slodkie, tag_cynamon, tag_drozdzowe)

        # Składniki - ciasto
        for name, qty, unit in [
            ('Mąka pszenna', '550', 'g'),
            ('Ciepłe mleko', '200', 'ml'),
            ('Drożdże', '20', 'g'),
            ('Roztopione masło', '90', 'g'),
            ('Kwaśna śmietana 18%', '120', 'g'),
            ('Jaja', '2', 'szt.'),
            ('Cukier', '60', 'g'),
            ('Śmietanka 30% (do polania)', '100', 'ml'),
        ]:
            Ingredient.objects.create(recipe=cynamonki, name=name, quantity=qty, unit=unit)

        # Składniki - nadzienie
        for name, qty, unit in [
            ('Miękkie masło (nadzienie)', '100', 'g'),
            ('Cynamon', '2', 'kopiaste łyżki'),
            ('Cukier z wanilią', '1', 'łyżka'),
            ('Brązowy cukier', '80', 'g'),
        ]:
            Ingredient.objects.create(recipe=cynamonki, name=name, quantity=qty, unit=unit)

        # Składniki - krem
        for name, qty, unit in [
            ('Serek kanapkowy śmietankowy (krem)', '200', 'g'),
            ('Miękkie masło (krem)', '70', 'g'),
            ('Cukier pudru (krem)', '50', 'g'),
            ('Sok z limonki (krem)', '2', 'łyżki'),
        ]:
            Ingredient.objects.create(recipe=cynamonki, name=name, quantity=qty, unit=unit)

        self.stdout.write(self.style.SUCCESS('Dodano: Cynamonki'))

        # === Makaron z kurczakiem w sosie serowym ===
        cat_dania, _ = Category.objects.get_or_create(name='Dania główne', slug='dania-glowne')
        tag_szybkie, _ = Tag.objects.get_or_create(name='szybkie', slug='szybkie')
        tag_makaron, _ = Tag.objects.get_or_create(name='makaron', slug='makaron')
        tag_kurczak, _ = Tag.objects.get_or_create(name='kurczak', slug='kurczak')

        makaron = Recipe.objects.create(
            title='Makaron z kurczakiem w sosie serowym',
            slug='makaron-z-kurczakiem-w-sosie-serowym',
            author=user,
            category=cat_dania,
            description='Szybki makaron z kurczakiem w kremowym sosie serowym z parmezanem. Łatwe i smaczne!',
            instructions=(
                '1. Do kurczaka dodajemy czosnek granulowany, paprykę wędzoną oraz sól.\n'
                '2. Smażymy kurczaka na oliwie z oliwek.\n'
                '3. Gotujemy makaron.\n'
                '4. Usmażonego kurczaka przekładamy na inne naczynie.\n'
                '5. Na tej samej patelni rozpuszczamy masło, dodajemy łyżeczkę mąki, '
                'mleko (jeżeli myślisz, że dałeś dużo to znaczy, że dałeś idealnie).\n'
                '6. Można dodać czosnek (opcjonalnie).\n'
                '7. Na koniec parmezan/grana padano i wszystko wymieszać.\n'
                '8. Dodajemy makaron i kurczaka do sosu, mieszamy i podajemy.'
            ),
            prep_time=10,
            cook_time=20,
            servings=2,
            difficulty='easy',
            is_published=True,
        )
        makaron.tags.add(tag_szybkie, tag_makaron, tag_kurczak)

        for name, qty, unit in [
            ('Kurczak (pierś lub udka)', '300', 'g'),
            ('Czosnek granulowany', '1', 'łyżeczka'),
            ('Papryka wędzona', '1', 'łyżeczka'),
            ('Sól', '', 'do smaku'),
            ('Oliwa z oliwek', '2', 'łyżki'),
            ('Makaron', '200', 'g'),
            ('Masło', '1', 'łyżka'),
            ('Mąka', '1', 'łyżeczka'),
            ('Mleko', '200', 'ml'),
            ('Czosnek świeży (opcjonalnie)', '2', 'ząbki'),
            ('Parmezan lub Grana Padano', '50', 'g'),
        ]:
            Ingredient.objects.create(recipe=makaron, name=name, quantity=qty, unit=unit)

        self.stdout.write(self.style.SUCCESS('Dodano: Makaron z kurczakiem w sosie serowym'))

        # === Makaron z boczkiem w sosie serowym ===
        tag_boczek, _ = Tag.objects.get_or_create(name='boczek', slug='boczek')

        makaron_boczek = Recipe.objects.create(
            title='Makaron z boczkiem w sosie serowym',
            slug='makaron-z-boczkiem-w-sosie-serowym',
            author=user,
            category=cat_dania,
            description='Szybki makaron z boczkiem w kremowym sosie serowym z parmezanem. Łatwe i smaczne!',
            instructions=(
                '1. Boczek kroimy w kostkę lub paski, dodajemy czosnek granulowany, paprykę wędzoną oraz sól.\n'
                '2. Smażymy boczek na oliwie z oliwek aż będzie chrupiący.\n'
                '3. Gotujemy makaron.\n'
                '4. Usmażony boczek przekładamy na inne naczynie.\n'
                '5. Na tej samej patelni rozpuszczamy masło, dodajemy łyżeczkę mąki, '
                'mleko (jeżeli myślisz, że dałeś dużo to znaczy, że dałeś idealnie).\n'
                '6. Można dodać czosnek (opcjonalnie).\n'
                '7. Na koniec parmezan/grana padano i wszystko wymieszać.\n'
                '8. Dodajemy makaron i boczek do sosu, mieszamy i podajemy.'
            ),
            prep_time=10,
            cook_time=20,
            servings=2,
            difficulty='easy',
            is_published=True,
        )
        makaron_boczek.tags.add(tag_szybkie, tag_makaron, tag_boczek)

        for name, qty, unit in [
            ('Boczek', '200', 'g'),
            ('Czosnek granulowany', '1', 'łyżeczka'),
            ('Papryka wędzona', '1', 'łyżeczka'),
            ('Sól', '', 'do smaku'),
            ('Oliwa z oliwek', '2', 'łyżki'),
            ('Makaron', '200', 'g'),
            ('Masło', '1', 'łyżka'),
            ('Mąka', '1', 'łyżeczka'),
            ('Mleko', '200', 'ml'),
            ('Czosnek świeży (opcjonalnie)', '2', 'ząbki'),
            ('Parmezan lub Grana Padano', '50', 'g'),
        ]:
            Ingredient.objects.create(recipe=makaron_boczek, name=name, quantity=qty, unit=unit)

        self.stdout.write(self.style.SUCCESS('Dodano: Makaron z boczkiem w sosie serowym'))
