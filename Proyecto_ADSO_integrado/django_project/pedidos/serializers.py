from rest_framework import serializers
from .models import Pedido, DetallePedido

class DetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = ['id','producto','cantidad','precio_snapshot','subtotal']

class PedidoSerializer(serializers.ModelSerializer):
    detalles = DetalleSerializer(many=True, read_only=True)
    class Meta:
        model = Pedido
        fields = ['id','cliente','total','estado','metodo_pago','detalles','creado_en']
