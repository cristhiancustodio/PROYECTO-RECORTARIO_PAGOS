from time import strftime
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
#MODELO WALLET
#importo mis clases de los otros archivos
from daoWallet import * 
from daoUsuarios import *
from User import User


app = Flask(__name__)
csrf = CSRFProtect()
login_manager_app = LoginManager(app)
app.secret_key = "B!1w8NAt1T^%kvhUI*S^"


daowallet = daoWallet()
daousuario = daoUsuarios()
#Errores de la web
@app.errorhandler(401)
def page_not_found(error):
    return redirect(url_for("login"))

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", error = error)

@app.errorhandler(500)
def error_server(error):
    return render_template("500.html",error = error)


# Inicio de sesión 
@login_manager_app.user_loader
def load_user(id):
    return daousuario.get_by_id(id)

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login",methods = ["GET","POST"])
def login():
    if request.method == "POST":
        usuario = request.form["txtusuario"]
        contraseña = request.form["txtpassword"]
        user = User(0,usuario,contraseña,None)
        logged_user = daousuario.verificar_usuario(user)
        if logged_user != None:
            if logged_user.contraseña == contraseña:
                print("Accedido")
                login_user(logged_user)
                return redirect(url_for("menu"))
            else:
                flash("Contraseña invalida")
                return render_template("login.html")
        else:
            flash("Usuario no encontrado")
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))        



#Crear cuenta
@app.route("/crear_cuenta",methods=["POST"])
def crear_cuenta():
    usuario = request.form["txtusuario"]
    contraseña = request.form["txtpassword"]
    nombre = request.form["txtnombre"]
    apellido = request.form["txtapellido"]
    telefono = request.form["txttelefono"]
    print(usuario,contraseña,nombre,apellido,telefono)
    daousuario.registrar_usuario(usuario,contraseña,nombre,apellido,telefono)
    return redirect(url_for("login"))

@app.route("/registro_banco", methods = ["POST"])
def registro_banco():
    banco = request.form["select_banco"]
    monto =  float(request.form["txtmonto"])
    moneda = request.form["moneda"]
    if moneda == "soles":
        monto = monto
    elif moneda == "dolares":
        monto = monto*3.80
    elif moneda =="euros":
        monto = monto*4.50
    daousuario.registrar_cuenta_bancaria(current_user.id,banco,monto)
    return redirect(url_for("historial"))

@app.route('/registrar_gastos', methods = ["POST"])
@login_required
def registrar_gastos():
    nombre = request.form["txtnombre"]
    cuenta = int(request.form["banco"])
    categoria= int(request.form["categoria"])
    importe = float(request.form["txtimporte"])
    moneda = request.form["moneda"]
    fecha = request.form["fecha"]
    tipo = request.form["operacion"]
    id_usuario = current_user.id
    daousuario.registrar_gastos(nombre,importe,moneda,fecha,tipo,id_usuario,categoria,cuenta)
    daousuario.actualizar_gastos(current_user.id,cuenta)
    return redirect(url_for("historial"))

@app.route('/registrar_pagos', methods = ["POST"])
@login_required
def registrar_pagos():
    id_usuario = current_user.id
    nombre = request.form["txtnombre"]
    importe = request.form["txtimporte"]
    moneda = request.form["moneda"]
    fecha = request.form["fecha"]
    notificacion = request.form["notificacion"]
    descripcion = request.form["txtarea"]
    tipo = request.form["operacion"]
    id_categoria = request.form["categoria"]
    frecuencia = request.form["frecuencia"]
    if frecuencia == "F-2":
        periodo = request.form["periodo"]
    elif frecuencia == "F-1":
        periodo = ""
    daousuario.registrar_pagos(id_usuario,nombre,importe,moneda,fecha,notificacion,descripcion,tipo,id_categoria,frecuencia,periodo)
    return redirect(url_for("historial"))


@app.route('/ver_mas_gastos')
def ver_mas_gastos():
    movimientos = daoWallet.obtener_todos_movimientos(current_user.id)
    return render_template("historial.html",movimientos = movimientos)

#El sistema
@app.route("/gastos")
@login_required
def gastos():
    categorias = daoWallet.obtener_categoria()
    cuentas = daoWallet.obtener_cuentas_abiertas(current_user.id)
    fecha = strftime('%Y-%m-%d')
    return render_template("gastos.html",categorias = categorias,cuentas = cuentas,fecha = fecha)

@app.route("/pagos")
@login_required
def pagos():
    categorias = daoWallet.obtener_categoria()
    notificaciones = daoWallet.obtener_notificacion()
    periodos = daoWallet.obtener_periodos()
    cuentas = daoWallet.obtener_cuentas_abiertas(current_user.id)
    fecha = strftime('%Y-%m-%d')
    return render_template("pagos.html",categorias = categorias,notificaciones=notificaciones,cuentas = cuentas,periodos = periodos,fecha = fecha)

@app.route("/banco")
@login_required
def banco():
    bancos = daoWallet.obtener_bancos()
    return render_template("banco.html",bancos = bancos)

@app.route("/historial")
@login_required
def historial():
    movimientos = daoWallet.obtener_ultimos_movimientos(current_user.id)
    proximos_pagos = daoWallet.obtener_proximo_pago(current_user.id)
    cuentas = daoWallet.obtener_cuentas_abiertas(current_user.id)
    return render_template("historial.html",cuentas = cuentas,movimientos = movimientos, proximos_pagos = proximos_pagos)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/menu")
@login_required
def menu():
    return render_template("menu.html")



if __name__ == '__main__':
    csrf.init_app(app)
    app.run(debug=True, port=3000)