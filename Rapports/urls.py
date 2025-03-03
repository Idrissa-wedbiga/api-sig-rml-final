from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . views import (
    RapportListAPIView,
    RapportDetailAPIView,
    RapportCreateAPIView,
    RapportUpdateAPIView,
    RapportDeleteAPIView,   
    HistoriqueListAPIView,
    HistoriqueDetailAPIView,
    HistoriqueCreateAPIView,
    HistoriqueUpdateAPIView,
    HistoriqueDeleteAPIView,
    
)

urlpatterns = [
    path('rapports/', RapportListAPIView.as_view(), name='liste_rapports'),
    path('rapports/<int:pk>/', RapportDetailAPIView.as_view(), name='detail_rapport'),
    path('rapports/create/', RapportCreateAPIView.as_view(), name='creer_rapport'),
    path('rapports/<int:pk>/update/', RapportUpdateAPIView.as_view(), name='modifier_rapport'),
    path('rapports/<int:pk>/delete/', RapportDeleteAPIView.as_view(), name='supprimer_rapport'),
    path('historiques/', HistoriqueListAPIView.as_view(), name='liste_historiques'),
    path('historiques/<int:pk>/', HistoriqueDetailAPIView.as_view(), name='detail_historique'),
    path('historiques/create/', HistoriqueCreateAPIView.as_view(), name='creer_historique'),
    path('historiques/<int:pk>/update/', HistoriqueUpdateAPIView.as_view(), name='modifier_historique'),
    path('historiques/<int:pk>/delete/', HistoriqueDeleteAPIView.as_view(), name='supprimer_historique'),
    
]