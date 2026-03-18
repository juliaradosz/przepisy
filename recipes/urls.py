from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    # Strona główna
    path('', views.home, name='home'),

    # Przepisy
    path('przepisy/', views.recipe_list, name='recipe_list'),
    path('przepis/nowy/', views.recipe_create, name='recipe_create'),
    path('przepis/<slug:slug>/', views.recipe_detail, name='recipe_detail'),
    path('przepis/<slug:slug>/edytuj/', views.recipe_update, name='recipe_update'),
    path('przepis/<slug:slug>/usun/', views.recipe_delete, name='recipe_delete'),

    # Kategorie
    path('kategorie/', views.category_list, name='category_list'),
    path('kategoria/nowa/', views.category_create, name='category_create'),
    path('kategoria/<slug:slug>/', views.category_detail, name='category_detail'),

    # Wyszukiwanie
    path('szukaj/', views.search, name='search'),

    # Ulubione
    path('przepis/<slug:slug>/ulubione/', views.toggle_favorite, name='toggle_favorite'),

    # Wydarzenia
    path('wydarzenia/', views.event_list, name='event_list'),
    path('wydarzenie/nowe/', views.event_create, name='event_create'),
    path('wydarzenie/<int:pk>/', views.event_detail, name='event_detail'),
    path('wydarzenie/<int:pk>/edytuj/', views.event_edit, name='event_edit'),
    path('wydarzenie/<int:pk>/usun/', views.event_delete, name='event_delete'),
    path('wydarzenie/<int:pk>/dodaj-przepis/', views.event_add_recipe, name='event_add_recipe'),
    path('wydarzenie/<int:pk>/usun-przepis/<int:recipe_id>/', views.event_remove_recipe, name='event_remove_recipe'),
    path('wydarzenie/<int:pk>/odhacz/<int:recipe_id>/', views.event_toggle_done, name='event_toggle_done'),
    path('wydarzenie/<int:pk>/zakupy/', views.event_shopping_list, name='event_shopping_list'),

    # Użytkownicy
    path('rejestracja/', views.register, name='register'),
    path('logowanie/', views.user_login, name='login'),
    path('wyloguj/', views.user_logout, name='logout'),
    path('profil/<str:username>/', views.profile, name='profile'),
    path('profil/<str:username>/edytuj/', views.profile_edit, name='profile_edit'),
    path('uzytkownik/<int:user_id>/uprawnienia/', views.toggle_staff, name='toggle_staff'),
]
