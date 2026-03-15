from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from recipes.models import Recipe, Ingredient, Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.first()

        def add(title, cat_name, desc, instr, servings, ings):
            cat, _ = Category.objects.get_or_create(name=cat_name, defaults={'slug': slugify(cat_name)})
            slug = slugify(title)
            base = slug
            c = 1
            while Recipe.objects.filter(slug=slug).exists():
                slug = f'{base}-{c}'
                c += 1
            r = Recipe.objects.create(
                title=title, slug=slug, author=user, category=cat,
                description=desc, instructions=instr, servings=servings, is_published=True,
            )
            for n, q, u in ings:
                Ingredient.objects.create(recipe=r, name=n, quantity=q, unit=u)
            self.stdout.write(f'Dodano: {title} ({len(ings)} skladnikow)')

        add(
            'Salatka ziemniaczana z ogorkiem i rzodkiewka',
            'Salatki',
            'Salatka ziemniaczana z ogorkiem, rzodkiewka i koperkiem na grilla.',
            '1. Ziemniaki gotuje w osolonej wodzie. Studze i obieram. Kroje w nieduza kosteczke.\n'
            '2. Rzodkiewki kroje w polplasterki, ogorki w kosteczke, koperek i szczypiorek oraz cebule siekam.\n'
            '3. Do miski wsypuje wszystkie pokrojone skladniki. W osobnej miseczce mieszam jogurt i majonez, dodaje przecisniety czosnek i mustarde, wlewam do salatki i mieszam. Doprawiam dosc obficie sola i pieprzem.\n'
            '4. Salatke odkladam do lodowki minimum na godzine, by sie przegryzla, a najlepiej na cala noc.',
            6,
            [
                ('Ziemniaki', '1.3', 'kg'), ('Rzodkiewki', '2', 'peczki'),
                ('Ogorki konserwowe lub kiszone', '5-6', 'szt.'),
                ('Koperek', '1', 'peczek'), ('Pietruszka zielona', '', 'garsc'),
                ('Cebula', '1', 'szt.'), ('Szczypiorek', '0.5', 'peczka'),
                ('Jogurt naturalny', '180', 'ml'), ('Majonez', '2', 'lyzki'),
                ('Musztarda', '1', 'lyzeczka'), ('Czosnek', '1', 'zabek'),
                ('Sol', '', 'do smaku'), ('Pieprz', '', 'do smaku'),
            ],
        )

        add(
            'Kruszonka',
            'Desery i wypieki',
            'Domowa kruszonka na ciescie jest jak wisienka na torcie. Chrupiaca kruszonka neutralizuje czesto kwasny smak owocow dodanych do ciasta.',
            'Wszystkie skladniki umiesc w misce i rozcieraj palcami na drobna kruszonke, az powstana nierowne kawaleczki. Posypac ciasto przed pieczeniem.',
            None,
            [('Maka pszenna', '150', 'g'), ('Cukier', '100', 'g'), ('Maslo', '100', 'g')],
        )

        add(
            'Chrupiace owsiane ciasteczka',
            'Ciastka',
            'Przepis na okolo 35 chrupiacych ciasteczek owsianych.',
            '1. Maslo i bialy cukier umiescic w misie miksera i utrzec do otrzymania jasnej, puszystej masy.\n'
            '2. Dodac cukier brazowy i kontynuowac ucieranie. Dodac jajko i zmiksowac.\n'
            '3. Wsypac pozostale skladniki i zmiksowac do otrzymania jednolitej masy.\n'
            '4. Blache wylozyc papierem do pieczenia. Z ciasta robic kulki wielkosci orzecha wloskiego, splaszczyc je lyzka. Ukladac na blaszce w sporych odstepach.\n'
            '5. Piec w 180 stopniach przez okolo 15-17 minut do lekkiego zbrazowienia.\n'
            '6. Chwile odczekac przed zdjeciem z blachy, potem studzic na kratce.',
            35,
            [
                ('Maslo', '200', 'g'), ('Cukier drobny do wypiekow', '3/4-1', 'szklanka'),
                ('Cukier brazowy muscovado', '1/4', 'szklanki'), ('Jajko duze', '1', 'szt.'),
                ('Ekstrakt z wanilii', '1', 'lyzeczka'), ('Maka pszenna', '1', 'szklanka'),
                ('Proszek do pieczenia', '3/4', 'lyzeczki'), ('Soda oczyszczona', '1/2', 'lyzeczki'),
                ('Sol', '', 'szczypta'), ('Platki owsiane', '2.5', 'szklanki'),
            ],
        )

        add(
            'Guacamole',
            'Inne',
            '',
            '1. Do czystego naczynia miksujacego wlozyc kolendre i chili, rozdrobnic 3 s/obr. 8.\n'
            '2. Dodac pomidor i cebule szalotke, rozdrobnic 5-7 s/obr. 5. Przelozyc do innego naczynia.\n'
            '3. Do naczynia miksujacego wlozyc awokado, dodac sok z cytryny, sol i pieprz, rozdrobnic 5-8 s/obr. 4.\n'
            '4. Dodac rozdrobnione wczesniej warzywa, wymieszac 5 s/obr. 3. Przelozyc do miseczki.\n'
            '5. Guacamole podawac bezposrednio po przygotowaniu lub odstawic do lodowki.',
            None,
            [
                ('Kolendra swieza', '10-15', 'galazek'), ('Papryczka chili', '10-20', 'g'),
                ('Pomidor', '80-100', 'g'), ('Cebula szalotka', '40-60', 'g'),
                ('Awokado dojrzale', '450', 'g'), ('Sok z cytryny', '15-20', 'g'),
                ('Sol', '1', 'lyzeczka'), ('Pieprz czarny mielony', '1', 'lyzeczka'),
            ],
        )

        add(
            'Miodownik',
            'Desery i wypieki',
            'Miodownik na blasze 25x25 cm z kremem mascarpone i masa orzechowa.',
            'Krem: Miksujemy orzechy pekan + kajmak + rum + pasta waniliowa na mase z mascarpone.\n\n'
            'Ciasto: Miod + mleko podgrzac, dodac do reszty skladnikow i szybko zagniesc. Dzielimy na 4 czesci.\n'
            'Pierwsza czesc wykladamy na blache i kladziemy na nia mase z roztopionych w rondlu orzechow + cukier + miod + maslo.\n'
            'Wkladamy razem do piekarnika 175 stopni na 10 min. Pozostale placki pieczymy tak samo.\n\n'
            'Na pierwsza warstwe placka kladziemy powidla sliwkowe i mase kremowa, pozniej powtorzyc czynnosc i na wierzch ciasto z masa orzechowa.\n'
            'Poczekac 2 dni zeby sie przegryzlo.',
            None,
            [
                ('Mascarpone', '1', 'kg'), ('Orzechy pekan lub wloskie (krem)', '100-150', 'g'),
                ('Masa kajmak', '400', 'g'), ('Rum', '2', 'lyzki'),
                ('Pasta waniliowa', '1', 'lyzeczka'), ('Powidla sliwkowe', '300', 'g'),
                ('Maka tortowa (ciasto)', '500', 'g'), ('Maslo (ciasto)', '200', 'g'),
                ('Cukier pudru (ciasto)', '100', 'g'), ('Jajka (ciasto)', '2', 'szt.'),
                ('Soda (ciasto)', '1', 'lyzeczka'), ('Mleko (ciasto)', '2', 'lyzki'),
                ('Miod (ciasto)', '60', 'g'),
                ('Orzechy pekan lub wloskie (wierzch)', '200', 'g'),
                ('Cukier (wierzch)', '80', 'g'), ('Miod (wierzch)', '2', 'lyzki'),
                ('Maslo (wierzch)', '110', 'g'),
            ],
        )

        add(
            'Ciasto ze sliwkami i budyniem',
            'Desery i wypieki',
            '',
            '1. Sliwki pokroic na cwiartki, usunac pestki. Make wymieszac z proszkiem do pieczenia i cukrem. Dodac pokrojone zimne maslo i rozcierac palcami na drobna kruszonke.\n'
            '2. Dodac jajko i zagniesc ciasto w jednolita kule. Wlozyc do lodowki na 30 minut.\n'
            '3. Ugotowac budyn z 500 ml mleka, 4 lyzkami cukru i 1 lyzka cukru wanilinowego.\n'
            '4. Ciasto podzielic na 2 czesci. Wieksza wylozyc w formie 20x30 cm, nakluc widelcem. Piec 15 min w 180 stopniach.\n'
            '5. Na spod wylozyc budyn, ulozyc sliwki (rocieciem do gory).\n'
            '6. Na wierzch zetrzec odlozona czesc ciasta.\n'
            '7. Piec ok. 45 minut w 180 stopniach. Posypac cukrem pudrem.',
            None,
            [
                ('Sliwki np. wegierki', '500', 'g'), ('Maka pszenna', '300', 'g'),
                ('Proszek do pieczenia', '1', 'lyzeczka'), ('Cukier', '120', 'g'),
                ('Maslo lub margaryna', '200', 'g'), ('Jajko', '1', 'szt.'),
                ('Budyn smietankowy', '1', 'szt.'), ('Cukier wanilinowy', '1', 'lyzka'),
                ('Cukier puder', '', 'do posypania'),
            ],
        )

        add(
            'Pasta z awokado i jajek',
            'Inne',
            'Blyskawiczna pasta z awokado i jajek z dodatkiem czosnku - pyszne i zdrowe smarowidlo do kanapek.',
            '1. Awokado przekroj na pol, wyjmij pestke i lyzka wydroz miazszna do miseczki.\n'
            '2. Rozgniec widelcem awokado, dodaj sok z cytryny.\n'
            '3. Jajka ugotowane na twardo pokroj w drobna kostke, dodaj do awokado.\n'
            '4. Dodaj przecisniety czosnek, majonez, posiekany szczypiorek.\n'
            '5. Wymieszaj, dopraw sola i pieprzem.\n'
            '6. Podawaj na waflach ryzowych lub bagietce z plastrem pomidora.',
            4,
            [
                ('Awokado dojrzale', '1', 'szt.'), ('Sok z cytryny', '1', 'lyzka'),
                ('Jajka ugotowane na twardo', '2', 'szt.'), ('Czosnek', '2', 'zabki'),
                ('Majonez', '1', 'lyzka'), ('Szczypiorek', '1', 'peczek'),
                ('Pomidor duzy', '1', 'szt.'), ('Sol', '', 'do smaku'),
                ('Pieprz czarny', '', 'do smaku'),
            ],
        )

        add(
            'Placki ziemniaczane',
            'Dania glowne',
            'Placki ziemniaczane z Thermomixa. Podawac posypane cukrem, polane smietana lub jogurtem.',
            '1. Do naczynia miksujacego wlozyc wszystkie skladniki wg. podanej kolejnosci, rozdrobnic 20-30s/obr. 5-6.\n'
            '2. Sprawdzic konsystencje - jezeli jest zbyt rzadka, dodac wiecej maki i wymieszac 7s/obr. 3-4.\n'
            '3. Smazyc na patelni na rozgrzanym oleju na zloty kolor.\n'
            '4. Smacznego!',
            4,
            [
                ('Ziemniaki obrane', '750', 'g'), ('Cebula', '100', 'g'),
                ('Czosnek', '1-2', 'zabki'), ('Maka pszenna', '70', 'g'),
                ('Jajka', '2', 'szt.'), ('Sol', '1-1.5', 'lyzeczki'),
            ],
        )

        add(
            'Tort cappuccino',
            'Desery i wypieki',
            '',
            'Spod:\n'
            '1. Piekarnik nastawic na 175 stopni. Forme o srednicy 21-22 cm wysmarowac maslem i posypac bulka tarta.\n'
            '2. Ubic jajka z cukrem (najlepiej nad para). Nastepnie zdjac z ognia i miksowac jeszcze 2-3 min.\n'
            '3. Przesiac make z proszkiem do pieczenia, delikatnie wymieszac. Wlewac powoli mleko.\n'
            '4. Piec 25-30 min w dolnej czesci piekarnika. Ostudzic, przekroic na 3 blaty.\n\n'
            'Krem:\n'
            '5. Ubic zoltka z cukrem nad para.\n'
            '6. Zelatyne rozpuscic w odrobinie goracej wody. Kawe wymieszac z woda, dodac zelatyne, podgrzac. Dodac mascarpone i likiier.\n'
            '7. Smietanke ubic na sztywny krem i wymieszac z masa mascarpone.\n\n'
            'Montaz:\n'
            '8. Blat nasaczyc mieszanka kawy z likierem, rozsmarowac 1/3 kremu. Powtorzyc z kazdym blatem.\n'
            '9. Kakao i cukier puder przesiac na wierzch. Wstawic do lodowki, godzine przed podaniem do zamrazalnika.',
            None,
            [
                ('Maslo (spod)', '100', 'g'), ('Jajka (spod)', '2', 'szt.'),
                ('Cukier (spod)', '170', 'g'), ('Maka (spod)', '180', 'g'),
                ('Proszek do pieczenia', '2', 'lyzeczki'), ('Mleko (spod)', '100', 'ml'),
                ('Zoltka (krem)', '4', 'szt.'), ('Cukier drobny (krem)', '170', 'g'),
                ('Mascarpone (krem)', '500', 'g'), ('Zelatyna w proszku (krem)', '2', 'lyzeczki'),
                ('Kawa rozpuszczalna (krem)', '2', 'lyzki'), ('Woda (krem)', '100', 'ml'),
                ('Likiier amaretto', '3', 'lyzki'), ('Smietanka kremowka 30%', '300', 'ml'),
                ('Kakao (dekoracja)', '3', 'lyzki'), ('Cukier pudru (dekoracja)', '3', 'lyzki'),
            ],
        )

        self.stdout.write(self.style.SUCCESS('\nWszystko dodane!'))
