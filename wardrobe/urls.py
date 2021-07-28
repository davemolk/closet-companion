from django.urls import path
from . import views

urlpatterns = [
    path('items', views.items, name='items'),
    path('item/<str:pk>/', views.item, name='item'),
    path('create-item/', views.createItem, name='create-item'),
    path('update-item/<str:pk>/', views.updateItem, name='update-item'),
    path('delete-item/<str:pk>/', views.deleteItem, name='delete-item'),   
]