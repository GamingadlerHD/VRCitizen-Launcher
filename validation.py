from screeninfo import get_monitors

def validate_resolution(width, height):
    for m in get_monitors():
        if m.width > width and m.height > height:
            return True
    return False
