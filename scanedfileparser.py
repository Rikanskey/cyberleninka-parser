import pytesseract
from wand.image import Image as wi
from PIL import Image
from io import BytesIO

TEXT_FILE_NAME = 'text.txt'


def parse_scan(pdf_file_name):
    pdf_file = wi(filename=pdf_file_name, resolution=300)
    pdf_image = pdf_file.convert('jpeg')
    img_blobs = []
    file = open(TEXT_FILE_NAME, 'w')

    for img in pdf_image.sequence:
        page = wi(image=img)
        img_blobs.append(page.make_blob('jpeg'))

    for img in img_blobs:
        im = Image.open(BytesIO(img))
        file.write(pytesseract.image_to_string(im, lang='rus+eng'))

    file.close()
    return TEXT_FILE_NAME


if __name__ == '__main__':
    parse_scan('test.pdf')

