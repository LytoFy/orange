from django.urls import path, include

from Relative.views import index

urlpatterns = [
        path('index',index,name='index')
]