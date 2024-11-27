import os

def start_frontend():
    os.chdir("./frontend")
    os.system("npm preview")

def start_backend():
    os.chdir("./backend")
    os.system("python -m gunicorn --config gunicorn_config.py app:app")
if __name__ == "__main__":
    start_frontend()
    start_backend()