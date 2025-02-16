import numpy as np
from PIL import Image
import math

# Источник алгоритма: https://en.wikipedia.org/wiki/Diamond-square_algorithm
def generate_plasma_square_diamond_algorithm(size=256, roughness=0.5):
    size += 1
    height_map = np.zeros((size, size))
    
    # Углы со случайными цветами.
    height_map[0, 0] = np.random.rand() * size
    height_map[0, -1] = np.random.rand() * size
    height_map[-1, 0] = np.random.rand() * size
    height_map[-1, -1] = np.random.rand() * size

    step = size - 1
    rand_range = size / 2

    while step > 1:
        half = step // 2
        
        # Алмаз
        for x in range(0, size-1, step):
            for y in range(0, size-1, step):
                avg = (height_map[x, y] + 
                       height_map[x+step, y] + 
                       height_map[x, y+step] + 
                       height_map[x+step, y+step]) / 4
                height_map[x+half, y+half] = avg + np.random.uniform(-rand_range, rand_range)
        
        # Квадрат
        for x in range(0, size, half):
            for y in range((x + half) % step, size, step):
                total = 0
                count = 0
                if x >= half:
                    total += height_map[x-half, y]
                    count += 1
                if x + half < size:
                    total += height_map[x+half, y]
                    count += 1
                if y >= half:
                    total += height_map[x, y-half]
                    count += 1
                if y + half < size:
                    total += height_map[x, y+half]
                    count += 1
                if count > 0:
                    avg = total / count
                    height_map[x, y] = avg + np.random.uniform(-rand_range, rand_range)
        
        step = half
        rand_range *= roughness

    return height_map

def main():
    size = 2**8
    plasma = generate_plasma_square_diamond_algorithm(size)
    
    img = Image.new('RGB', (size+1, size+1))
    pixels = img.load()
    
    # Преобразование значений в цвета методом фазового кодирования.
    # Цветовая модель осуществляется поворотом по цветовому кругу.
    # 0 - красный, 120 - зелёный, 240 - синий.
    for x in range(size+1):
        for y in range(size+1):
            value = plasma[x, y]
            r = int(128 + 127 * math.sin(value * 0.1))
            g = int(128 + 127 * math.sin(value * 0.1 + 2))
            b = int(128 + 127 * math.sin(value * 0.1 + 4))
            pixels[x, y] = (r, g, b)
    
    img.save('plasma.png')

if __name__ == '__main__':
    main()