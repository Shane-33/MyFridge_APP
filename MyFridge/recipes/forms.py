# recipes/forms.py
from .models import Recipe, Category, Tag
from django import forms
from .models import Rating, Review


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment']


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['heading', 'ingredients', 'image_url', 'category', 'tags']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
