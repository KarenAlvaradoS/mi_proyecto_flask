from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import Usuario

# Inicializo mi app Flask
app = Flask(__name__)
app.secret_key = "mi_clave_secreta"  # esto lo necesito para las sesiones

# Configuro Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # si no hay login, redirige a la página de login

# Esta función carga el usuario por su id, necesaria para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    usuarios = Usuario.obtener_todos()
    for u in usuarios:
        if u['id_usuario'] == int(user_id):
            return Usuario(u['id_usuario'], u['nombre'], u['email'], u['password'])
    return None

# -----------------------------
# RUTAS
# -----------------------------

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Dashboard protegido (solo para usuarios logueados)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', nombre=current_user.nombre)

# Ruta para iniciar sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        usuario = Usuario.obtener_por_mail(email)
        if usuario and usuario.password == password:
            login_user(usuario)  # logueo al usuario
            return redirect(url_for('dashboard'))
        else:
            flash("Usuario o contraseña incorrectos")  # mensaje de error
            return redirect(url_for('login'))
    return render_template('login.html')

# Ruta para registrar un nuevo usuario
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        if Usuario.obtener_por_mail(email):  # verifico que no esté registrado
            flash("El email ya está registrado")
            return redirect(url_for('registro'))
        Usuario.registrar(nombre, email, password)  # registro nuevo usuario
        flash("Usuario registrado correctamente")
        return redirect(url_for('login'))
    return render_template('registro.html')

# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada")
    return redirect(url_for('index'))

# -----------------------------
# EJECUTAR SERVIDOR
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
