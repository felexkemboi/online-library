from django.db import models
from django.urls import reverse #used t generate URLs by reversing the URL patterns
import uuid #rewuired for unique book instances

# Create your models here.
class Genre(models.Model):
	 """model representing a book genre(e.g Science fiction,Non-fiction)"""
	 name = models.CharField(max_length = 200,help_text = "Enter a book genre (e.g Science Fiction,French poetry etc.)")
	 def __str__(self):
        	""" String for representing the Model object (in Admin site etc.)"""
        	return self.name

class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file.
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre'
    
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title
    
    
    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this book.
        """
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
	"""model for representing a specific copy of a book( i.e that can be borrowed form the library)"""
	id = models.UUIDField(primary_key =True,default=uuid.uuid4,help_text = "Unique ID for this partcular book across the whole library")
	book  = models.ForeignKey('Book', on_delete = models.SET_NULL,null= True)
	imprint  = models.CharField(max_length=200)
	due_back = models.DateField(null=True,blank = True)

	LOAN_STATUS = (
		           ('m', 'Maintenance'),
		           ('o', 'On loan'),
		           ('a', 'Available'),
		           ('r', 'Reserved'),
                  )

	status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Books availability')
	list_filter = ('status','due_back')

	class meta:
		ordering = ["due_back"]

	def __str__(self):
		"""String for representing model object"""
		return '{0}({1})'.format(self.id,self.book.title)

class Author(models.Model):
	"""Model for representing an author"""
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	date_of_birth = models.DateField(null =True,blank = True)
	date_of_death = models.DateField('Died' ,null = True,blank = True)

	class meta:
		ordering = [ "first_name", "last_name" ]

	def get_absolute_url(self):
		"""Returns the url to access a particular author instance"""
		return reverse('author_detail',args =[str(self.id)])

	def __str__(self):
		"""String reperesenting the model object"""
		return '{0},{1}'.format(self.last_name,self.first_name)
