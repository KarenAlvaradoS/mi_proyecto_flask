from flask import Flask, request, render_template, redirect, url_for, session
from models import Usuario

app = Flask(__name__)
app.secret_key = "clave_secreta"  # Necesario para manejar sesiones de usuario

# -------------------------------
# Página de inicio
# -------------------------------
@app.route('/')
def index():
    # Simple página de bienvenida con enlaces a registro y login
    return render_template('index.html')


# -------------------------------
# Registro de usuario
# -------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Tomo los datos que ingresó el usuario
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        # Verifico que el email no esté registrado
        if Usuario.obtener_por_mail(email):
            return "El email ya está registrado"

        # Si no existe, registro el usuario
        Usuario.registrar(nombre, email, password)
        return redirect(url_for('login'))  # Después voy al login

    # Si es GET, muestro el formulario
    return render_template('register.html')


# -------------------------------
# Login de usuario
# -------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        usuario = Usuario.obtener_por_mail(email)  # Busco el usuario por email
        if usuario and usuario.password == password:
            # Creo la sesión para recordar al usuario
            session['usuario_id'] = usuario.id_usuario
            session['usuario_nombre'] = usuario.nombre
            return redirect(url_for('dashboard'))
        else:
            # Si no coincide, muestro error
            return "Email o contraseña incorrectos"

    # Si es GET, muestro el formulario de login
    return render_template('login.html')


# -------------------------------
# Dashboard
# -------------------------------
@app.route('/dashboard')
def dashboard():
    # Verifico que el usuario haya iniciado sesión
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    # Muestro la página principal del usuario con su nombre
    return render_template('dashboard.html', nombre=session['usuario_nombre'])


# -------------------------------
# Ver todos los usuarios
# -------------------------------
@app.route('/ver_usuarios')
def ver_usuarios():
    # Solo usuarios logueados pueden ver la lista
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    usuarios = Usuario.obtener_todos()  # Traigo todos los usuarios
    return render_template('ver_usuarios.html', usuarios=usuarios)


# -------------------------------
# Cerrar sesión
# -------------------------------
@app.route('/logout')
def logout():
    # Limpio la sesión para cerrar sesión
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    # Arranco la app en modo debug
    app.run(debug=True)
