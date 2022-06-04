import pymysql


class BD:
    def __init__(self,base_datos) :
        self.base_datos = base_datos
    try:
        def obtener_conexion(self):
            conexion = pymysql.connect(host="127.0.0.1",port=3307,user="root",passwd="luisnunura123456",db=self.base_datos)
            return conexion
        print("Conectado exitosamente")
    except:
        print("Error en conexion a base de datos")
    #para obtener datos (select)

    #en la funcion sentencia, trae varias filas con matriz bidimensional en forma de tupla
    def sentencia(self,sql):
        conexion = BD.obtener_conexion(self)
        datos = []
        with conexion.cursor() as cursor:
            cursor.execute(sql)
            datos = cursor.fetchall()
            if datos != None:
                return datos 
            else:
                return None
        
    # en esta funcion solo trae una fila con una tupla simple  
    def sentencia_unica(self,sql):
        conexion = BD.obtener_conexion(self)
        datos = []
        with conexion.cursor() as cursor:
            cursor.execute(sql)
            datos = cursor.fetchone()
            if datos !=None:
                return datos   
            else:
                return None
    #para hacer modificaciones a la tabla(insert,update, delete)
    def ejecutar(self,sql):
        conexion = BD.obtener_conexion(self)
        with conexion.cursor() as cursor:
            cursor.execute(sql)
        conexion.commit()
        conexion.close()
