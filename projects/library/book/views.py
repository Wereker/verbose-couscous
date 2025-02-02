from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from book.models import Book, Genre, Author, Review, Cart, Loan
from book.forms import AddReviewForm
from django.http import JsonResponse
import json

def check_loggin(request):
    if 'sessionid' in request.COOKIES:
        session_key = request.COOKIES['sessionid']

        session = Session.objects.get(session_key=session_key)
        if session:

            user = request.user
            if user.id:
                return True

    return False


class HomeBookView(View):

    def get(self, request):

        is_logged = check_loggin(request)
        genres = Genre.objects.all()
        books = Book.objects.filter(Removed=False)[:6]
        user = None
        if request.user.id:
            user = User.objects.get(pk=request.user.id)

        categories = []
        for genre in genres:
            categories.append((genre.pk, Book.objects.filter(Genre=genre.pk).count()))

        context = {
            'genres': genres,
            'books': books,
            'categories': categories,
            'is_logged': is_logged,
            'user': user,
        }

        return render(request, 'library/index.html', context=context)


def index(request):
    return redirect('home')


class BookShopView(View):
    def get(self, request):

        is_logged = check_loggin(request)
        books = Book.objects.filter(Removed=False)
        genres = Genre.objects.all()
        user = None
        if request.user.id:
            user = User.objects.get(pk=request.user.id)

        '''Paginator'''
        page = request.GET.get('page', 1)
        paginator = Paginator(books, 6)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)

        context = {
            'books': books,
            'genres': genres,
            'is_logged': is_logged,
            'user': user,
        }

        return render(request, 'book/shop.html', context=context)


class BookShopCategoryView(View):

    def get(self, request, **kwargs):
        is_logged = check_loggin(request)
        genres = Genre.objects.all()
        genre = Genre.objects.get(pk=kwargs['pk'])
        books = Book.objects.filter(Genre=genre.pk)
        user = None
        if request.user.id:
            user = User.objects.get(pk=request.user.id)

        '''Paginator'''
        page = request.GET.get('page', 1)
        paginator = Paginator(books, 6)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)

        context = {
            'genres': genres,
            'genre': genre,
            'books': books,
            'is_logged': is_logged,
            'user': user,
        }

        return render(request, 'book/shop-category.html', context=context)


class BookCardView(View):

    def get(self, request, **kwargs):
        is_logged = check_loggin(request)
        genres = Genre.objects.all()
        book = Book.objects.get(pk=kwargs['pk'])
        reviews = Review.objects.filter(Book=kwargs['pk'])
        user = None
        if request.user.id:
            user = User.objects.get(pk=request.user.id)

        context = {
            'book': book,
            'reviews': reviews,
            'genres': genres,
            'is_logged': is_logged,
            'user': user,
        }

        return render(request, template_name='book/card.html', context=context)


def search_book_title(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        books = Book.objects.filter(Title__startswith=search_str)

        data = books.values()

        return JsonResponse(list(data), safe=False)


def get_book_filter(request):
    if request.method == 'POST':
        filter_str = json.loads(request.body).get('filterText')

        match filter_str:
            case 'ALL':
                books = Book.objects.filter(Removed=False)[:6]
            case 'NEWEST':
                books = Book.objects.filter(Date_Create__date__gt=(datetime.now() - timedelta(days=14)))
            case _:
                books = Book.objects.filter(Removed=False)[:6]

        data = books.values()

        return JsonResponse(list(data), safe=False)


@login_required
def books_buy(request):
    cart = Cart(request)
    quantities = cart.get_quants()
    user = None
    if request.user.id:
        user = User.objects.get(pk=request.user.id)

    for key, value in quantities.items():
        book = Book.objects.get(pk=int(key))
        Loan.objects.create(Book=book, User=user, Quantity=int(value))

    cart.clear()

    return JsonResponse({'qty': quantities})


@login_required
def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_books = cart.get_books()

    genres = Genre.objects.all()
    is_logged = check_loggin(request)
    quantities = cart.get_quants
    totals = cart.cart_total()

    user = None
    if request.user.id:
        user = User.objects.get(pk=request.user.id)

    form = AddReviewForm(request.POST)

    context = {
        'cart_books': cart_books,
        'genres': genres,
        'is_logged': is_logged,
        'quantities': quantities,
        'totals': totals,
        'user': user,
        'form': form,
    }
    return render(request, 'book/cart.html', context)


@login_required
def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # Test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        book_id = int(request.POST.get('book_id'))
        book_qty = int(request.POST.get('book_qty'))

        # lookup book in DB
        book = get_object_or_404(Book, id=book_id)

        # Save to session
        cart.add(book=book, quantity=book_qty)

        # Get Cart Quantity
        cart_quantity = cart.__len__()

        # Return response
        response = JsonResponse({'qty': cart_quantity})
        return response


@login_required
def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        book_id = int(request.POST.get('book_id'))

        cart.delete(book=book_id)

        response = JsonResponse({'book': book_id})
        return response


@login_required
def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        book_id = int(request.POST.get('book_id'))
        book_qty = int(request.POST.get('book_qty'))

        cart.update(book=book_id, quantity=book_qty)

        response = JsonResponse({'qty': book_qty})
        return response
