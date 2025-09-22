# archivo: Conexion/conexion.py
# Esta función sirve para conectarnos a la base de datos MySQL
# usando el usuario root y la contraseña que definimos.

import mysql.connector

def obtener_conexion():
    # Conexión a la base de datos
    # host: dirección del servidor MySQL (localhost porque es mi PC)
    # user: usuario que usamos (root)
    # password: contraseña de MySQL (root1234)
    # database: nombre de la base de datos que creamos para la app
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root1234",   # mi contraseña de MySQL
        database="desarrollo_web"  # <- cambiar por el nombre real de tu DB
    )
