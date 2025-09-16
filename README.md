
# TP2: Algoritmos Genéticos

### Instrucciones de ejecución:
Ejecutar el archivo main.py desde el root del proyecto, con un entorno virtual de python con las dependencias actualizadas
> `python main.py <nombre-archivo>`

Las imágenes ouput del programa se almacenarán en un directorio ./images/nombre-archivo

Se guardan cada 25 generaciones el individuo con mejor fitness

Se pueden cambiar las rutas desde el archivo de configuración

### Métricas

Se almacenan en ./metricas/nombre-archivo/fitness_log_nombre-archivo.txt 
    y en ./metricas/nombre-archivo/time_log_nombre-archivo.txt 

### Configuración Inicial
Modificar el archivo ./configs/config.json con los parametros deseados

| Clave | Tipo | Descripción breve |
|-------|------|-------------------|
| **pop_size** | int | Tamaño de la población por generación. |
| **k** | int | Cantidad de individuos seleccionados. |
| **num_triangles** | int | Cantidad de triángulos que componen cada individuo. |
| **mutation_rate** | float | Probabilidad de mutación por gen tras el cruce. |
| **num_generations** | int | Número máximo de generaciones a ejecutar. |
| **selection_method** | string | Método de selección de padres (p. ej. `ranking`, `roulette`, `boltzmann`). |
| **generation_selection_method** | string | Estrategia para elegir la población de la siguiente generación. |
| **crossover_method** | string | Tipo de cruce para combinar padres (`one_point`, `uniform`, etc.). |
| **mutation_method** | string | Estrategia de mutación (`uniform`, `basic`, etc.). |
| **replacement_strategy** | string | Forma de reemplazar la población (`traditional`, `elitist`, etc.). |
| **target_image_path** | string | Ruta de la imagen objetivo a aproximar. |
| **output_dir** | string | Carpeta de salida para resultados e imágenes generadas. |
| **FITNESS_THRESHOLD** | float | Nivel de aptitud en [0,1] que detiene el algoritmo si se alcanza. |
| **boltzmann_initial_temp** | float | Temperatura inicial para selección Boltzmann. |
| **boltzmann_final_temp** | float | Temperatura final mínima para Boltzmann. |
| **boltzmann_decay** | float | Tasa de enfriamiento en Boltzmann. |


