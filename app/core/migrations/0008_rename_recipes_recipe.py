# Generated by Django 3.2.23 on 2024-01-09 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_rename_recipe_recipes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Recipes',
            new_name='Recipe',
        ),
    ]
