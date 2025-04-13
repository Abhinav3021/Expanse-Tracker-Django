from django.urls import path
from tracker.views import index, deleteTransaction, registration,login_page,logout_page

urlpatterns=[
    path('',index,name="index"),
    path('delete-tranaction/<uuid>/',deleteTransaction,name='deleteTransaction'),
    path('registration/',registration, name='registation'),
    path('login/',login_page, name="login_page"),
    path('logout/',logout_page,name='logout_page')
]