"""empowered URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework import routers
from django.conf.urls.static import static
from chat_backend.api.views import (ConversationViewSet,
                                    MessageViewSet)
# from microsoft_auth.views import (MicrosoftLoginView)
# from microsoft_auth.views import (MicrosoftLogoutView)
# from microsoft_auth.views import (MicrosoftCallbackView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('messages/', include('chat_backend.urls', namespace="messages")),
    path('accounts/', include('allauth.urls')),
    path('microsoft/', include('microsoft_auth.urls', namespace='microsoft')),

    # path('microsoft-auth/login/', MicrosoftLoginView.as_view(), name='microsoft_auth_login'),
    # path('microsoft-auth/logout/', MicrosoftLogoutView.as_view(), name='microsoft_auth_logout'),
    # path('microsoft-auth/callback/', MicrosoftCallbackView.as_view(), name='microsoft_auth_callback'),

    path('', include('home.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


router = routers.DefaultRouter()

router.register("api/conversations", ConversationViewSet,
                basename='Conversations')
router.register("api/messages", MessageViewSet, basename='Messages')

urlpatterns += router.urls
