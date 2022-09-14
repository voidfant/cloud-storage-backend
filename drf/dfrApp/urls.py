from django.urls import path, re_path
from .views import *


app_name = 'element'
urlpatterns = [
    path('imports', importApi),
    re_path('^nodes/(?P<elementId>.+)$', nodesApi),
    re_path('^delete/(?P<elementId>.+)$', deleteApi)
]