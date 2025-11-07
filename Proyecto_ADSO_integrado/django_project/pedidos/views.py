from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from pedidos.models import Pedido, Producto, Cliente  # ajusta los modelos según tu app

# Solo permite acceso a usuarios staff
def staff_required(user):
    return user.is_staff

@login_required
@user_passes_test(staff_required)
def admin_home(request):
    # Datos de ejemplo: cámbialos según tus modelos reales
    pedidos_pendientes = Pedido.objects.filter(estado='pendiente').count()
    clientes_activos = Cliente.objects.filter(activo=True).count()
    total_productos = Producto.objects.count()

    ultimos_pedidos = Pedido.objects.order_by('-fecha_creacion')[:5]
    productos_bajo_stock = Producto.objects.filter(stock_actual__lte=models.F('stock_minimo'))

    contexto = {
        'pedidos_pendientes': pedidos_pendientes,
        'clientes_activos': clientes_activos,
        'total_productos': total_productos,
        'ultimos_pedidos': ultimos_pedidos,
        'productos_bajo_stock': productos_bajo_stock,
    }
    return render(request, 'admin_home.html', contexto)
