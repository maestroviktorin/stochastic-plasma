import numpy as np
from PIL import Image
import math

# Источник алгоритма: https://en.wikipedia.org/wiki/Diamond-square_algorithm
def square_diamond_algorithm(size=256, roughness=.5) -> np.ndarray[np.float64]:
    step = size
    size += 1
    array_pixels = np.zeros((size, size))
    
    # Углы со случайными цветами.
    array_pixels[0, 0] = np.random.rand() * size
    array_pixels[0, -1] = np.random.rand() * size
    array_pixels[-1, 0] = np.random.rand() * size
    array_pixels[-1, -1] = np.random.rand() * size

    rand_range = size / 2

    while step > 1:
        half = step // 2
        
        # Алмаз
        for x in range(0, size-1, step):
            for y in range(0, size-1, step):
                avg = (array_pixels[x, y] + 
                       array_pixels[x+step, y] + 
                       array_pixels[x, y+step] + 
                       array_pixels[x+step, y+step]) / 4
                array_pixels[x+half, y+half] = avg + np.random.uniform(-rand_range, rand_range)
        
        # Квадрат
        for x in range(0, size, half):
            for y in range((x + half) % step, size, step):
                total = 0
                count = 0
                if x >= half:
                    total += array_pixels[x-half, y]
                    count += 1
                if x + half < size:
                    total += array_pixels[x+half, y]
                    count += 1
                if y >= half:
                    total += array_pixels[x, y-half]
                    count += 1
                if y + half < size:
                    total += array_pixels[x, y+half]
                    count += 1
                if count > 0:
                    avg = total / count
                    array_pixels[x, y] = avg + np.random.uniform(-rand_range, rand_range)
        
        step = half
        rand_range *= roughness

    return array_pixels


def generate_plasma(img_name='plasma.png', algorithm=square_diamond_algorithm, size=2**8, roughness=.5):
    plasma = algorithm(size, roughness)

    img = Image.new('RGB', (size+1, size+1))
    img_pixel_access = img.load()

    # Преобразование значений в цвета методом фазового кодирования.
    # Цветовая модель осуществляется поворотом по цветовому кругу.
    # 0 - красный, 120 - зелёный, 240 - синий.
    for x in range(size+1):
        for y in range(size+1):
            value = plasma[x, y]
            r = int(128 + 127 * math.sin(value * 0.1))
            g = int(128 + 127 * math.sin(value * 0.1 + 2))
            b = int(128 + 127 * math.sin(value * 0.1 + 4))
            img_pixel_access[x, y] = (r, g, b)
    
    img.save(img_name)


def main():
    generate_plasma()

if __name__ == '__main__':
    main()