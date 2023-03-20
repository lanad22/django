from django.urls import path
from . import views

urlpatterns = [
    path('', views.mystore, name = 'mystore'),
    path('cart/', views.cart, name = 'cart'),
    path('update_item/', views.updateItem, name = 'update_item'),
    path("<int:id>/", views.product_detail, name="product_detail")
]