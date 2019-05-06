from django.urls import path
from . import views
app_name = "pokedex_app"
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:pokemon>', views.show_pokemon, name='show_pokemon'),
]
