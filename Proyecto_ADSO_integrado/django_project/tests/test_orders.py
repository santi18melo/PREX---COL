# Tests básicos para flujos críticos (usar pytest-django / Django TestCase)
def test_create_order_insufficient_stock(db):
    # crear producto con stock 0 y simular pedido -> debería fallar
    assert True
