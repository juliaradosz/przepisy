# Przepisy Kulinarne - Aplikacja Django

Strona internetowa do przeglądania, dodawania i komentowania przepisów kulinarnych.

## Funkcjonalności

- **Przeglądanie przepisów** – lista przepisów z podziałem na kategorie i tagi
- **CRUD przepisów** – dodawanie, edycja, usuwanie przepisów (wymaga logowania)
- **System komentarzy** – ocenianie i komentowanie przepisów (1-5 gwiazdek)
- **Konta użytkowników** – rejestracja, logowanie, profile z avatarami
- **Wyszukiwanie** – po tytule, opisie, składnikach i poziomie trudności
- **Panel administracyjny** – zarządzanie wszystkimi danymi
- **Responsywny design** – Bootstrap 5

## Wymagania

- Python 3.10+
- Django 5.0+
- Pillow (obsługa obrazów)

## Instalacja i uruchomienie

```bash
# Zainstaluj zależności
pip install -r requirements.txt

# Wykonaj migracje
python manage.py migrate

# Utwórz konto administratora
python manage.py createsuperuser

# Wypełnij bazę przykładowymi danymi
python manage.py seed_data

# Uruchom serwer
python manage.py runserver
```

## Komendy manage.py

- `python manage.py seed_data` – wypełnia bazę przykładowymi przepisami
- `python manage.py import_recipes plik.csv` – importuje przepisy z pliku CSV
- `python manage.py delete_old_recipes --days 30` – usuwa stare nieopublikowane przepisy

## Uruchamianie testów

```bash
python manage.py test recipes
```

## Modele danych

- **Category** – kategorie przepisów (np. Zupy, Desery)
- **Tag** – tagi (np. wegetariańskie, szybkie) – relacja ManyToMany z Recipe
- **Recipe** – przepisy (relacja ForeignKey do User i Category)
- **Ingredient** – składniki przepisu (relacja ForeignKey do Recipe)
- **Comment** – komentarze z oceną (relacja ForeignKey do Recipe i User)
- **UserProfile** – rozszerzony profil użytkownika (OneToOne z User)

## Struktura projektu

```
przepisy_project/     – konfiguracja Django (settings, urls)
recipes/              – główna aplikacja
  models.py           – modele danych (6 modeli)
  views.py            – widoki (function-based views)
  forms.py            – formularze
  urls.py             – routing
  admin.py            – konfiguracja panelu admina
  management/commands/ – komendy manage.py (3 komendy)
  tests.py            – testy
templates/            – szablony HTML (Bootstrap 5)
static/css/           – pliki CSS
```

## Autor

Projekt I z Programowania w języku Python 2025/26.
