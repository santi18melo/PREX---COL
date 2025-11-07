from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventario import api as inventario_api
from pedidos import api as pedidos_api

router = DefaultRouter()
router.register('productos', inventario_api.ProductViewSet, basename='producto')
router.register('pedidos', pedidos_api.OrderViewSet, basename='pedido')

urlpatterns = [
    path('', include(router.urls)),
]
