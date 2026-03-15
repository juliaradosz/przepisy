from django.core.management.base import BaseCommand
from recipes.models import Category, Recipe


class Command(BaseCommand):
    help = 'Przenosi przepisy z Makarony do Dania główne i usuwa kategorię Makarony'

    def handle(self, *args, **options):
        try:
            makarony = Category.objects.get(name='Makarony')
            dania, _ = Category.objects.get_or_create(
                name='Dania główne',
                defaults={'slug': 'dania-glowne', 'description': 'Obiadowe dania główne'},
            )
            count = Recipe.objects.filter(category=makarony).update(category=dania)
            self.stdout.write(f'  Przeniesiono {count} przepisów do Dania główne')
            makarony.delete()
            self.stdout.write(self.style.SUCCESS('Usunięto kategorię Makarony'))
        except Category.DoesNotExist:
            self.stdout.write('Kategoria Makarony nie istnieje')
