# recipes/urls.py
from .views import create_recipe, recipe_detail, recipe_list, toggle_favorite
from .views import create_category, create_tag, google_search, recipe_moment
from django.urls import path
from .views import (
    GetRecipeSuggestions,
    RateRecipe,
    WriteReview,
    GetRecipeSuggestions,
    CreateRecipe,)


urlpatterns = [
    path('recipes/moment/', recipe_moment, name='recipe_moment'),
    path('google-search/', google_search, name='google_search'),
    path('get-recipe-suggestions/', GetRecipeSuggestions.as_view(),
         name='get_recipe_suggestions'),
    path('create-recipe/', CreateRecipe.as_view(), name='create_recipe'),
    path('toggle-favorite/<int:recipe_id>/',
         toggle_favorite, name='toggle_favorite'),

    path('create-recipe/', create_recipe, name='recipe_create'),
    path('<int:pk>/', recipe_detail, name='recipe_detail'),
    path('toggle_favorite/<int:pk>/', toggle_favorite, name='toggle_favorite'),

    path('', recipe_list, name='recipe_list'),
    path('create/category/', create_category, name='create_category'),
    path('create/tag/', create_tag, name='create_tag'),
    path('get-recipe-suggestions/', GetRecipeSuggestions.as_view(),
         name='get_recipe_suggestions'),
    path('rate-recipe/<int:pk>/', RateRecipe.as_view(), name='rate_recipe'),
    path('write-review/<int:pk>/', WriteReview.as_view(), name='write_review'),
]
