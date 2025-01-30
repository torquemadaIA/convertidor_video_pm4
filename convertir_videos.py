import os
import shutil
import pathlib
import tempfile
from moviepy.editor import VideoFileClip

# Ruta a la carpeta de los videos originales
source_folder = r'D:/ireunlocker/solo ireunlocker/new post ireunlocker/prueba video'

# Nueva carpeta para los videos convertidos
output_folder = r'D:/ireunlocker/solo ireunlocker/new post ireunlocker/videos_convertidos'

# Asegúrate de que la carpeta de salida exista
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Lista todos los archivos de video en la carpeta
def listar_archivos_video(carpeta):
    formatos_video = (
        '.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.mpeg', '.mpg', '.3gp', '.rm', '.rmvb', '.ts'
    )
    archivos = []
    for item in pathlib.Path(carpeta).iterdir():
        if item.is_file() and item.suffix.lower() in formatos_video:
            archivos.append(item)
    return archivos

video_files = listar_archivos_video(source_folder)

def renombrar_archivo_largo(ruta_archivo):
    ruta = pathlib.Path(ruta_archivo)
    nuevo_nombre = ruta.stem[:200] + ruta.suffix  # Limita el nombre a 200 caracteres
    ruta_nueva = ruta.with_name(nuevo_nombre)
    if ruta != ruta_nueva:
        shutil.move(ruta_archivo, ruta_nueva)
        print(f'Archivo renombrado de {ruta_archivo} a {ruta_nueva}')
        return ruta_nueva
    return ruta_archivo

def desbloquear_y_convertir(archivo_path):
    try:
        # Copiar archivo a un nombre temporal si está bloqueado
        with tempfile.NamedTemporaryFile(delete=False, suffix=archivo_path.suffix) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfile(archivo_path, temp_file_path)
        
        # Renombrar el archivo temporal si el nombre es demasiado largo
        temp_file_path = renombrar_archivo_largo(temp_file_path)
        output_path = os.path.join(output_folder, pathlib.Path(temp_file_path).stem + '.mov')  # Convertir a .mov

        # Imprimir ruta para depuración
        print(f'Archivo temporal: {temp_file_path}')
        print(f'Archivo convertido: {output_path}')
        
        # Convertir el archivo temporal
        try:
            with VideoFileClip(temp_file_path) as video:
                video.write_videofile(output_path, codec='libx264', audio_codec='aac')
            print(f'Video convertido y guardado como {output_path}')
        except Exception as e:
            print(f'Error al convertir con MoviePy: {e}')
        
        # Eliminar el archivo temporal
        os.remove(temp_file_path)

    except Exception as e:
        print(f'Error al procesar {archivo_path}: {e}')

# Convertir todos los videos en la carpeta
for archivo_path in video_files:
    print(f'Procesando: {archivo_path}')
    desbloquear_y_convertir(archivo_path)

print("Conversión completa.")
