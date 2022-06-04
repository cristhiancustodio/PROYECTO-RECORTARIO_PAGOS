/*drop database wallet;*/
create database wallet;

use wallet;
/*TABLAS PREVIAMENTE LLENADAS*/
create table BANCOS(
	codBanco int primary key auto_increment not null,
    banco varchar(50) not null unique
);
alter table BANCOS auto_increment = 10;
insert into BANCOS(banco) values("BBVA Continental"),("BCP"),("Interbank"),("Scotiabank"),("Banco de la Nación");

create table FRECUENCIAS(
	frecuencia varchar(50) primary key not null,
    nomina varchar(45) not null
);

insert into FRECUENCIAS values("F-1","Una vez"),("F-2","Pago recurrente");

create table PERIODOS(
	periodo varchar(50) primary key not null,
    dias int not null
);

insert into PERIODOS values("Diario",1),("Semanal",7),("Quincenal",15),("Mensual",30),("Semestral",60);

create table NOTIFICACIONES(
	notificacion varchar(50) primary key not null,
    dias int not null
);
insert into NOTIFICACIONES values("Ninguno", 0),("Un dia Antes",1),("Tres dias antes",3),("Una semana antes",7);

create table CATEGORIAS(
	idCategoria int primary key not null auto_increment,
    nombre_categoria varchar(50)
);
alter table CATEGORIAS auto_increment = 100;
insert into CATEGORIAS (nombre_categoria) values("Comidas y Bebidas"),
("Compras"),
("Vivienda"),
("Transporte"),
("Educación"),
("Vestimenta"),
("Tecnologia"),
("Salud"),("Ocio"),("Otros");

create table USUARIOS(
	idUsuario int primary key not null auto_increment,
    usuario varchar(45) not null unique ,
    contraseña varchar(255) not null,
    nombre varchar(45) not null,
    apellido varchar(45) not null,
    telefono varchar(45) not null
);

create table CUENTAS(
	idCuenta int primary key not null auto_increment,
    idUsuario int,
    codBanco int,
    monto DECIMAL(7,2),
    foreign key(idUsuario) references USUARIOS(idUsuario)
    on delete cascade
    on update cascade,
    foreign key(codBanco) references BANCOS(codBanco)
    on delete cascade
    on update cascade
);

create table PAGOS(
	idPago int primary key not null auto_increment,
    idUsuario int not null,
    nombre varchar(45) not null,
    importe DECIMAL(7,2) not null,
    moneda varchar(45) not null,
    fecha_inicio date,
    notificacion varchar(45) not null,
    descripcion varchar(45) not null,
    tipo varchar(45) not null check(tipo="gastos" or tipo = "ingresos"),
    idCategoria int not null,
    frecuencia varchar(45) not null,
    periodo varchar(45) not null,
    foreign key(idUsuario) references USUARIOS(idUsuario) on delete cascade on update cascade,
    foreign key(idCategoria) references CATEGORIAS(idCategoria) on delete cascade on update cascade ,
    foreign key(frecuencia) references FRECUENCIAS(frecuencia)on delete cascade on update cascade,
    foreign key(periodo) references PERIODOS(periodo)on delete cascade on update cascade,
    foreign key(notificacion) references NOTIFICACIONES(notificacion)on delete cascade on update cascade
);

create table MOVIMIENTOS(
	idGastos int not null primary key auto_increment,
    nombre varchar(45) not null,
    importe DECIMAL(7,2) not null,
    moneda varchar(45) not null,
    fecha_inicio date,
    tipo varchar(45) not null check(tipo="gastos" or tipo = "ingresos"),
	idUsuario int not null,
	idCategoria int not null,
    idCuenta int not null,
    foreign key(idUsuario) references USUARIOS(idUsuario) on delete cascade on update cascade,
    foreign key(idCategoria) references CATEGORIAS(idCategoria) on delete cascade on update cascade,
    foreign key(idCuenta) references CUENTAS(idCuenta) on delete cascade on update cascade
	
);

create table HISTORIAL_PAGOS(
	cod_historial_pagos int not null primary key auto_increment,
    idUsuario int not null,
    idPago int not null,
    subtotal DECIMAL(7,2) not null,
    foreign key(idUsuario) references USUARIOS(idUsuario) on delete cascade on update cascade,
    foreign key(idPago) references PAGOS(idPago) on delete cascade on update cascade
);

create table HISTORIAL_MOVIMIENTOS(
	cod_historial_movimientos int not null primary key auto_increment,
    idUsuario int not null,
    idGastos int not null,
    subtotal DECIMAL(7,2) not null,
    foreign key(idUsuario) references USUARIOS(idUsuario) on delete cascade on update cascade,
    foreign key(idGastos) references MOVIMIENTOS(idGastos)on delete cascade on update cascade
);

create table ALERTAS (
	idNotificacion int not null primary key auto_increment,
    idUsuario int not null,
	frecuencia	varchar(50) not null,
    periodo varchar(50) not null,
    notificacion varchar(50) not null,
    fecha_inicio date not null,
    
    foreign key(idUsuario) references USUARIOS(idUsuario) on delete cascade on update cascade,
    foreign key(frecuencia) references FRECUENCIAS(frecuencia) on delete cascade on update cascade,
    foreign key(periodo) references PERIODOS(periodo) on delete cascade on update cascade,
    foreign key(notificacion) references NOTIFICACIONES(notificacion) on delete cascade on update cascade
);




/*PROCEDIMIENTOS ALMACENADOS*/

create procedure usp_Login(
in _usuario varchar(25))
select * from usuarios where usuario = _usuario;
call usp_Login('Custox06');

create procedure usp_Login_by_id(
in id_usuario int)
select idUsuario,usuario,nombre from usuarios where idUsuario = id_usuario;


create procedure usp_RegistrarUsuario(
in _usuario varchar(25), 
in _contraseña varchar(25),
in _nombre varchar(25),
in _apellido varchar(25),
in _telefono varchar(25))
insert into usuarios values(null,_usuario,_contraseña,_nombre,_apellido,_telefono);

create procedure usp_RegistrarCuentaBancaria
(in _idUsuario int,
in _codbanco int,
in _monto DECIMAL(7,2))
insert into cuentas values(null,_idUsuario,_codbanco,_monto);

create procedure verCuentasAbiertas (in _idUsuario int)
select bancos.codBanco, bancos.banco,cuentas.monto,cuentas.idCuenta from bancos 
inner join cuentas on bancos.codBanco = cuentas.codBanco
where idUsuario = _idUsuario;

call verCuentasAbiertas(2);
create procedure insertarGastos(
in _nombre varchar(45),
in _importe DECIMAL(7,2),
in _moneda varchar(45),
in _fecha date,
in _tipo varchar(45),
in _id_usuario int,
in _idCategoria int,
in _idCuenta int)
    insert into MOVIMIENTOS values(null,_nombre,_importe,_moneda,_fecha,_tipo,_id_usuario,_idCategoria,_idCuenta);
    
create procedure usp_insertPagos(
in id_usuario int,
in nombre varchar(45),
in importe decimal(7,2),
in moneda varchar(50),
in fecha date,
in notificacion varchar(50),
in descripcion varchar(50),
in tipo varchar(25),
in id_categoria int,
in frecuencia varchar(25),
in periodo varchar(25))
insert into pagos values (null,id_usuario,nombre,importe,moneda,fecha,notificacion,descripcion,tipo,id_categoria,frecuencia,periodo);
    
create procedure usp_verMovimientos(
in id_usuario int )
	select categorias.nombre_categoria,movimientos.nombre,movimientos.importe,movimientos.fecha_inicio,movimientos.tipo 
	from movimientos inner join categorias on categorias.idCategoria = movimientos.idCategoria
	where idusuario = id_usuario order by movimientos.fecha_inicio desc;

create procedure actualizarSaldoCuentas(
in id_usuario int, 
in id_cuenta int)
	update cuentas set monto = subtotal_movimientos(id_cuenta) where idUsuario = id_usuario and idCuenta = id_Cuenta;

create procedure usp_verUltimosMovimientos(
in id_usuario int )
select categorias.nombre_categoria,movimientos.nombre,movimientos.importe,movimientos.fecha_inicio,movimientos.tipo 
from movimientos inner join categorias on categorias.idCategoria = movimientos.idCategoria
where idusuario = id_usuario order by movimientos.fecha_inicio desc limit 3;


create procedure usp_verProximosPagos(in id_usuario int)
select pagos.nombre, pagos.importe, categorias.nombre_categoria, date_format(pagos.fecha_inicio,"%e-%b") as fechas, pagos.tipo
from pagos inner join categorias on pagos.idCategoria = categorias.idCategoria where idUsuario = id_usuario;

