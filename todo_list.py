import json
import os
from datetime import datetime
from typing import List, Dict

class TodoList:
    """Aplicación de lista de tareas con almacenamiento local."""
    
    def __init__(self, archivo_datos: str = 'tareas.json'):
        self.archivo_datos = archivo_datos
        self.tareas = self.cargar_tareas()
    
    def cargar_tareas(self) -> List[Dict]:
        """Carga las tareas desde el archivo local."""
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
    
    def guardar_tareas(self) -> None:
        """Guarda las tareas en el archivo local."""
        with open(self.archivo_datos, 'w', encoding='utf-8') as f:
            json.dump(self.tareas, f, indent=2, ensure_ascii=False)
    
    def agregar_tarea(self, titulo: str, descripcion: str = '', prioridad: str = 'media') -> Dict:
        """Agrega una nueva tarea a la lista."""
        if not titulo:
            raise ValueError("El título de la tarea no puede estar vacío")
        
        nueva_tarea = {
            'id': len(self.tareas) + 1,
            'titulo': titulo,
            'descripcion': descripcion,
            'prioridad': prioridad,
            'completada': False,
            'fecha_creacion': datetime.now().isoformat(),
            'fecha_completacion': None
        }
        
        self.tareas.append(nueva_tarea)
        self.guardar_tareas()
        return nueva_tarea
    
    def marcar_completada(self, tarea_id: int) -> bool:
        """Marca una tarea como completada."""
        for tarea in self.tareas:
            if tarea['id'] == tarea_id:
                tarea['completada'] = True
                tarea['fecha_completacion'] = datetime.now().isoformat()
                self.guardar_tareas()
                return True
        return False
    
    def marcar_pendiente(self, tarea_id: int) -> bool:
        """Marca una tarea como pendiente."""
        for tarea in self.tareas:
            if tarea['id'] == tarea_id:
                tarea['completada'] = False
                tarea['fecha_completacion'] = None
                self.guardar_tareas()
                return True
        return False
    
    def eliminar_tarea(self, tarea_id: int) -> bool:
        """Elimina una tarea de la lista."""
        for i, tarea in enumerate(self.tareas):
            if tarea['id'] == tarea_id:
                self.tareas.pop(i)
                self.guardar_tareas()
                return True
        return False
    
    def editar_tarea(self, tarea_id: int, titulo: str = None, 
                     descripcion: str = None, prioridad: str = None) -> bool:
        """Edita los detalles de una tarea."""
        for tarea in self.tareas:
            if tarea['id'] == tarea_id:
                if titulo:
                    tarea['titulo'] = titulo
                if descripcion:
                    tarea['descripcion'] = descripcion
                if prioridad:
                    tarea['prioridad'] = prioridad
                self.guardar_tareas()
                return True
        return False
    
    def obtener_tarea(self, tarea_id: int) -> Dict:
        """Obtiene los detalles de una tarea específica."""
        for tarea in self.tareas:
            if tarea['id'] == tarea_id:
                return tarea
        return None
    
    def listar_tareas(self, filtro: str = 'todas') -> List[Dict]:
        """
        Lista las tareas con opciones de filtrado.
        Filtros: 'todas', 'pendientes', 'completadas'
        """
        if filtro == 'pendientes':
            return [t for t in self.tareas if not t['completada']]
        elif filtro == 'completadas':
            return [t for t in self.tareas if t['completada']]
        return self.tareas
    
    def listar_por_prioridad(self, prioridad: str) -> List[Dict]:
        """Lista las tareas filtradas por prioridad."""
        return [t for t in self.tareas if t['prioridad'] == prioridad]
    
    def estadisticas(self) -> Dict:
        """Obtiene estadísticas de las tareas."""
        total = len(self.tareas)
        completadas = sum(1 for t in self.tareas if t['completada'])
        pendientes = total - completadas
        
        return {
            'total': total,
            'completadas': completadas,
            'pendientes': pendientes,
            'porcentaje_completadas': round((completadas / total * 100) if total > 0 else 0, 2)
        }
    
    def mostrar_tareas(self, filtro: str = 'todas') -> None:
        """Muestra las tareas en formato tabla."""
        tareas = self.listar_tareas(filtro)
        
        print("\n" + "=" * 100)
        print(f"📋 LISTA DE TAREAS - {filtro.upper()}")
        print("=" * 100)
        
        if not tareas:
            print("No hay tareas en esta categoría.")
            print("=" * 100 + "\n")
            return
        
        print(f"{'ID':<4} | {'Título':<25} | {'Descripción':<30} | {'Prioridad':<10} | {'Estado':<12}")
        print("-" * 100)
        
        for tarea in tareas:
            estado = "✅ Completada" if tarea['completada'] else "⏳ Pendiente"
            print(f"{tarea['id']:<4} | {tarea['titulo']:<25} | {tarea['descripcion']:<30} | {tarea['prioridad']:<10} | {estado:<12}")
        
        print("=" * 100 + "\n")
    
    def mostrar_estadisticas(self) -> None:
        """Muestra las estadísticas de las tareas."""
        stats = self.estadisticas()
        
        print("\n" + "=" * 50)
        print("📊 ESTADÍSTICAS")
        print("=" * 50)
        print(f"Total de tareas:        {stats['total']}")
        print(f"Tareas completadas:     {stats['completadas']}")
        print(f"Tareas pendientes:      {stats['pendientes']}")
        print(f"Progreso:               {stats['porcentaje_completadas']}%")
        print("=" * 50 + "\n")


def demostacion():
    """Demostración del funcionamiento de la aplicación."""
    
    # Crear instancia de lista de tareas
    todo = TodoList('tareas_demo.json')
    
    # Limpiar tareas previas para la demostración
    todo.tareas = []
    
    print("\n🚀 DEMOSTRACIÓN - APLICACIÓN DE LISTA DE TAREAS\n")
    
    # Agregar tareas
    print("1️⃣  Agregando tareas...")
    todo.agregar_tarea("Completar proyecto DORA", "Implementar calculadora de métricas", "alta")
    todo.agregar_tarea("Revisar código", "Hacer revisión del PR #42", "media")
    todo.agregar_tarea("Documentar API", "Escribir documentación del endpoint /users", "media")
    todo.agregar_tarea("Escribir tests", "Crear pruebas unitarias para auth", "alta")
    todo.agregar_tarea("Actualizar dependencias", "Actualizar npm packages", "baja")
    print("✅ Tareas agregadas exitosamente\n")
    
    # Mostrar todas las tareas
    todo.mostrar_tareas('todas')
    
    # Marcar algunas tareas como completadas
    print("2️⃣  Marcando tareas como completadas...")
    todo.marcar_completada(1)
    todo.marcar_completada(3)
    print("✅ Tareas marcadas\n")
    
    # Mostrar tareas pendientes
    todo.mostrar_tareas('pendientes')
    
    # Mostrar tareas completadas
    todo.mostrar_tareas('completadas')
    
    # Mostrar estadísticas
    todo.mostrar_estadisticas()
    
    # Mostrar tareas por prioridad
    print("3️⃣  Tareas de alta prioridad:\n")
    tareas_alta = todo.listar_por_prioridad('alta')
    for tarea in tareas_alta:
        estado = "✅" if tarea['completada'] else "⏳"
        print(f"  {estado} {tarea['titulo']}")
    print()


if __name__ == '__main__':
    demostacion()
