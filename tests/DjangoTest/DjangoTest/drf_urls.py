from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from error_tracker.django import urls
from core import views
from core.serializers import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dev/', include(urls)),
    path('', views.index),
    path('value-error', views.value_error),
    path('post-view', views.post_view),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]
