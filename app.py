from Conexion.conexion import obtener_conexion
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# -------------------------------
# Rutas HTML
# -------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return render_template('usuario.html', nombre=nombre)

@app.route('/about')
def about():
    return render_template('about.html')


# -------------------------------
# NUEVAS RUTAS: MySQL y CRUD
# -------------------------------

# Ruta para probar la conexión a la base de datos
@app.route('/test_db')
def test_db():
    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT DATABASE();")
                resultado = cursor.fetchone()
        return f"Conectado a la base de datos: {resultado[0]}"
    except Exception as e:
        return {"error": str(e)}, 500


# Ruta: listar todos los usuarios
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        with obtener_conexion() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id_usuario, nombre, mail FROM usuarios")
                rows = cursor.fetchall()
        return jsonify(rows)
    except Exception as e:
        return {"error": str(e)}, 500


# Ruta: crear un nuevo usuario
@app.route('/usuario', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    mail = data.get('mail')

    if not nombre or not mail:
        return jsonify({"error": "Nombre y mail son requeridos"}), 400

    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO usuarios (nombre, mail) VALUES (%s, %s)",
                    (nombre, mail)
                )
                conn.commit()
                nuevo_id = cursor.lastrowid
        return jsonify({'id_usuario': nuevo_id, 'nombre': nombre, 'mail': mail}), 201
    except Exception as e:
        return {"error": str(e)}, 500


# Ruta: actualizar un usuario
@app.route('/usuario/<int:id_usuario>', methods=['PUT'])
def actualizar_usuario(id_usuario):
    data = request.get_json()
    nombre = data.get('nombre')
    mail = data.get('mail')

    if not nombre or not mail:
        return jsonify({"error": "Nombre y mail son requeridos"}), 400

    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE usuarios SET nombre=%s, mail=%s WHERE id_usuario=%s",
                    (nombre, mail, id_usuario)
                )
                conn.commit()
                filas = cursor.rowcount
        if filas == 0:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        return jsonify({'id_usuario': id_usuario, 'nombre': nombre, 'mail': mail})
    except Exception as e:
        return {"error": str(e)}, 500


# Ruta: eliminar un usuario
@app.route('/usuario/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM usuarios WHERE id_usuario=%s",
                    (id_usuario,)
                )
                conn.commit()
                filas = cursor.rowcount
        if filas == 0:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        return '', 204
    except Exception as e:
        return {"error": str(e)}, 500


# -------------------------------
# Ejecutar aplicación
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
