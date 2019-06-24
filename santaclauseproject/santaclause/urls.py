from . import views as santaclause_views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'santaclause'

urlpatterns = [
    path('present/', santaclause_views.present, name='present'),
    path('signup/', santaclause_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='santaclause/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('user_info/<int:pk>/', santaclause_views.user_info, name='user_info'),
    path('user_info/<int:pk>/edit', santaclause_views.profile_edit, name='profile_edit'),
    path('account_info/<int:pk>/', santaclause_views.account_info, name='account_info'),
    path('account_info/<int:pk>/edit', santaclause_views.account_edit, name='account_edit'),
    path('detail/<int:pk>/', santaclause_views.detail, name='detail'),
    path('detail/<int:pk>/edit/', santaclause_views.edit, name='edit'),
    path('detail/<int:pk>/delete/', santaclause_views.delete, name='delete'),
    path('api/favorite/<int:pk>/', santaclause_views.api_favorite, name='api_favorite'),
    path('', santaclause_views.index, name='index'),
]

