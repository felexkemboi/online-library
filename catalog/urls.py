# Use include() to add paths from the catalog application 
from django.urls import path
from . import views


urlpatterns = [
   path('', views.index, name='index'),
   #path('books/',views.BookListView.as_View(), name = 'books'),
]
