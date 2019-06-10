#from .views import Drivers
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import DriverPofile,Login
urlpatterns=[
    path('profile/',DriverPofile.as_view()),
    path('login/',Login.as_view())
    #path('add/<int:pk>/', Drivers.as_view())

]
urlpatterns = format_suffix_patterns(urlpatterns)
