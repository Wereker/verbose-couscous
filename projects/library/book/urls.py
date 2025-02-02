from django.urls import path
from book import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'book'

urlpatterns = [
    path('shop/', views.BookShopView.as_view(), name='book_shop'),
    path('about/<int:pk>/', views.BookCardView.as_view(), name='book_about'),
    path('category/<int:pk>', views.BookShopCategoryView.as_view(), name='book_category'),
    path('cart/', views.cart_summary, name='cart-summary'),
]
