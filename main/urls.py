from django.conf.urls import url
from . import views


app_name = 'inviter'
urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^signin/$', views.signin_view, name='login'),
    url(r'^signout/$', views.signout_view, name='logout'),
    url(r'^use-invite/(?P<code>\w+)$', views.use_invite_view,
        name='use_invite'),
]
