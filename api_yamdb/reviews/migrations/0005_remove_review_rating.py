# Generated by Django 2.2.16 on 2022-03-09 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_review_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='rating',
        ),
    ]
