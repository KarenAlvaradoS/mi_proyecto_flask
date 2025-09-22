from flask_login import UserMixin
from Conexion.conexion import obtener_conexion

# Clase que representa a un usuario de mi app
# Uso UserMixin para que funcione con Flask-Login
class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, email, password):
        # Inicializo los atributos del usuario
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password

    # MÉTODO REQUERIDO POR FLASK-LOGIN
    def get_id(self):
        # Devuelve el id como string para Flask-Login
        return str(self.id_usuario)

    # ------------------------------------------
    # Función que busca un usuario en la base por su email
    # ------------------------------------------
    @staticmethod
    def obtener_por_mail(email):
        conexion = obtener_conexion()  # me conecto a la base
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        dato = cursor.fetchone()       # obtengo un solo usuario
        cursor.close()
        conexion.close()
        
        if dato is None:
            return None
        # Devuelvo un objeto Usuario si existe en la base
        return Usuario(dato['id_usuario'], dato['nombre'], dato['email'], dato['password'])

    # ------------------------------------------
    # Función para registrar un nuevo usuario en la base de datos
    # ------------------------------------------
    @staticmethod
    def registrar(nombre, email, password):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, password)
        )
        conexion.commit()  # confirmo los cambios
        cursor.close()
        conexion.close()

    # ------------------------------------------
    # Función para obtener todos los usuarios (para pruebas y Flask-Login)
    # ------------------------------------------
    @staticmethod
    def obtener_todos():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        datos = cursor.fetchall()  # traigo todos los usuarios
        cursor.close()
        conexion.close()
        return datos
