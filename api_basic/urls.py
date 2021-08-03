from django.urls import path
from .views import ticker_list, TickerAPIView, TickerDetails, TickerMostrar, TickerMostrarMonth,TickerMostrarWeek
#from .views import TickerAPIView, TickerDetails, TickerMostrar
urlpatterns = [
    path('show/<str:ticker_id>', ticker_list), 
    path('ticker/', TickerAPIView.as_view()),
    path('detail/<str:ticker_id>', TickerDetails.as_view()),
    path('mostrar/<str:ticker_id>/<str:interval>', TickerMostrar.as_view()),
    # path('mostrar', TickerMostrar.as_view()),
    path('mostrar/w', TickerMostrar.as_view()),
    path('line/w', TickerMostrarWeek.as_view()),
    path('line/m', TickerMostrarMonth.as_view())
    
]


#/<str:interval>