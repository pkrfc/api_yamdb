from rest_framework import serializers

from reviews.models import Categories, Genres, Titles

from datetime import datetime as dt


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'slug']
        model = Categories


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'slug']
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all(),
    )

    class Meta:
        fields = '__all__'
        model = Titles

    def to_representation(self, obj):
        self.fields['genre'] = GenreSerializer(many=True)
        self.fields['category'] = CategoriesSerializer()
        return super(TitlesSerializer, self).to_representation(obj)

    def validate_year(self, value):
        year = dt.now().year
        if not (0 <= value <= year):
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего'
            )
        return value
