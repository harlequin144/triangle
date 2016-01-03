from enum import Enum
from PIL import ImageColor
import random


class ColorLayers(Enum):
    red = 0
    blue = 1
    white = 2
    black = 3
    orange = 4
    purp = 5
    dgreen = 6
    lgreen = 7
    burg = 8


def get_color_from_color_layer(color_layer):
    if color_layer == ColorLayers.red:
        return ImageColor.getrgb('#DE5A51')
    elif color_layer == ColorLayers.blue:
        return ImageColor.getrgb('#61CDF5')
    elif color_layer == ColorLayers.white:
        return ImageColor.getrgb('#F2F1ED')
    elif color_layer == ColorLayers.black:
        return ImageColor.getrgb('#050505')
    elif color_layer == ColorLayers.orange:
        return ImageColor.getrgb('#E66643')
    elif color_layer == ColorLayers.purp:
        return ImageColor.getrgb('#5B32B2')
    elif color_layer == ColorLayers.dgreen:
        return ImageColor.getrgb('#4E8B61')
    elif color_layer == ColorLayers.lgreen:
        return ImageColor.getrgb('#77DD77')
    elif color_layer == ColorLayers.burg:
        return ImageColor.getrgb('#520519')


def contrasting_colors(color_layer, contrast_against=None):
    if contrast_against is None:
        return [c for c in list(ColorLayers) if c != color_layer]
    else:
        return [c for c in contrast_against if c != color_layer]


def get_random_contrasting_color(color_layer=None, contrast_against=None):
    if contrast_against is None:
        print('in here')
        contrast_against = list(ColorLayers)

    if color_layer is None:
        return random.choice(contrast_against)
    else:
        return random.choice(contrasting_colors(color_layer, contrast_against))
