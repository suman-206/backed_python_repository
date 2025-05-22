from django.urls import path
from . import views
from .views import Registration, Login

urlpatterns=[
    path("",views.index,name="index"),
    path('registration/', Registration.as_view(), name='registration'),
    path('login/',Login.as_view(), name='login'),

]