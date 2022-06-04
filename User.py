from flask_login import UserMixin
# para la autenticacion de usuario
class User(UserMixin):
    def __init__(self,id,usuario,contraseña,nombre) -> None:
        self.id = id
        self.usuario = usuario
        self.contraseña = contraseña
        self.nombre = nombre
    
