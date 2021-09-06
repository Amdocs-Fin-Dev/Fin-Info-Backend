
from django.urls import path
from .views import account_list, account_detail, portfolio_detail, portfolio_list, portifolio_add
urlpatterns = [
    path('api/', account_list),
    path('detail/<str:email>/',account_detail),
    path('portfolio/',portfolio_list),
    path('portfolio/<str:email>/',portfolio_list),
    path('newportfolio/<str:email>/',portfolio_detail),  #no funciona
    path('addfavorites/',portifolio_add),
    path('portfolio/<str:email>/<str:ticker>/',portfolio_list),
    
    
]