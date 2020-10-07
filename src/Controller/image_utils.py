from io import BytesIO
from PIL import Image


class ImageUtils(object):

    def image_to_bytes(self, image: Image):
        buf = BytesIO()
        image.save(buf, 'JPEG')
        buf.seek(0)
        image_bytes = buf.read()
        buf.close()
        return image_bytes

    def bytes_to_image(self, binary_img):
        img_bytes = BytesIO(binary_img)
        img_bytes.seek(0)
        img = Image.open(img_bytes)
        return img

    def bytes_to_bytesIO(self, binary_img):
        img_bytes = BytesIO(binary_img)
        img_bytes.seek(0)
        return img_bytes

