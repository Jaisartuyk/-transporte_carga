#!/usr/bin/env python
"""
Script para aplicar mejoras al sistema de trazabilidad
Ejecutar: python aplicar_mejoras.py
"""

import os
import sys
import shutil
from datetime import datetime

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_step(step, text):
    print(f"[{step}] {text}")

def print_success(text):
    print(f"✅ {text}")

def print_warning(text):
    print(f"⚠️  {text}")

def print_error(text):
    print(f"❌ {text}")

def confirmar(mensaje):
    respuesta = input(f"{mensaje} (s/n): ").lower()
    return respuesta == 's'

def main():
    print_header("🚀 APLICAR MEJORAS AL SISTEMA DE TRAZABILIDAD")
    
    print("""
Este script realizará las siguientes acciones:

1. ✅ Crear backup de la base de datos actual
2. ✅ Crear backup del archivo models.py actual  
3. ✅ Reemplazar models.py con la versión mejorada
4. ✅ Crear migraciones de Django
5. ✅ Aplicar migraciones
6. ✅ Actualizar archivos relacionados

⚠️  IMPORTANTE: Asegúrate de tener un backup antes de continuar
    """)
    
    if not confirmar("¿Deseas continuar?"):
        print("\n❌ Operación cancelada por el usuario")
        return
    
    # Paso 1: Backup de base de datos
    print_header("PASO 1: Backup de Base de Datos")
    print_step(1, "Creando backup de la base de datos...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_db_{timestamp}.json"
    
    try:
        os.system(f"python manage.py dumpdata > {backup_file}")
        print_success(f"Backup creado: {backup_file}")
    except Exception as e:
        print_error(f"Error al crear backup: {e}")
        if not confirmar("¿Deseas continuar sin backup?"):
            return
    
    # Paso 2: Backup de models.py
    print_header("PASO 2: Backup de models.py")
    print_step(2, "Creando backup de models.py...")
    
    models_original = "cargas/models.py"
    models_backup = f"cargas/models_backup_{timestamp}.py"
    
    try:
        shutil.copy(models_original, models_backup)
        print_success(f"Backup creado: {models_backup}")
    except Exception as e:
        print_error(f"Error al crear backup de models: {e}")
        return
    
    # Paso 3: Reemplazar models.py
    print_header("PASO 3: Reemplazar models.py")
    print_step(3, "Reemplazando models.py con versión mejorada...")
    
    if not confirmar("¿Confirmas el reemplazo de models.py?"):
        print_warning("Reemplazo cancelado")
        return
    
    try:
        shutil.copy("cargas/models_mejorado.py", models_original)
        print_success("models.py reemplazado exitosamente")
    except Exception as e:
        print_error(f"Error al reemplazar models: {e}")
        # Restaurar backup
        shutil.copy(models_backup, models_original)
        print_warning("models.py restaurado desde backup")
        return
    
    # Paso 4: Crear migraciones
    print_header("PASO 4: Crear Migraciones")
    print_step(4, "Generando migraciones de Django...")
    
    try:
        os.system("python manage.py makemigrations")
        print_success("Migraciones creadas")
    except Exception as e:
        print_error(f"Error al crear migraciones: {e}")
        return
    
    # Paso 5: Aplicar migraciones
    print_header("PASO 5: Aplicar Migraciones")
    print_step(5, "Aplicando migraciones a la base de datos...")
    
    if not confirmar("¿Confirmas aplicar las migraciones?"):
        print_warning("Migraciones no aplicadas")
        print_warning("Puedes aplicarlas manualmente con: python manage.py migrate")
        return
    
    try:
        os.system("python manage.py migrate")
        print_success("Migraciones aplicadas exitosamente")
    except Exception as e:
        print_error(f"Error al aplicar migraciones: {e}")
        return
    
    # Paso 6: Resumen
    print_header("✅ PROCESO COMPLETADO")
    
    print("""
🎉 ¡Mejoras aplicadas exitosamente!

📋 Archivos creados:
   - {backup_file} (Backup de base de datos)
   - {models_backup} (Backup de models.py)

📝 Próximos pasos recomendados:

1. Actualizar admin.py para mostrar nuevos campos
2. Actualizar serializers.py para API
3. Actualizar forms.py para formularios
4. Actualizar templates para mostrar nueva información
5. Crear fixtures de datos de prueba
6. Probar todas las funcionalidades

🔍 Para verificar los cambios:
   python manage.py shell
   >>> from cargas.models import Envio
   >>> Envio._meta.get_fields()

📚 Consulta MEJORAS_IMPLEMENTADAS.md para más detalles
    """.format(backup_file=backup_file, models_backup=models_backup))
    
    print_success("¡Sistema actualizado correctamente!")

if __name__ == "__main__":
    main()
