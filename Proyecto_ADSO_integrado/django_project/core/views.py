from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from pedidos.models import Pedido
from inventario.models import Producto
from clientes.models import Usuario


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Añadir contexto para usuarios autenticados si es necesario
            pass
        return context


@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class AdminHomeView(TemplateView):
    template_name = 'core/admin_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadir estadísticas para el panel de administración
        context['pedidos_pendientes'] = (
            Pedido.objects.filter(estado='pendiente').count()
        )
        context['clientes_activos'] = (
            Usuario.objects.filter(is_active=True).count()
        )
        context['total_productos'] = Producto.objects.count()
        
        # Últimos 5 pedidos
        context['ultimos_pedidos'] = (
            Pedido.objects.select_related('usuario')
            .order_by('-fecha_pedido')[:5]
        )
        
        # Productos con bajo stock
        context['productos_bajo_stock'] = (
            Producto.objects.filter(stock_actual__lte=10)
            .order_by('stock_actual')[:5]
        )
        
        return context
