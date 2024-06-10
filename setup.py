import importlib
import subprocess

def install_package(package):
    subprocess.check_call(['pip', 'install', package])

dependencies = ['cv2', 'numpy', 'tkinter', 'PIL']

for dependency in dependencies:
    try:
        importlib.import_module(dependency)
    except ImportError:
        print(f"{dependency} is not installed. Installing...")
        install_package(dependency)
