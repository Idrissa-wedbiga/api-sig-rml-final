from django.urls import path
from . views import CreateLaboratoireAPIView, LaboratoireListAPIView, LaboratoireDetailAPIView, LaboratoireUpdateAPIView,LaboratoireDeleteAPIView

urlpatterns = [
    path('creer/', CreateLaboratoireAPIView.as_view(), name='creer_laboratoire'),
    path('liste/', LaboratoireListAPIView.as_view(), name='liste_laboratoires'),
    path('detail/<int:pk>/', LaboratoireDetailAPIView.as_view(), name='detail_laboratoire'),
    path('modifier/<int:pk>/', LaboratoireUpdateAPIView.as_view(), name='modifier_laboratoire'),
    path('supprimer/<int:pk>/', LaboratoireDeleteAPIView.as_view(), name='supprimer_laboratoire'),
]