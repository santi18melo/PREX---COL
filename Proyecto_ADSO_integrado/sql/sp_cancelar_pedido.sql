-- Procedure para cancelar pedido y devolver stock (PostgreSQL style)
CREATE OR REPLACE FUNCTION sp_cancelar_pedido(pid bigint, motivo text) RETURNS void AS $$
DECLARE
    rec record;
BEGIN
    UPDATE pedidos_pedido SET estado='CANCELADO', actualizado_en = now() WHERE id = pid AND estado <> 'CANCELADO';
    FOR rec IN SELECT producto_id, cantidad FROM pedidos_detallepedido WHERE pedido_id = pid LOOP
        UPDATE inventario_producto SET stock = stock + rec.cantidad WHERE id = rec.producto_id;
        INSERT INTO inventario_stockmovimientos(producto_id, cambio, motivo, referencia_id, creado_en)
        VALUES (rec.producto_id, rec.cantidad, motivo, pid, now());
    END LOOP;
END;
$$ LANGUAGE plpgsql;
