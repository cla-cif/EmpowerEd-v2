from django.urls import path, include
from . import views

app_name = "home"

urlpatterns = [
    path('', views.LandingView.as_view(), name='home'),
    path('logout/', views.logout_view),
    path('accounts/', include('allauth.urls')),
    path('microsoft/', include('microsoft_auth.urls', namespace='microsoft')),
    path('resources/', views.ResourcesView.as_view(), name='resources'),
    path('mentors/', views.MentorsView.as_view(), name='mentors'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('profile/<pk>', views.UserProfileDetailView.as_view(),
         name='profile'),
    path('profile/update/<pk>', views.UserProfileUpdateView.as_view(),
         name='update_profile'),
]
