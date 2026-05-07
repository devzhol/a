from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
    path('product/<int:id>/', views.product_detail),
]