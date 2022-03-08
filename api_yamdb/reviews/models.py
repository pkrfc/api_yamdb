from django.db import models

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from datetime import datetime as dt


def validate_year(value):
    if value <= dt.now().year and value >= 0:
        return value
    else:
        raise ValidationError('Год выпуска не может быть больше текущего')


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        unique=True,
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message=('Неккоректное поле slug')
            )
        ]
    )

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        unique=True,
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message=('Неккоректное поле slug')
            )
        ]
    )

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(validators=[validate_year])
    description = models.TextField(null=True, blank=True)
    genre = models.ManyToManyField(
        Genres,
        through='GenreTitles',
        related_name='genre',
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=False,
        null=True
    )

    def __str__(self):
        return self.name


class GenreTitles(models.Model):
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.titles}'
