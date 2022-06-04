use wallet;

delimiter //
create function subtotal_movimientos(id_cuenta int ) returns float
DETERMINISTIC
READS SQL DATA
begin
	declare sub_total float;
	select (cuentas.monto-movimientos.importe) into sub_total 
	from movimientos inner join cuentas on movimientos.idCuenta = cuentas.idCuenta 
    where movimientos.idCuenta = id_cuenta 
    order by movimientos.idGastos DESC LIMIT 1;
    return sub_total;
end //
delimiter ;

-- select subtotal_movimientos(1)




 