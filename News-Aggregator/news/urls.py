from django.urls import path
from news.views import scrape, news_list, search_articles

urlpatterns = [
    path('scrape/<str:name>', scrape, name="scrape"),
    path('search/', search_articles, name="search"),
    path('', news_list, name="home"),
]