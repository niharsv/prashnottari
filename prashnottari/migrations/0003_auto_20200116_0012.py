# Generated by Django 2.2.6 on 2020-01-15 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prashnottari', '0002_auto_20200114_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]