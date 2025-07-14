from django.urls import path
from . import views

urlpatterns = [
    path('lol/analytics/<str:game_name>/<str:tag_line>/', views.get_lol_analytics),
]
