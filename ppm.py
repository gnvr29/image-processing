import math
from math import sqrt
from typing import List

from graph import Graph


class Pixel:
    def __init__(self, r : int, g : int, b : int):
        self.r = r
        self.g = g
        self.b = b

class PpmHeader:
    def __init__(self, image_format : str, columns : int, rows : int, max_color_value : int):
        self.image_format = image_format
        self.columns = columns
        self.rows = rows
        self.max_color_value = max_color_value

class PpmBody:
    def __init__(self, pixel_grid : List[List[Pixel]]):
        self.pixel_grid = pixel_grid

class PPM:
    def __init__(self, image_path : str):
        self.header : PpmHeader = None
        self.body : PpmBody = None

    def parse_ppm(self, image_path : str) -> None:
        """
        Parses PPM image and extracts the header data and pixel grid,
        creates PpmHeader and PpmBody objects and then sets the class objects
        :param image_path:
        :return: None
        """
        with open(image_path, 'r') as file:
            all_values = []
            for line in file:
                if line.startswith('#'):
                    continue
                all_values.extend(line.strip().split())

        # extracts the header
        image_format = all_values[0]
        columns = int(all_values[1])
        rows = int(all_values[2])
        max_color_value = int(all_values[3])
        self.header = PpmHeader(image_format, columns, rows, max_color_value)

        # extracts the body
        pixels = all_values[4:]

        pixel_grid : List[List[Pixel]] = []
        pixel_index = 0
        for i in range(rows):
            row = []
            for c in range(columns):
                r = int(pixels[pixel_index])
                g = int(pixels[pixel_index + 1])
                b = int(pixels[pixel_index + 2])
                pixel = Pixel(r, g, b)
                row.append(pixel)
                pixel_index += 3
            pixel_grid.append(row)

        self.body = PpmBody(pixel_grid)

    @staticmethod
    def calculate_similarity(pixel_a : Pixel, pixel_b : Pixel, sigma : float):
        """
        Takes in two pixels and a sigma value to calculate the color similarity between two pixels
        using the gaussian similarity function:

        :param pixel_a:
        :param pixel_b:
        :param sigma:
        :return: gaussian similarity
        """
        euclidean_distance = sqrt(
            (pixel_a.r - pixel_b.r) ** 2 + (pixel_a.g - pixel_b.g) ** 2 + (pixel_a.b - pixel_b.b) ** 2
        )
        gaussian_similarity = math.exp(-(euclidean_distance ** 2) / (2 * (sigma ** 2)))
        return gaussian_similarity

