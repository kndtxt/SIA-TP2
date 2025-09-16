#!/usr/bin/env python3
import os
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import imageio
import json

# --- Configuración ---
DATASET_FOLDER = "./metrics/datasets"
GRAPH_FOLDER = "./metrics/graphs"
GIF_NAME = "all_graphs.gif"
FIGSIZE = (10, 6)
DPI = 150
GIF_FRAME_DURATION = 0.6  # segundos por frame

# --- Utilidades ---
def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def load_file(path):
    """Lee archivo y devuelve su contenido como texto."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def parse_dataset(text):
    """
    Espera texto con líneas 'Generación;Mejor Fitness' y devuelve (xs, ys).
    Ignora encabezado y líneas vacías.
    """
    lines = text.splitlines()
    xs, ys = [], []
    for line in lines[1:]:  # saltar encabezado
        line = line.strip()
        if not line:
            continue
        # defensivo: ignorar líneas malformadas
        parts = line.split(";")
        if len(parts) < 2:
            continue
        try:
            x = float(parts[0])
            y = float(parts[1])
        except ValueError:
            # intentar reemplazar comas por puntos si hubiera
            try:
                x = float(parts[0].replace(",", "."))
                y = float(parts[1].replace(",", "."))
            except Exception:
                continue
        xs.append(x)
        ys.append(y)
    return xs, ys

# --- Ploteo ---
def plot_combined(datasets, out_path):
    plt.figure(figsize=FIGSIZE)
    for name, (xs, ys) in datasets.items():
        plt.plot(xs, ys, label=name)
    plt.xlabel("Generación")
    plt.ylabel("Mejor Fitness")
    plt.title("Mejor Fitness por Generación (varios datasets)")
    plt.grid(True)
    plt.legend(ncol=1, fontsize="small")
    plt.tight_layout()
    plt.savefig(out_path, dpi=DPI)
    plt.close()

def plot_individual(name, xs, ys, out_path):
    plt.figure(figsize=FIGSIZE)
    plt.plot(xs, ys)
    plt.xlabel("Generación")
    plt.ylabel("Mejor Fitness")
    plt.title(f"{name}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=DPI)
    plt.close()

def make_gif_from_folder(folder, gif_path, duration=GIF_FRAME_DURATION):
    files = sorted([f for f in os.listdir(folder) if f.lower().endswith(".png")])
    images = []
    for fn in files:
        path = os.path.join(folder, fn)
        try:
            images.append(imageio.imread(path))
        except Exception as e:
            print(f"Advertencia: no se pudo leer {path}: {e}")
    if images:
        imageio.mimsave(gif_path, images, duration=duration)
        print(f"GIF guardado en {gif_path}")
    else:
        print("No se encontraron imágenes PNG para generar el GIF.")

# --- Main ---
def main():
    ensure_folder(GRAPH_FOLDER)

    if not os.path.isdir(DATASET_FOLDER):
        print(f"Error: carpeta de datasets no existe: {DATASET_FOLDER}")
        sys.exit(1)

    files = [f for f in os.listdir(DATASET_FOLDER) if os.path.isfile(os.path.join(DATASET_FOLDER, f))]
    files = sorted(files)  # orden consistente

    datasets = {}
    for file_name in files:
        file_path = os.path.join(DATASET_FOLDER, file_name)
        try:
            text = load_file(file_path)
        except Exception as e:
            print(f"Error leyendo {file_path}: {e}")
            continue
        xs, ys = parse_dataset(text)
        if not xs:
            print(f"Advertencia: no hay datos válidos en {file_name}, se salta.")
            continue
        label = os.path.splitext(file_name)[0]
        datasets[label] = (xs, ys)

        # guardar gráfica individual
        individual_out = os.path.join(GRAPH_FOLDER, f"{label}.png")
        plot_individual(label, xs, ys, individual_out)
        print(f"Guardada gráfica individual: {individual_out}")

    if not datasets:
        print("No se encontraron datasets válidos para graficar.")
        return

    # gráfica combinada
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    combined_out = os.path.join(GRAPH_FOLDER, f"combined_{timestamp}.png")
    plot_combined(datasets, combined_out)
    print(f"Guardada gráfica combinada: {combined_out}")

    # también guardar una versión con nombre fijo (sobrescribe)
    fixed_combined_out = os.path.join(GRAPH_FOLDER, "combined_latest.png")
    plot_combined(datasets, fixed_combined_out)
    print(f"Guardada gráfica combinada (latest): {fixed_combined_out}")

    # crear GIF usando PNGs en la carpeta graphs
    gif_out = os.path.join(GRAPH_FOLDER, GIF_NAME)
    make_gif_from_folder(GRAPH_FOLDER, gif_out, duration=GIF_FRAME_DURATION)

if __name__ == "__main__":
    main()
