from django.urls import path
from .views import stock_list, ticker_list, TickerAPIView, TickerDetails, TickerMostrar, TickerMostrarMonth,TickerMostrarWeek,TecnicalAnalisis
#from .views import TickerAPIView, TickerDetails, TickerMostrar
urlpatterns = [
    path('show/<str:ticker_id>', ticker_list), 
    path('ticker/', TickerAPIView.as_view()),
    path('api/<str:ticker_id>', TickerDetails.as_view()),
    path('mostrar/<str:ticker_id>/<str:interval>/<str:period>', TickerMostrar.as_view()),
    # path('mostrar', TickerMostrar.as_view()),
    path('mostrar/w', TickerMostrar.as_view()),
    path('line/w', TickerMostrarWeek.as_view()),
    path('line/m', TickerMostrarMonth.as_view()),
    path('analisis/<str:ticker>/<str:flag>',TecnicalAnalisis.as_view()),
    path('search/<str:patterMatch>', stock_list)
]


#/<str:interval>