from django.urls import path
from .views import *

urlpatterns = [
    # http://127.0.0.1:8000/twitter/test
    path('test', twitter_test)
]
