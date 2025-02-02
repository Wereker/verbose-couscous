from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.decorators.csrf import csrf_exempt

from book import views as book_views

urlpatterns = [
    path('', book_views.index, name='index'),
    path('home/', book_views.HomeBookView.as_view(), name='home'),
    path('book/', include('book.urls', namespace='book')),
    path('user/', include('user.urls', namespace='user')),
    re_path(r'create/', csrf_exempt(book_views.cart_add), name='cart-add'),
    re_path(r'delete/', csrf_exempt(book_views.cart_delete), name='cart-delete'),
    re_path(r'update/', csrf_exempt(book_views.cart_update), name='cart-update'),
    re_path(r'buy/', csrf_exempt(book_views.books_buy), name='books-buy'),
    re_path(r'ajax/search/', csrf_exempt(book_views.search_book_title), name='ajax-search'),
    re_path(r'ajax/filter/', csrf_exempt(book_views.get_book_filter), name='ajax-filter'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
