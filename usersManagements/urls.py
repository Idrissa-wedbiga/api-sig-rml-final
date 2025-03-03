from django.urls import path
from . views import(
    GetAllUsersView,
    UtilisateurDetailView,
    UtilisateurUpdateView,
    CreateUserView,
    UtilisateurDeleteView,
)

urlpatterns = [
    path('get_all_users/', GetAllUsersView.as_view(), name='get_all_users'),    
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('utilisateur/<int:pk>/', UtilisateurDetailView.as_view(), name='utilisateur_detail'),
    path('utilisateur/<int:pk>/update/', UtilisateurUpdateView.as_view(), name='utilisateur_update'),
    path('utilisateur/<int:pk>/delete/', UtilisateurDeleteView.as_view(), name='utilisateur_delete'),
    
   
]