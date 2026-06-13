from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('skins/', views.skin_list, name='skin_list'),
    path('skins/<int:pk>/', views.skin_detail, name='skin_detail'),
    path('sell/', views.sell_skin, name='sell_skin'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('profile/', views.profile, name='profile'),
    path('skins/<int:pk>/delete/', views.delete_skin, name='delete_skin'),
    path('register/', views.register, name='register'),
    path('newsletter/', views.newsletter_subscribe, name='newsletter'),
    path('game/<slug:slug>/', views.game_skins, name='game_skins'),
]
