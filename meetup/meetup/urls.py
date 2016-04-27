from django.conf.urls import url, include
from rest_framework import routers

from todo import views as todo_views

router = routers.DefaultRouter()
router.register(r'todos', todo_views.TodoViewSet, base_name='todo')


urlpatterns = [
    url(r'^$', todo_views.index, name='index'),
    url(r'^login/$', todo_views.login, name='login'),
    url(r'^logout/$', todo_views.logout, name='logout'),
    url(r'^api/', include(router.urls)),
]
