from bd import BD

#cuando se hace alguna modificacion a la tabla como insert, delete, updata usamos el
#conexion.commit() antes de cerrar nuestra conexion

#y si queremos hacer una consulta y traer datos simplemente cerramos la conexion, pero antes un fetchall()

bd = BD("wallet")

class daoWallet:

    def obtener_bancos():
        consulta = bd.sentencia("select * from bancos order by codbanco asc;")
        return consulta

    def obtener_categoria():
        consulta = bd.sentencia("select* from categorias")
        return consulta
    def obtener_frecuencia():
        consulta = bd.sentencia("select* from frecuencias")
        return consulta
        
    def obtener_notificacion():
        return bd.sentencia("select* from frecuencias")

    def obtener_periodo():
        return bd.sentencia("select* from periodos")

    def obtener_cuentas_abiertas(id_usuario):
        return bd.sentencia("call verCuentasAbiertas({})".format(id_usuario))

    def obtener_periodos():
        return bd.sentencia("select * from periodos")

    def obtener_ultimos_movimientos(id_usuario):
        return bd.sentencia("call usp_verUltimosMovimientos({})".format(id_usuario))

    def obtener_todos_movimientos(id_usuario):
        return bd.sentencia("call usp_verMovimientos({})".format(id_usuario))
    
    def obtener_proximo_pago(id_usuario):
        return bd.sentencia("call usp_verProximosPagos({})".format(id_usuario))
