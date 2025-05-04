from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('dish/<int:dish_id>/', views.dish_detail, name='dish_detail'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
