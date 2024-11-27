import os
import subprocess

if __name__ == "__main__":
    curr_dir = os.path.dirname(__file__)
    
    path1 = os.path.join(curr_dir, "frontend")
    path2  =os.path.join(curr_dir, "backend")
    
    process1 = subprocess.Popen(['pnpm', 'preview'], cwd=path1)
    process2 = subprocess.Popen(['python', '-m', 'gunicorn', '--config', 'gunicorn_config.py', 'app:app'], cwd=path2)
    
    process1.wait()
    process2.wait()