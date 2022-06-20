from django.urls import path, include
from rest_framework import routers

from . import views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'api/questions', views.QuestionViewSet,)


app_name = 'polls'
urlpatterns = [
    path('', include(router.urls)),
    path('', views.IndexView.as_view(), name='index'),
]

urlpatterns += [
    path('api/api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]