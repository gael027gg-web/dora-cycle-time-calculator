import pytz
from datetime import datetime
from typing import List, Dict

def obtener_hora_zonas(zonas_horarias: List[str]) -> Dict:
    """
    Obtiene la hora actual en diferentes zonas horarias.
    
    Args:
        zonas_horarias: Lista de zonas horarias (ej: 'America/New_York', 'Europe/London')
    
    Returns:
        Diccionario con las horas en cada zona horaria
    """
    
    resultado = {}
    hora_utc = datetime.now(pytz.UTC)
    
    for zona in zonas_horarias:
        try:
            tz = pytz.timezone(zona)
            hora_local = hora_utc.astimezone(tz)
            resultado[zona] = {
                'hora_formateada': hora_local.strftime('%H:%M:%S'),
                'fecha': hora_local.strftime('%Y-%m-%d'),
                'timezone': str(hora_local.tzname()),
                'offset_utc': hora_local.strftime('%z')
            }
        except pytz.exceptions.UnknownTimeZoneError:
            resultado[zona] = {'error': f'Zona horaria no reconocida: {zona}'}
    
    return resultado


def mostrar_reloj_digital(zonas_horarias: List[str]) -> None:
    """
    Muestra un reloj digital con las horas de diferentes zonas horarias.
    """
    
    datos = obtener_hora_zonas(zonas_horarias)
    
    print("\n" + "=" * 70)
    print("⏰ RELOJ DIGITAL - ZONAS HORARIAS")
    print("=" * 70)
    
    for zona, info in datos.items():
        if 'error' in info:
            print(f"\n❌ {info['error']}")
        else:
            print(f"\n📍 {zona}")
            print(f"   Hora:      {info['hora_formateada']}")
            print(f"   Fecha:     {info['fecha']}")
            print(f"   Zona:      {info['timezone']}")
            print(f"   Offset:    {info['offset_utc']}")
    
    print("\n" + "=" * 70 + "\n")


# Zonas horarias principales
zonas_ejemplo = [
    'UTC',
    'America/New_York',      # Nueva York (EST/EDT)
    'Europe/London',         # Londres (GMT/BST)
    'Europe/Paris',          # París (CET/CEST)
    'Asia/Tokyo',            # Tokio (JST)
    'Asia/Shanghai',         # Shangái (CST)
    'Asia/Dubai',            # Dubái (GST)
    'Australia/Sydney',      # Sídney (AEDT/AEST)
    'America/Los_Angeles',   # Los Ángeles (PST/PDT)
    'America/Mexico_City',   # Ciudad de México (CST/CDT)
    'America/Sao_Paulo',     # São Paulo (BRT/BRST)
    'Africa/Johannesburg',   # Johannesburgo (SAST)
    'Asia/Bangkok',          # Bangkok (ICT)
    'Asia/Kolkata',          # India (IST)
]

if __name__ == '__main__':
    mostrar_reloj_digital(zonas_ejemplo)
