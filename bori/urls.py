from django.conf.urls import url
from django.urls import path
from bori import views
from .views import RcmdNewsListView
from .views import RcmdNewsListAPI, RcmdDetailAPI


urlpatterns = [
    
    path('rcmdNews/', RcmdNewsListAPI.as_view() ),
    path('rcmdNews<int:pk>/', RcmdDetailAPI.as_view()),
    
    url(r'^head', views.head),
    url(r'^rcmd', views.rcmd),

]