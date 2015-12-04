import random

from PIL import ImageColor





#red = (222, 90, 81, 255) #DE5A51
#blue = (97, 205, 245, 255) #61CDF5
#white = (242, 241, 237, 255) #F2F1ED
#black = (5,5,5,255) #555

red = ImageColor.getrgb('#DE5A51')
blue = ImageColor.getrgb('#61CDF5')
white = ImageColor.getrgb('#F2F1ED')
black = ImageColor.getrgb('#050505')

orange = ImageColor.getrgb('#E66643')
purp = ImageColor.getrgb('#5B32B2')

dgreen = ImageColor.getrgb('#4E8B61')
lgreen = ImageColor.getrgb('#77DD77')
burg = ImageColor.getrgb('#520519')

colors = [red, blue, white, orange, purp, dgreen, lgreen, burg ]


def contrasting_colors(color):
    return [c for c in colors if c != color]

def get_random_color(color = None):
    if color == None:
        return random.choice(colors)
    else:
        return random.choice(contrasting_colors(color))


