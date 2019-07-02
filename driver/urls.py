#from .views import Drivers
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (DriverPofile,Login,ActiveLogin,ActiveDrivers, RideCreationView)

urlpatterns=[
    path('profile/',DriverPofile.as_view()),
    path('login/',Login.as_view()),
    path('active/', ActiveLogin.as_view()),
    path('active_drivers/',ActiveDrivers.as_view()),
    path('rides/',RideCreationView.as_view())

]
urlpatterns = format_suffix_patterns(urlpatterns)
