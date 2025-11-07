from rest_framework import viewsets, status
from .models import Producto
from .serializers import ProductoSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db import transaction

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def stock_adjust(self, request, pk=None):
        delta = int(request.data.get('delta', 0))
        motivo = request.data.get('motivo','ajuste')
        with transaction.atomic():
            p = Producto.objects.select_for_update().get(pk=pk)
            if p.stock + delta < 0:
                return Response({'error':'stock insuficiente'}, status=status.HTTP_400_BAD_REQUEST)
            p.stock += delta
            p.save()
        return Response({'stock': p.stock})
