from PIL import Image
from io import BytesIO

def convert_image_to_pdf(image_bytes: bytes) -> bytes:
    """
    Converts image bytes to PDF bytes
    """
    image = Image.open(BytesIO(image_bytes))

    if image.mode != "RGB":
        image = image.convert("RGB")

    pdf_bytes = BytesIO()
    image.save(pdf_bytes, format="PDF")
    pdf_bytes.seek(0)

    return pdf_bytes.read()
