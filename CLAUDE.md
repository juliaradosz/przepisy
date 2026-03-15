# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Polish-language Django recipe sharing app ("Przepisy Kulinarne"). Users can browse, create, and comment/rate recipes. Uses SQLite, function-based views, Bootstrap 5 frontend, and Django's built-in auth.

## Commands

```bash
pip install -r requirements.txt   # Install dependencies
python manage.py migrate          # Apply migrations
python manage.py runserver        # Start dev server
python manage.py test recipes     # Run all tests
python manage.py seed_data        # Populate DB with sample data
python manage.py import_recipes plik.csv        # Import recipes from CSV
python manage.py delete_old_recipes --days 30   # Remove old unpublished recipes
```

## Architecture

- **Django project**: `przepisy_project/` (settings, root urls, wsgi/asgi)
- **Single app**: `recipes/` — all business logic lives here
- **Views**: All function-based (no CBVs), in `recipes/views.py`
- **Forms**: `recipes/forms.py` — uses `inlineformset_factory` for `IngredientFormSet` (Recipe + Ingredients edited together)
- **Templates**: `templates/` at project root (not inside the app), using `base.html` layout with Bootstrap 5
- **Static files**: `static/css/style.css`
- **Media uploads**: `media/` (avatars, recipe images, category images)
- **URL namespace**: All recipe URLs use `recipes:` namespace; URL paths are in Polish (e.g., `/przepisy/`, `/kategoria/`, `/szukaj/`)

## Key Design Decisions

- Recipe slugs are auto-generated from title with uniqueness suffix in `recipe_create` view
- Comments have `unique_together = ['recipe', 'author']` — one comment per user per recipe
- Recipe edit/delete is restricted to the author or staff users
- `UserProfile` is created on registration and lazily via `get_or_create` in profile views
- Settings: `LANGUAGE_CODE = 'pl'`, `TIME_ZONE = 'Europe/Warsaw'`

## Models (recipes/models.py)

6 models with these relationships:
- `Recipe` → ForeignKey to `User` (author) and `Category`; ManyToMany to `Tag`
- `Ingredient` → ForeignKey to `Recipe`
- `Comment` → ForeignKey to `Recipe` and `User`; has `rating` (1-5)
- `UserProfile` → OneToOne with `User`
- `Recipe.average_rating` is a computed property via `Avg` aggregate on comments
