
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from  usersManagements.views import LoginView
from rest_framework.authtoken.views import obtain_auth_token  # ✅ Import the obtain_auth_token view.   

schema_view = get_schema_view(
    openapi.Info(
        title="SIG-RML API",
        default_version='v1',
        description="Documentation de l'API de SIG-RML",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@sig-rml.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    #authentication_classes=[],  # 🔥 Désactive l'authentification (uniquement pour dev
)


urlpatterns = [
    path('admin/', admin.site.urls),
    
    #Mes applications
    path('api/Materiels/',include('materiels.urls')),
    path('api/Reservations/',include('reservations.urls')),
    path('api/Rapports/',include('Rapports.urls')),
    path('api/Laboratoire/',include('Laboratoire.urls')),
    path('api/Utilisateurs/',include('usersManagements.urls')),
    
    #login
    # Endpoint pour récupérer un token
    path('api/login/', LoginView.as_view(), name='api_login'),  
    # API documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # Redoc UI (optionnel)
    # API documentation en JSON / YAML
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),

]