from django.urls import path

from . views import AjouterMaterielView, ListeMaterielsView, ListeMaterielIdView, ModifierMaterielView, SupprimerMaterielView


urlpatterns = [
    
        path('ajouter/', AjouterMaterielView.as_view(), name='ajouter_materiel'),
        path('liste/', ListeMaterielsView.as_view(), name='liste_materiels'),
        path('liste/<int:pk>/', ListeMaterielIdView.as_view(), name='liste_materiel_id'),
        path('modifier/<int:pk>/', ModifierMaterielView.as_view(), name='modifier_materiel'),
        path('supprimer/<int:pk>/', SupprimerMaterielView.as_view(), name='supprimer_materiel'),
        

]