from rest_framework import viewsets, status
from .models import Pedido, DetallePedido
from .serializers import PedidoSerializer, DetalleSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from inventario.models import Producto

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all().prefetch_related('detalles')
    serializer_class = PedidoSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        cliente_id = data.get('cliente')
        items = data.get('items', [])
        with transaction.atomic():
            pedido = Pedido.objects.create(cliente_id=cliente_id, estado='PENDIENTE', total=0)
            total = 0
            for it in items:
                prod = Producto.objects.select_for_update().get(pk=it['producto'])
                if prod.stock - prod.stock_reservado < int(it['cantidad']):
                    raise Exception('Stock insuficiente')
                precio = prod.precio
                subtotal = precio * int(it['cantidad'])
                DetallePedido.objects.create(pedido=pedido, producto=prod, cantidad=int(it['cantidad']), precio_snapshot=precio, subtotal=subtotal)
                prod.stock_reservado += int(it['cantidad'])
                prod.save()
                total += subtotal
            pedido.total = total
            pedido.save()
        serializer = PedidoSerializer(pedido)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def pay(self, request, pk=None):
        pedido = self.get_object()
        with transaction.atomic():
            if pedido.estado != 'PENDIENTE':
                return Response({'error':'estado no válido'}, status=status.HTTP_400_BAD_REQUEST)
            pedido.estado = 'PAGADO'
            pedido.save()
            for det in pedido.detalles.all():
                prod = Producto.objects.select_for_update().get(pk=det.producto_id)
                if prod.stock < det.cantidad:
                    raise Exception('Stock insuficiente al pagar')
                prod.stock -= det.cantidad
                prod.stock_reservado = max(0, prod.stock_reservado - det.cantidad)
                prod.save()
        return Response({'status':'pagado'})
