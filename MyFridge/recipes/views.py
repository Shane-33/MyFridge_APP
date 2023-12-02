# recipes/views.py
from .models import Recipe, Moment
from django.shortcuts import render, get_object_or_404
from .models import Moment, Comment, Like
from urllib.parse import quote
import requests
from .forms import RatingForm, ReviewForm
from django.shortcuts import render
from .forms import RecipeForm, CategoryForm, TagForm
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import Recipe, Review, Rating, Moment
from .serializers import RecipeInputSerializer, RecipeOutputSerializer, ReviewSerializer, RatingSerializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# @login_required


def recipe_moment(request, pk=None):
    if pk is not None:
        recipe = get_object_or_404(Recipe, pk=pk)
        moments = Moment.objects.filter(recipe=recipe).order_by('-created_at')
    else:
        # Handle the case when pk is not provided (optional parameter)
        moments = Moment.objects.all()
        recipe = None

    # Handle posting a new moment
    if request.method == 'POST':
        caption = request.POST.get('caption', '')
        image = request.FILES.get('image', None)
        if caption or image:
            new_moment = Moment.objects.create(
                user=request.user if request.user.is_authenticated else None,
                recipe=recipe,
                caption=caption,
                image=image
            )

    return render(request, 'recipes/recipe_moment.html', {'moments': moments, 'recipe': recipe})


def google_search(request):
    api_key = 'AIzaSyC6JjJA761cI4asqcxgO2a9jrsTH8nbw2c'
    cx = '41a1122bf3d4d429e'  # This is your Custom Search Engine ID

    query = request.GET.get('q', '')
    if query:
        # Properly encode the query for the URL
        encoded_query = quote(query)

        # Make a request to the Custom Search JSON API
        search_url = f'https://www.googleapis.com/customsearch/v1?q={encoded_query}&key={api_key}&cx={cx}'
        response = requests.get(search_url)
        results = response.json().get('items', [])

        return render(request, 'recipes/google_search_results.html', {'query': query, 'results': results})

    return render(request, 'recipes/google_search.html')


class GetRecipeSuggestions(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ingredients = request.data.get('ingredients_list', [])
        placeholder_ingredients = ', '.join(
            [f'ingredient {i + 1}' for i in range(len(ingredients))])

        prompt = f"Generate 5 recipes suggestions based on ingredients {placeholder_ingredients}, and mention the quantity for each ingredient. e.g. 1 cup ingredient name 1, 1/2 cup ingredient name 2 etc. Generate at least 5 different types of recipes based on the ingredients given and give : (colon)after the heading of each recipe: {', '.join(ingredients)}"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1000,
            temperature=1.2,
        )

        suggestions = response.choices[0].text.strip()
        recipes = parse_suggestions(suggestions)

        return Response({'recipes': recipes})


class CreateRecipe(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RecipeInputSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({'message': 'Recipe created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RateRecipe(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        rating = request.data.get('rating')

        # Placeholder logic to save the rating to the database
        # Ensure you have a field in your Recipe model to store ratings
        recipe.average_rating = (recipe.average_rating + float(rating)) / 2
        recipe.save()

        return Response({'message': 'Rating submitted successfully'})


class WriteReview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        comment = request.data.get('comment')

        # Placeholder logic to save the review to the database
        # Ensure you have a model for storing reviews and establish a relationship with Recipe
        review = Review.objects.create(
            user=request.user, recipe=recipe, comment=comment)

        return Response({'message': 'Review submitted successfully'})


@login_required
@require_POST
def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    user = request.user

    if recipe.favorites.filter(pk=user.pk).exists():
        # Recipe is in favorites, remove it
        recipe.favorites.remove(user)
        is_favorite = False
    else:
        # Recipe is not in favorites, add it
        recipe.favorites.add(user)
        is_favorite = True

    return JsonResponse({'is_favorite': is_favorite})


# ... (similarly modify other views as needed)


@login_required
@require_POST
def toggle_favorite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    user = request.user

    if recipe.favorites.filter(pk=user.pk).exists():
        # Recipe is in favorites, remove it
        recipe.favorites.remove(user)
        is_favorite = False
    else:
        # Recipe is not in favorites, add it
        recipe.favorites.add(user)
        is_favorite = True

    # You can return a JsonResponse with the updated state
    return JsonResponse({'is_favorite': is_favorite})


@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            # Redirect to the recipe list or wherever you want
            return redirect('recipe_list')
    else:
        form = CategoryForm()
    return render(request, 'recipes/recipe_create.html', {'form': form})


def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recipe_list')
    else:
        form = TagForm()
    return render(request, 'recipes/ecipe_create.html', {'form': form})


@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()  # Save many-to-many relationships (e.g., tags)
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_create.html', {'form': form})


def recipe_detail(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    rating_form = RatingForm()
    review_form = ReviewForm()

    context = {
        'recipe': recipe,
        'rating_form': rating_form,
        'review_form': review_form,
    }

    return render(request, 'recipes/recipe_detail.html', context)


def recipe_list(request):
    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    tag_filter = request.GET.get('tag', '')

    recipes = Recipe.objects.all()
    print(recipes)
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

    if query:
        recipes = recipes.filter(heading__icontains=query)

    if category_filter:
        recipes = recipes.filter(category__name=category_filter)

    if tag_filter:
        recipes = recipes.filter(tags__name=tag_filter)

    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})
