from screeninfo import get_monitors

def validate_resolution(width, height):
    return (any(m.width >= width and m.height >= height for m in get_monitors()))
