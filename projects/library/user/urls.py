from django.urls import path, re_path
from user import views

app_name = 'user'

urlpatterns = [
    re_path(r'login/', views.UserDjangoLogin.as_view(), name='login'),
    re_path(r'signup/', views.UserDjangoSignUp.as_view(), name='signup'),
    path('logout/', views.userLogout, name='logout'),
    path('save/', views.UserSave.as_view(), name='save-user'),
    path('profile/<int:pk>/', views.UserProfile.as_view(), name='profile'),
]
