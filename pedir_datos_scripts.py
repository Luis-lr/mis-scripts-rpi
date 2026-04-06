import subprocess

# Lista de scripts a ejecutar
scripts = ["pedir_humedad_en_WOR.py", "pedir_temp_suelo_WOR.py", "pedir_temp_hum_int_WOR.py", "pedir_temp_hum_ext_WOR.py"]

# Bucle para ejecutar los scripts en secuencia
for script in scripts:
    try:
        result = subprocess.run(["python3", script], check=True, capture_output=True, text=True)
        print(f"Script {script} ejecutado con éxito.")
        print("Salida del script:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el script {script}: {e}")
        print("Salida de error:\n", e.stderr)
        break # Detener el bucle si hay un error
