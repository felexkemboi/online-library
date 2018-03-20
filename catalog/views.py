from django.shortcuts import render
from .models import Book,Author,BookInstance,Genre
from django.views import generic 
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def index(request):
	"""View function for home page site"""
	#generate counts of some main objects
	num_books = Book.objects.all().count()
	num_instances=BookInstance.objects.all().count()
	num_instances_available=BookInstance.objects.filter(status__exact='a').count()
	#available books(status = 'a')
	num_authors = Author.objects.count() #the all() is implified by default

	#number of visits 
	num_visits = request.session.get('num_visits',0)
	request.session['num_visits'] = num_visits+1

	#render the html template index.html with the data  in the context variable
	return render(request, 'index.html', context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors,'num_visits':num_visits,})


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'   # your own name for the list as a template variable
    template_name = 'book_list.html'  # Specify your own template name/location
    def get_context_data(self, **kwargs):
       # Call the base implementation first to get a context
       context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
       context['book_list'] = Book.objects.all()
       return context

class BookDetailView(generic.DetailView):
    """
    Generic class-based detail view for a book.
    """
    model = Book
    context_object_name = 'book-detail'   # your own name for the list as a template variable

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        return context

"""class AuthorListView(generic.ListView):
    ""
    Generic class-based list view for a list of authors.
   
    model = Author
    context_object_name = 'author_list'   # your own name for the list as a template variable
    #queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    template_name = 'author_list.html'  # Specify your own template name/location
    #book_list = Book.objects.all()
    def get_context_data(self, **kwargs):
     """
class AuthorListView(generic.ListView):
    """
    Generic class-based list view for a list of authors.
    """
    model = Author
    template_name = 'author_list.html' 
    paginate_by = 10 


class AuthorDetailView(generic.DetailView):
    """
    Generic class-based detail view for an author.
    """
    model = Author
    context_object_name = 'author_detail'   # your own name for the list as a template variable

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        return context

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
	"""Generic class-based view listing books on loan to a current user"""
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by  = 10

	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')