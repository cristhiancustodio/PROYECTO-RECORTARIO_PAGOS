from flask_login import current_user
from User import User
from bd import BD
bd = BD("wallet")

class daoUsuarios:
    #Para la validacion de usuario
    @classmethod
    def verificar_usuario(self,user):
        row =  bd.sentencia_unica("call usp_Login('{}')".format(user.usuario))
        if row != None:
            user = User(row[0], row[1], row[2], row[3])
            return user
        else: 
            return None

    @classmethod
    def get_by_id(self,id) :
        row = bd.sentencia_unica("call usp_Login_by_id ({})".format(id))
        if row != None: 
            return User(row[0], row[1], None, row[2])
        else: 
            return None


    # Todo lo que hara el usuario como llenar algun formulario
    def registrar_usuario(self,usu,passw,nombre,apellido,telefono):
        bd.ejecutar("call usp_RegistrarUsuario('{}','{}','{}','{}','{}')".format(usu,passw,nombre,apellido,telefono))

    def registrar_cuenta_bancaria(self,usu,cod_banco,monto):
        bd.ejecutar("call usp_RegistrarCuentaBancaria ({},{},{})".format(usu,cod_banco,monto))
    
    def registrar_gastos(self,nombre,importe,moneda,fecha,tipo,id_usuario,categoria,cuenta):
        bd.ejecutar("call insertarGastos ('{}',{},'{}','{}','{}',{},{},{})".format(nombre,importe,moneda,fecha,tipo,id_usuario,categoria,cuenta))

    def actualizar_gastos(self,id_usuario,id_cuenta):
        bd.ejecutar("call actualizarSaldoCuentas({},{})".format(id_usuario,id_cuenta))

    def registrar_pagos(self,id_usuario,nombre,importe,moneda,fecha,notificacion,descripcion,tipo,id_categoria,frecuencia,periodo):
        bd.ejecutar("call usp_insertPagos({},'{}',{},'{}','{}','{}','{}','{}',{},'{}','{}')".format(id_usuario,nombre,importe,moneda,fecha,notificacion,descripcion,tipo,id_categoria,frecuencia,periodo))