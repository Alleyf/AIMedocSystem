from PIL import Image
from django.http import HttpResponse

from AIMeDocSys import settings


def images(request, path):
    im = Image.open(settings.STATIC_ROOT + path)
    x, y = im.size
    im = im.resize((int(x / 1.5), int(y / 1.5)), Image.ANTIALIAS)
    response = HttpResponse(mimetype="image/png")
    # 将PIL的image对象写入response中，通过response返回
    im.save(response, "PNG")
    return response
