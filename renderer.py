# renderer.py
from PIL import Image, ImageDraw
from typing import List
from triangle import Triangle

def render(triangles: List[Triangle], width: int, height: int) -> Image.Image:
    """
    Dibuja una lista de triángulos sobre un lienzo blanco.
    
    Args:
        triangles: La lista de objetos Triangulo a dibujar.
        width: Ancho de la imagen.
        height: Alto de la imagen.

    Returns:
        Un objeto Image de Pillow con los triángulos renderizados.
    """
    # 1. Crea un lienzo base de color blanco
    image = Image.new("RGB", (width, height), "white")
    
    # 2. Crea una capa de dibujo temporal que soporte transparencia (RGBA)
    # Esto es importante para que los triángulos traslúcidos se mezclen correctamente.
    draw_layer = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(draw_layer)

    # 3. Dibuja cada triángulo en la capa temporal
    for tri in triangles:
        # El formato de los puntos debe ser una lista plana: [x1, y1, x2, y2, ...]
        flat_points = [coord for point in tri.points for coord in point]
        draw.polygon(flat_points, fill=tri.color)

    # 4. Combina la capa con los triángulos sobre el lienzo blanco
    # El 'mask=draw_layer' asegura que la transparencia se aplique correctamente.
    image.paste(draw_layer, mask=draw_layer)
    
    return image