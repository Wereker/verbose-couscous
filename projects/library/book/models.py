from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    Title = models.CharField(max_length=64, blank=False, null=False)
    Author = models.ForeignKey('Author', blank=False, null=False, on_delete=models.CASCADE)
    Year_Publishing = models.IntegerField(blank=False, null=False)
    Count_Page = models.IntegerField(blank=False, null=False)
    Cover = models.ImageField(upload_to='uploads', blank=True, null=True)
    Publisher = models.CharField(max_length=64, blank=False, null=False)
    Genre = models.ForeignKey('Genre', blank=False, null=False, on_delete=models.CASCADE)
    Price = models.IntegerField(blank=False, null=False)
    Removed = models.BooleanField(default=False)
    Date_Create = models.DateTimeField(auto_now_add=True)
    Date_Update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Author} "{self.Title}"'


class Author(models.Model):
    First_Name = models.CharField(max_length=64, blank=False, null=False)
    Last_Name = models.CharField(max_length=64, blank=False, null=False)
    Pseudonym = models.CharField(max_length=64, blank=True, null=True)
    Biography = models.TextField(blank=True, null=True)
    Date_Create = models.DateTimeField(auto_now_add=True)
    Date_Update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.First_Name[0]}. {self.Last_Name}'


class Genre(models.Model):
    Name = models.CharField(max_length=64, blank=False, null=False)
    Description = models.TextField(blank=True, null=True)
    Image = models.ImageField(upload_to='genres', blank=True, null=True)

    def __str__(self):
        return self.Name


class Loan(models.Model):
    Book = models.ForeignKey('Book', blank=False, null=False, on_delete=models.CASCADE)
    User = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    Quantity = models.IntegerField(blank=True, null=True)
    Date_Create = models.DateTimeField(auto_now_add=True)
    Date_Update = models.DateTimeField(auto_now=True)


class Review(models.Model):
    Book = models.ForeignKey('Book', blank=False, null=False, on_delete=models.CASCADE)
    User = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    Mark = models.IntegerField(blank=False, null=False)
    Text_Review = models.TextField(blank=True, null=True)
    Date_Create = models.DateTimeField(auto_now_add=True)
    Date_Update = models.DateTimeField(auto_now=True)


class Cart:

    def __init__(self, request):
        self.session = request.session

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, no session key! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available on all pages of site
        self.cart = cart

    def add(self, book, quantity):
        book_id = str(book.id)
        book_qty = str(quantity)

        # Logic
        if book_id in self.cart:
            pass
        else:
            self.cart[book_id] = int(book_qty)

        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_books(self):
        # Get ids from cart
        book_ids = self.cart.keys()

        # Use ids to lookup products in database model
        books = Book.objects.filter(id__in=book_ids)

        # Return those looked up products
        return books

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, book, quantity):
        book_id = str(book)
        book_qty = str(quantity)

        ourcart = self.cart

        ourcart[book_id] = book_qty

        self.session.modified = True

        thing = self.cart
        return thing

    def delete(self, book):
        book_id = str(book)

        if book_id in self.cart:
            del self.cart[book_id]

        self.session.modified = True

    def clear(self):
        self.cart.clear()
        self.session.modified = True

    def cart_total(self):
        # Get book IDs
        book_id = self.cart.keys()

        # Lookup those keys in our product
        books = Book.objects.filter(id__in=book_id)
        quantities = self.cart
        total = 0

        for key, value in quantities.items():
            key = int(key)
            for book in books:
                if book.id == key:
                    total = total + (book.Price * int(value))

        return total
