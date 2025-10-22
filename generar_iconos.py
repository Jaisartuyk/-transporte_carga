"""
Script para generar todos los iconos de la PWA desde una imagen base
"""

from PIL import Image
import os

# Ruta de la imagen original
imagen_original = "cargas/static/icons/trasporte.png"

# Tamaños necesarios
tamaños = {
    "icon-72.png": 72,
    "icon-96.png": 96,
    "icon-128.png": 128,
    "icon-144.png": 144,
    "icon-152.png": 152,
    "icon-192.png": 192,
    "icon-384.png": 384,
    "icon-512.png": 512,
    "badge-72.png": 72,
}

def generar_iconos():
    try:
        # Abrir imagen original
        print(f"📂 Abriendo imagen: {imagen_original}")
        img = Image.open(imagen_original)
        
        # Convertir a RGBA si no lo está
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        print(f"✅ Imagen cargada: {img.size[0]}x{img.size[1]} píxeles")
        print(f"📐 Generando {len(tamaños)} iconos...")
        print()
        
        # Generar cada tamaño
        for nombre, tamaño in tamaños.items():
            # Redimensionar
            img_redimensionada = img.resize((tamaño, tamaño), Image.Resampling.LANCZOS)
            
            # Guardar
            ruta_salida = f"cargas/static/icons/{nombre}"
            img_redimensionada.save(ruta_salida, 'PNG', optimize=True)
            
            # Obtener tamaño del archivo
            tamaño_archivo = os.path.getsize(ruta_salida)
            tamaño_kb = tamaño_archivo / 1024
            
            print(f"✅ {nombre:20} ({tamaño}x{tamaño}px) - {tamaño_kb:.1f} KB")
        
        print()
        print("🎉 ¡Todos los iconos generados exitosamente!")
        print()
        print("📋 Archivos creados:")
        print("   cargas/static/icons/")
        for nombre in tamaños.keys():
            print(f"   ├── {nombre}")
        print()
        print("✅ Tu PWA ahora tiene todos los iconos necesarios")
        print("🚀 Recarga la aplicación y prueba instalarla")
        
    except FileNotFoundError:
        print("❌ Error: No se encontró la imagen trasporte.png")
        print("   Verifica que esté en: cargas/static/icons/trasporte.png")
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("💡 Solución:")
        print("   Instala Pillow con: pip install Pillow")

if __name__ == "__main__":
    print()
    print("=" * 60)
    print("  GENERADOR DE ICONOS PWA")
    print("=" * 60)
    print()
    generar_iconos()
    print()
