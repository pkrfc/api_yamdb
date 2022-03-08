from .models import Comment, Review
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from user.models import User
from api.models import Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )
    score = serializers.IntegerField(max_value=10, min_value=1)

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        if self.context['request'].method == 'PATCH':
            return data
        review_exists = Review.objects.filter(title=title_id,
                                                 author=user).exists()
        if review_exists:
            raise serializers.ValidationError('Вы уже оставили отзыв.')
        return data    

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'pub_date', 'score')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date')
        model = Comment
