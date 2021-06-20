from django.urls import path, re_path
from app import views

urlpatterns = [
    # The home page
    path('dashboard/', views.index, name='home'),
    path('', views.visit_page, name='home'),
    path('visits/', views.visits, name="visits"),
    path('populate-db/', views.populate_db, name="populate-db"),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
]
