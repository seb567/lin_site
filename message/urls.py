from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
    path('manager_main', views.main, name='main'),
    path('start_tieba',views.start_tieba,name='start_tieba'),
    path('refresh',views.refresh,name='refresh'),
    path('save_last_pos/<str:pos>',views.savelastpos,name='savelastpos'),
    path('submit', views.submit_tieba_config, name='submit_tieba_config'),
    path('submit', views.submit_tieba_config, name='submit_tieba_config'),
    path('user_main', views.user_main, name='user_main'),
    path('search',views.search,name='search'),
    path('login',views.login,name='login'),
    path('gotoconfig',views.getConfig,name='gotoconfig'),
    path('usermanger',views.usermanger,name='usermanger'),
]