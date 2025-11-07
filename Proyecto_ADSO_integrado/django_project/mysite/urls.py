from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URLs de Django Admin
    path('admin/', admin.site.urls),
    path('admin-panel/', views.admin_home, name='admin_home'),
]
    # URLs de la API
    path('api/', include('core.api_urls')),
    path('api/auth/', include('clientes.auth_urls')),
    
    # URLs del frontend
    path('', include('core.urls')),  # URLs principales/home
    path('clientes/', include('clientes.auth_urls')),  # URLs de autenticación
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
