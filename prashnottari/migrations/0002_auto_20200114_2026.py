# Generated by Django 2.2.6 on 2020-01-14 14:56

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prashnottari', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=ckeditor.fields.RichTextField(max_length=5000),
        ),
    ]
