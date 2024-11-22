import pandas as pd
import os
from datetime import datetime

RESERVACIONES_FILE = "data/reservaciones.csv"

def init_reservaciones_file():
    """Inicializa el archivo de reservaciones si no existe"""
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(RESERVACIONES_FILE):
        df = pd.DataFrame(columns=['fecha', 'hora', 'nombre', 'email', 'telefono', 'personas', 'comentarios'])
        df.to_csv(RESERVACIONES_FILE, index=False)

def guardar_reservacion(fecha, hora, nombre, email, telefono, personas, comentarios):
    """Guarda una nueva reservación en el archivo CSV"""
    nueva_reservacion = pd.DataFrame([[fecha, hora, nombre, email, telefono, personas, comentarios]], 
                                   columns=['fecha', 'hora', 'nombre', 'email', 'telefono', 'personas', 'comentarios'])
    
    if os.path.exists(RESERVACIONES_FILE):
        df = pd.read_csv(RESERVACIONES_FILE)
        df = pd.concat([df, nueva_reservacion], ignore_index=True)
    else:
        df = nueva_reservacion
    
    df.to_csv(RESERVACIONES_FILE, index=False)
    return True

def obtener_reservaciones():
    """Obtiene todas las reservaciones ordenadas por fecha y hora"""
    if os.path.exists(RESERVACIONES_FILE):
        df = pd.read_csv(RESERVACIONES_FILE)
        df['fecha'] = pd.to_datetime(df['fecha'])
        return df.sort_values(by=['fecha', 'hora'])
    return pd.DataFrame()