import os
from app.core.config import Config

def test_file_paths():
    config = Config()
    
    print("=== File path verification ===")
    print(f"Base directory: {config.BASE_DIR}")
    print(f"CV path: {config.CV_PDF_PATH}")
    print(f"Experience path: {config.EXPERIENCE_TXT_PATH}")
    print()

    print("=== File existence verification ===")
    cv_exists = os.path.exists(config.CV_PDF_PATH)
    exp_exists = os.path.exists(config.EXPERIENCE_TXT_PATH)
    
    print(f"CV exists: {cv_exists}")
    if cv_exists:
        print(f"  Size: {os.path.getsize(config.CV_PDF_PATH)} bytes")
    else:
        print(f"  File not found at: {config.CV_PDF_PATH}")

    print(f"Experience exists: {exp_exists}")
    if exp_exists:
        print(f"  Size: {os.path.getsize(config.EXPERIENCE_TXT_PATH)} bytes")
    else:
        print(f"  File not found at: {config.EXPERIENCE_TXT_PATH}")
    
    print()
    print("=== Data directory contents ===")
    data_dir = os.path.join(config.BASE_DIR, 'data')
    if os.path.exists(data_dir):
        files = os.listdir(data_dir)
        print(f"Files in {data_dir}:")
        for file in files:
            file_path = os.path.join(data_dir, file)
            size = os.path.getsize(file_path) if os.path.isfile(file_path) else "DIR"
            print(f"  - {file} ({size} bytes)")
    else:
        print(f"Data directory does not exist: {data_dir}")

if __name__ == "__main__":
    test_file_paths()
