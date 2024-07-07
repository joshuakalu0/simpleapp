from django.urls import path
from userauth.views import RegisterView,MyTokenObtainPairView
app_name='auth'
urlpatterns = [
    path('register',RegisterView.as_view(),name='signup'),
    path('login',MyTokenObtainPairView.as_view(),name='signin'),

]
