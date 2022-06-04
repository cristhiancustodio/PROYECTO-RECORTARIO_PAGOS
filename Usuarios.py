from unicodedata import name

from click import password_option


class Usuarios:
    '''con un * accederas a una lista de funciones .
       con dos ** accederas a un diccionario'''
    #usuarios = [names,user,password,phone,last_name]
    def __init__(self,*usuarios) -> None:
        self.name = name
        self.user = user
        self.password = password
        self.phone = phone
        self.las_name = last_name
        
