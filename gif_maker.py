import imageio
import os
import glob
import re
import sys

path = f'./images/{sys.argv[1]}'

files = glob.glob(os.path.join(path, "generation_*.png"))

def extract_number(filename):
    match = re.search(r"generation_boltzmann_k1_nocheestrellada(\d+)\.png", os.path.basename(filename))
    return int(match.group(1)) if match else -1

files = sorted(files, key=extract_number)

output_gif = os.path.join(path, f'{sys.argv[2]}.gif')

with imageio.get_writer(output_gif, mode="I", duration=0.2, loop=0) as writer:
    for filename in files:
        image = imageio.imread(filename)
        writer.append_data(image)

print(f"GIF creado en: {output_gif}")

