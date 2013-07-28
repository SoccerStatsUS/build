from PIL import Image

def resize(p):
    i = Image.open(p)
    if i.size[1] > 200:
        ratio = i.size[0] / 200.0
        dims = [int(e / ratio) for e in i.size]
    else:
        dims = i.size

    i = i.resize(dims, Image.ANTIALIAS)
    i.save(p, optimize=True, quality=95)

