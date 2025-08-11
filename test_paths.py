import os
from app.core.config import Config

def test_file_paths():
    config = Config()
    
    print("=== Verificación de rutas de archivos ===")
    print(f"Directorio base: {config.BASE_DIR}")
    print(f"Ruta CV: {config.CV_PDF_PATH}")
    print(f"Ruta Experience: {config.EXPERIENCE_TXT_PATH}")
    print()
    
    print("=== Verificación de existencia de archivos ===")
    cv_exists = os.path.exists(config.CV_PDF_PATH)
    exp_exists = os.path.exists(config.EXPERIENCE_TXT_PATH)
    
    print(f"CV existe: {cv_exists}")
    if cv_exists:
        print(f"  Tamaño: {os.path.getsize(config.CV_PDF_PATH)} bytes")
    else:
        print(f"  Archivo no encontrado en: {config.CV_PDF_PATH}")
    
    print(f"Experience existe: {exp_exists}")
    if exp_exists:
        print(f"  Tamaño: {os.path.getsize(config.EXPERIENCE_TXT_PATH)} bytes")
    else:
        print(f"  Archivo no encontrado en: {config.EXPERIENCE_TXT_PATH}")
    
    print()
    print("=== Contenido del directorio data ===")
    data_dir = os.path.join(config.BASE_DIR, 'data')
    if os.path.exists(data_dir):
        files = os.listdir(data_dir)
        print(f"Archivos en {data_dir}:")
        for file in files:
            file_path = os.path.join(data_dir, file)
            size = os.path.getsize(file_path) if os.path.isfile(file_path) else "DIR"
            print(f"  - {file} ({size} bytes)")
    else:
        print(f"Directorio data no existe: {data_dir}")

if __name__ == "__main__":
    test_file_paths()
