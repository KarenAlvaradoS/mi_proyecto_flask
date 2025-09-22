import mysql.connector

# Esta función me permite conectarme a mi base de datos MySQL
# Siempre la llamo cuando necesito hacer consultas
def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",           # mi servidor MySQL local
        user="root",                # usuario root
        password="root1234",        # mi contraseña
        database="desarrollo_web"   # la base de datos que creé para este proyecto
    )
