import imageio
import os
import glob
import re

path = "./images/toad_tour_det_comp"

files = glob.glob(os.path.join(path, "generation_*.png"))

def extract_number(filename):
    match = re.search(r"generation_(\d+)\.png", os.path.basename(filename))
    return int(match.group(1)) if match else -1

files = sorted(files, key=extract_number)

output_gif = os.path.join(path, "toad_tour_det_comp_evolution.gif")

with imageio.get_writer(output_gif, mode="I", duration=0.2, loop=0) as writer:
    for filename in files:
        image = imageio.imread(filename)
        writer.append_data(image)

print(f"GIF creado en: {output_gif}")

