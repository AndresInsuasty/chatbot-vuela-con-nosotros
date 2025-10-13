"""Utilidades para la gestión de vuelos y reservas."""

from typing import Dict, Any
import sqlite3
import os


def conectar_base_datos(
    nombre_db: str = "vuelos.db", script_sql: str = "inicial.sql"
) -> None:
    """
    Crea una base de datos SQLite con las tablas estado_vuelos y reservas solo si no existe.
    Llena las tablas con datos iniciales desde un archivo .sql.
    """
    if not os.path.exists(nombre_db):
        conn = sqlite3.connect(nombre_db)
        with open(script_sql, "r", encoding="utf-8") as f:
            sql_script = f.read()
        conn.executescript(sql_script)
        conn.close()
    return sqlite3.connect(nombre_db)


def consulta_estado_vuelo(
    numero_vuelo: str, conn: sqlite3.Connection
) -> Dict[str, Any]:
    """
    Consulta el estado de un vuelo dado su número, obteniendo los datos desde la base de datos.

    Args:
        numero_vuelo (str): El número del vuelo a consultar.
        conn (sqlite3.Connection): Conexión a la base de datos.

    Returns:
        dict: Un diccionario con la información del estado del vuelo.
    """
    cursor = conn.cursor()
    try:
        # Usar parámetros en la consulta evita que valores como PSO se interpreten como columnas
        cursor.execute(
            """SELECT vuelo, estado, origen, destino, fecha, hora
         FROM estado_vuelos WHERE vuelo = ?""",
            (numero_vuelo,),
        )
        resultado = cursor.fetchone()
    finally:
        cursor.close()
    if resultado:
        vuelo, estado, origen, destino, fecha, hora = resultado
    else:
        vuelo, estado, origen, destino, fecha, hora = (
            numero_vuelo,
            "Desconocido",
            None,
            None,
            None,
            None,
        )

    estado_vuelo = {
        "numero_vuelo": vuelo,
        "estado": estado,
        "origen": origen,
        "destino": destino,
        "fecha": fecha,
        "hora": hora,
    }
    return estado_vuelo


def consultar_opciones_vuelo(
    origen: str, destino: str, fecha: str, conn: sqlite3.Connection
) -> Dict[str, Any]:
    """
    Consulta las opciones de vuelo disponibles entre un origen y un destino en una fecha dada.

    Args:
        origen (str): Ciudad de origen.
        destino (str): Ciudad de destino.
        fecha (str): Fecha del vuelo en formato 'YYYY-MM-DD'.
        conn (sqlite3.Connection): Conexión a la base de datos.

    Returns:
        dict: Un diccionario con las opciones de vuelo disponibles.
    """
    cursor = conn.cursor()
    try:
        cursor.execute(
            """SELECT vuelo, hora, estado
         FROM estado_vuelos
         WHERE origen = ? AND destino = ? AND fecha = ?""",
            (origen, destino, fecha),
        )
        resultados = cursor.fetchall()
    finally:
        cursor.close()

    opciones = []
    # Para cada vuelo, consultar los asientos reservados y calcular el primer asiento
    # disponible en el rango 1..20. Si todos los asientos 1..20 están asignados,
    # el vuelo se considera lleno y retornamos None en 'asiento'.
    for vuelo, hora, estado in resultados:
        c2 = conn.cursor()
        try:
            c2.execute(
                "SELECT numero_asiento FROM reservas WHERE vuelo = ?",
                (vuelo,),
            )
            usados = {row[0] for row in c2.fetchall()}
        finally:
            c2.close()

        asiento_disponible = None
        for n in range(1, 21):
            if n not in usados:
                asiento_disponible = n
                break

        opciones.append(
            {
                "numero_vuelo": vuelo,
                "hora": hora,
                "estado": estado,
                "asiento": asiento_disponible,
            }
        )

    return {"origen": origen, "destino": destino, "fecha": fecha, "opciones": opciones}
