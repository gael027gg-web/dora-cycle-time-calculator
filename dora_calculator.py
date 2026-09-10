from datetime import datetime
from typing import List, Dict

def calcular_tiempo_ciclo_dora(tareas: List[Dict]) -> Dict:
    """
    Calcula el tiempo de ciclo promedio DORA entre inicio y despliegue.
    
    Args:
        tareas: Lista de diccionarios con 'nombre', 'fecha_inicio' y 'fecha_despliegue'
    
    Returns:
        Diccionario con detalles del cálculo y tiempo promedio en horas
    """
    
    if not tareas:
        raise ValueError("La lista de tareas no puede estar vacía")
    
    tiempos_ciclo = []
    detalles = []
    
    for tarea in tareas:
        fecha_inicio = datetime.fromisoformat(tarea['fecha_inicio'])
        fecha_despliegue = datetime.fromisoformat(tarea['fecha_despliegue'])
        
        # Calcular diferencia en horas
        tiempo_ciclo_horas = (fecha_despliegue - fecha_inicio).total_seconds() / 3600
        tiempos_ciclo.append(tiempo_ciclo_horas)
        
        detalles.append({
            'tarea': tarea['nombre'],
            'inicio': tarea['fecha_inicio'],
            'despliegue': tarea['fecha_despliegue'],
            'tiempo_ciclo_horas': round(tiempo_ciclo_horas, 2),
            'tiempo_ciclo_dias': round(tiempo_ciclo_horas / 24, 2)
        })
    
    tiempo_promedio = sum(tiempos_ciclo) / len(tiempos_ciclo)
    
    return {
        'tareas_procesadas': len(tareas),
        'detalles': detalles,
        'tiempo_ciclo_promedio_horas': round(tiempo_promedio, 2),
        'tiempo_ciclo_promedio_dias': round(tiempo_promedio / 24, 2),
        'tiempo_minimo_horas': round(min(tiempos_ciclo), 2),
        'tiempo_maximo_horas': round(max(tiempos_ciclo), 2)
    }


# Ejemplo con tres tareas
tareas_ejemplo = [
    {
        'nombre': 'Autenticación de usuarios',
        'fecha_inicio': '2024-09-01T08:00:00',
        'fecha_despliegue': '2024-09-05T14:30:00'
    },
    {
        'nombre': 'Integración de pagos',
        'fecha_inicio': '2024-09-03T10:00:00',
        'fecha_despliegue': '2024-09-10T16:00:00'
    },
    {
        'nombre': 'Panel de administrador',
        'fecha_inicio': '2024-09-02T09:00:00',
        'fecha_despliegue': '2024-09-06T11:00:00'
    }
]

if __name__ == '__main__':
    resultado = calcular_tiempo_ciclo_dora(tareas_ejemplo)
    
    print("=" * 60)
    print("CALCULADORA DE MÉTRICA DORA - TIEMPO DE CICLO")
    print("=" * 60)
    print(f"\nTotal de tareas analizadas: {resultado['tareas_procesadas']}\n")
    
    print("DETALLES POR TAREA:")
    print("-" * 60)
    for detalle in resultado['detalles']:
        print(f"\nTarea: {detalle['tarea']}")
        print(f"  Inicio:         {detalle['inicio']}")
        print(f"  Despliegue:     {detalle['despliegue']}")
        print(f"  Tiempo ciclo:   {detalle['tiempo_ciclo_horas']} horas ({detalle['tiempo_ciclo_dias']} días)")
    
    print("\n" + "=" * 60)
    print("RESUMEN GENERAL:")
    print("=" * 60)
    print(f"Tiempo ciclo promedio: {resultado['tiempo_ciclo_promedio_horas']} horas")
    print(f"Tiempo ciclo promedio: {resultado['tiempo_ciclo_promedio_dias']} días")
    print(f"Tiempo mínimo: {resultado['tiempo_minimo_horas']} horas")
    print(f"Tiempo máximo: {resultado['tiempo_maximo_horas']} horas")
    print("=" * 60)
