-- Trigger BEFORE INSERT para DetallePedido: fijar precio_snapshot y subtotal
CREATE OR REPLACE FUNCTION fn_set_precio_subtotal() RETURNS trigger AS $$
BEGIN
    NEW.precio_snapshot := (SELECT precio FROM inventario_producto WHERE id = NEW.producto_id);
    NEW.subtotal := NEW.precio_snapshot * NEW.cantidad;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_detalle_before_insert ON pedidos_detallepedido;
CREATE TRIGGER trg_detalle_before_insert
BEFORE INSERT ON pedidos_detallepedido
FOR EACH ROW EXECUTE FUNCTION fn_set_precio_subtotal();
