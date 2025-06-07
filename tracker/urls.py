from django.urls import path
from .views import check_price

urlpatterns = [
    path('check_price/', check_price, name='check_price'),
]
