from django.urls import path
from . import views

urlpatterns = [
    path('items', views.items, name='items'),
    path('item/<str:pk>/', views.item, name='item'),
    path('create-item/', views.createItem, name='create-item'),
    path('update-item/<str:pk>/', views.updateItem, name='update-item'),
    path('delete-item/<str:pk>/', views.deleteItem, name='delete-item'),
    path('outfits/', views.outfits, name='outfits'),
    path('outfit/<str:pk>/', views.outfit, name='outfit'),
    path('create-outfit/', views.createOutfit.as_view(), name="create-outfit"),
    path('update-outfit/<str:pk>/', views.updateOutfit.as_view(), name="update-outfit"),
    path('delete-outfit/<str:pk>/', views.deleteOutfit, name="delete-outfit"), 

]