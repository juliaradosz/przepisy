import re

import django.db.models.deletion
from django.db import migrations, models


NUM_PREFIX = re.compile(r'^\s*\d+\s*[.)]\s*')


def populate_steps_from_instructions(apps, schema_editor):
    Recipe = apps.get_model('recipes', 'Recipe')
    Step = apps.get_model('recipes', 'Step')

    for recipe in Recipe.objects.all():
        if not recipe.instructions:
            continue
        if Step.objects.filter(recipe=recipe).exists():
            continue
        order = 1
        for raw in recipe.instructions.splitlines():
            text = raw.strip()
            if not text:
                continue
            text = NUM_PREFIX.sub('', text).strip()
            if not text:
                continue
            Step.objects.create(recipe=recipe, order=order, text=text)
            order += 1


def reverse_noop(apps, schema_editor):
    Step = apps.get_model('recipes', 'Step')
    Step.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_event_eventrecipe_event_recipes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='Kolejność')),
                ('text', models.TextField(verbose_name='Treść kroku')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='recipes.recipe', verbose_name='Przepis')),
            ],
            options={
                'verbose_name': 'Krok',
                'verbose_name_plural': 'Kroki',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.RunPython(populate_steps_from_instructions, reverse_noop),
    ]
