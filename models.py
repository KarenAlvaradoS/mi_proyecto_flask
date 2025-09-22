from Conexion.conexion import obtener_conexion

# Clase que representa a un usuario
class Usuario:
    def __init__(self, id_usuario, nombre, email, password):
        # Inicializo los datos del usuario
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password

    @staticmethod
    def obtener_por_mail(email):
        # Busco un usuario por su email
        conexion = obtener_conexion()       # Conecto a la base
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        dato = cursor.fetchone()            # Obtengo un solo usuario
        cursor.close()
        conexion.close()
        
        if dato is None:
            return None
        # Devuelvo un objeto Usuario si existe
        return Usuario(dato['id_usuario'], dato['nombre'], dato['email'], dato['password'])

    @staticmethod
    def registrar(nombre, email, password):
        # Registro un nuevo usuario en la base
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                       (nombre, email, password))
        conexion.commit()    # Confirmo los cambios
        cursor.close()
        conexion.close()

    @staticmethod
    def obtener_todos():
        # Obtengo todos los usuarios de la base
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        datos = cursor.fetchall()   # Traigo todos los usuarios
        cursor.close()
        conexion.close()
        return datos
