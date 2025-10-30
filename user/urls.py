from django.urls import path

from .views import login_view, register_view, logout_view, profile_view, delete_account, change_password


urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('delete_account/', delete_account, name='delete_account'),
    path('change_password/', change_password, name='change_password'),
]
