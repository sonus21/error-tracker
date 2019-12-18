from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from error_tracker.django import urls
from core import views
from core.serializers import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url('admin/', admin.site.urls),
    url("dev/", include(urls)),
    url(r'^$', views.index),
    url(r'^value-error$', views.value_error),
    url(r'^post-view$', views.post_view),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls'))
]
