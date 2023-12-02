# recipes/serializers.py
from rest_framework import serializers
from .models import Recipe, Review, Rating


class RecipeInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['heading', 'ingredients', 'image_url', 'category', 'tags']


class RecipeOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
