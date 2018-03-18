from django.shortcuts import render
from .models import Book,Author,BookInstance,Genre

# Create your views here.
def index(request):
	"""View function for home page site"""
	#generate counts of some main objects
	num_books = Book.objects.all().count()
	num_instances=BookInstance.objects.all().count()
	num_instances_available=BookInstance.objects.filter(status__exact='a').count()
	#available books(status = 'a')
	num_authors = Author.objects.count() #the all() is implified by default

	#render the html template index.html with the data  in the context variable
	return render(request,'index.html', context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},)