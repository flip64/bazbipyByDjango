from django.urls import path
from .views import check_price
from . import views

urlpatterns = [
    path('check_price/', check_price, name='check_price'),
    path('watched-urls/', views.watched_urls_view, name='watched_urls'),

]
