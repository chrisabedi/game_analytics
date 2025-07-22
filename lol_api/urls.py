from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_player_info),
    path('get/<str:game_name>/<str:tag_line>',views.get_player_info),
    path('delete/<str:game_name>/<str:tag_line>',views.delete_player),
    path('update', views.update_player),
    path('get/all',views.get_all_players)
]
