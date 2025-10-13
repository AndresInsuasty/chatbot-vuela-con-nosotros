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
                "numero_asiento": asiento_disponible,
            }
        )

    return {"origen": origen, "destino": destino, "fecha": fecha, "opciones": opciones}


def reservar_asiento(
    vuelo: str, numero_asiento: int, id_pasajero: str, conn: sqlite3.Connection
) -> Dict[str, Any]:
    """
    Reserva un asiento en un vuelo específico para un pasajero.

    Args:
        vuelo (str): El número del vuelo.
        numero_asiento (int): El número del asiento a reservar.
        id_pasajero (str): El ID del pasajero.
        conn (sqlite3.Connection): Conexión a la base de datos.

    Returns:
        dict: Un diccionario con el resultado de la reserva.
    """
    cursor = conn.cursor()
    try:
        # Verificar si el asiento ya está reservado
        cursor.execute(
            "SELECT COUNT(*) FROM reservas WHERE vuelo = ? AND numero_asiento = ?",
            (vuelo, numero_asiento),
        )
        if cursor.fetchone()[0] > 0:
            return {"error": "Asiento ya reservado"}

        # Realizar la reserva
        cursor.execute(
            "INSERT INTO reservas (vuelo, numero_asiento, id_pasajero) VALUES (?, ?, ?)",
            (vuelo, numero_asiento, id_pasajero),
        )
        conn.commit()
        return {
            "vuelo": vuelo,
            "numero_asiento": numero_asiento,
            "id_pasajero": id_pasajero,
            "estado": "Reservado",
        }
    except sqlite3.IntegrityError as e:
        return {"error": str(e)}
    finally:
        cursor.close()


def eliminar_reserva(
    vuelo: str, numero_asiento: int, id_pasajero: str, conn: sqlite3.Connection
) -> Dict[str, Any]:
    """
    Elimina una reserva de asiento en un vuelo específico para un pasajero.

    Args:
        vuelo (str): El número del vuelo.
        numero_asiento (int): El número del asiento a eliminar.
        id_pasajero (str): El ID del pasajero.
        conn (sqlite3.Connection): Conexión a la base de datos.

    Returns:
        dict: Un diccionario con el resultado de la eliminación de la reserva.
    """
    cursor = conn.cursor()
    try:
        # Verificar si la reserva existe
        cursor.execute(
            "SELECT COUNT(*) FROM reservas WHERE vuelo = ? AND numero_asiento = ? AND id_pasajero = ?",
            (vuelo, numero_asiento, id_pasajero),
        )
        if cursor.fetchone()[0] == 0:
            return {"error": "Reserva no encontrada"}

        # Eliminar la reserva
        cursor.execute(
            "DELETE FROM reservas WHERE vuelo = ? AND numero_asiento = ? AND id_pasajero = ?",
            (vuelo, numero_asiento, id_pasajero),
        )
        conn.commit()
        return {
            "vuelo": vuelo,
            "asiento": numero_asiento,
            "id_pasajero": id_pasajero,
            "estado": "Reserva eliminada",
        }
    except sqlite3.IntegrityError as e:
        return {"error": str(e)}
    finally:
        cursor.close()
