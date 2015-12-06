import random

from PIL import ImageColor


red = ImageColor.getrgb('#DE5A51')
blue = ImageColor.getrgb('#61CDF5')
white = ImageColor.getrgb('#F2F1ED')
black = ImageColor.getrgb('#050505')
orange = ImageColor.getrgb('#E66643')
purp = ImageColor.getrgb('#5B32B2')
dgreen = ImageColor.getrgb('#4E8B61')
lgreen = ImageColor.getrgb('#77DD77')
burg = ImageColor.getrgb('#520519')

color_universe = [red, blue, white, orange, purp, dgreen, lgreen, burg]


def contrasting_colors(color, contrast_against=None):
    if contrast_against is None:
        return [c for c in color_universe if c != color]
    else:
        return [c for c in contrast_against if c != color]


def get_random_contrasting_color(color=None, contrast_against=None):
    if contrast_against == None:
        contrast_against = color_universe

    if color is None:
        return random.choice(contrast_against)
    else:
        return random.choice(contrasting_colors(color, contrast_against))
