import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root1234",  # La contraseña que configuraste
        database="desarrollo_web"  # Tu base de datos real
    )
