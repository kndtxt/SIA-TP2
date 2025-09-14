
import os

BASE_DIR = "./metrics"

def delete_existing_file(filename: str) -> None:
    """Elimina el archivo si ya existe."""
    dir = BASE_DIR + "/" + filename
    if os.path.exists(dir):
        os.remove(dir)


def write_to_file(filename: str, content: str) -> None:
    """Escribe el contenido en un archivo."""
    dir = BASE_DIR + "/" + filename

    with open(dir, 'a') as file:
        file.write(content)